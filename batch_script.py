#!/usr/bin/env python3
"""
scan_runner.py — orchestrates one SAST batch job against one git repository.

Pipeline:  resolve config -> clone -> Semgrep -> SonarQube (optional) -> merge -> report -> S3

Every knob is an environment variable so a SINGLE container image serves every repo;
the AWS Batch job definition holds defaults and `submit-job --container-overrides`
supplies the per-run values.
"""

import json
import os
import subprocess
import sys
import tarfile
import time
import shutil
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests

from report_builder import build_reports

# --------------------------------------------------------------------------------------
# DEMO ONLY — intentional vulnerabilities for testing the SAST pipeline's own detection
# capability. Not used by any real code path below. Safe to remove.
# --------------------------------------------------------------------------------------
import pickle
import hashlib
import random

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "SuperSecret123!"


def _demo_run_user_command(user_input: str):
    subprocess.run(f"echo {user_input}", shell=True)


def _demo_ping_host(hostname: str):
    os.system("ping -c 1 " + hostname)


def _demo_evaluate_expression(expr: str):
    return eval(expr)


def _demo_load_user_data(raw_bytes: bytes):
    return pickle.loads(raw_bytes)


def _demo_hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def _demo_generate_session_token() -> str:
    return str(random.randint(100000, 999999))


def _demo_read_report(filename: str) -> str:
    with open("/tmp/reports/" + filename) as f:
        return f.read()

# --------------------------------------------------------------------------------------
# Configuration layer
# --------------------------------------------------------------------------------------

# Path constants. /workspace and /out were created and chowned in the Dockerfile.
# On Fargate these live on the task's ephemeral storage (20 GiB default, up to 200 GiB).
WORKSPACE = Path(os.environ.get("WORKSPACE_DIR", "/workspace"))
OUTDIR = Path(os.environ.get("OUTPUT_DIR", "/out"))


def env(key: str, default=None, required: bool = False) -> str:
    """Read an env var, strip whitespace, and hard-fail early if a required one is absent.

    Failing at second 0 instead of at minute 6 (after the clone and the Semgrep run)
    is the single highest-value thing you can do for batch job UX.
    """
    val = os.environ.get(key, default)
    if val is not None:
        val = str(val).strip()
    if required and not val:
        sys.exit(f"[FATAL] Required environment variable {key} is not set.")
    return val


def log(msg: str) -> None:
    """Timestamped, unbuffered log line.

    CloudWatch Logs applies its own ingest timestamp, but that is the time the line was
    *received*. Embedding our own UTC stamp lets you measure real phase durations when
    the log stream is backed up.
    """
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd: list, cwd: Path = None, timeout: int = 3600, check: bool = False):
    """Thin subprocess wrapper.

    - `cmd` is a LIST, never a string: no shell is spawned, so a repo name containing
      `; rm -rf /` is passed as a literal argument. This is the command-injection control
      for the whole script.
    - stdout/stderr are captured as text and echoed, so scanner output lands in CloudWatch.
    - `timeout` prevents a pathological repo from pinning the job until the Batch
      `attemptDurationSeconds` timeout burns the full Fargate spend.
    """
    log(f"$ {' '.join(cmd)}")
    proc = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None,
        capture_output=True, text=True, timeout=timeout,
    )
    if proc.stdout:
        print(proc.stdout, flush=True)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, flush=True)
    if check and proc.returncode != 0:
        sys.exit(f"[FATAL] Command failed with exit {proc.returncode}: {' '.join(cmd)}")
    return proc


# --------------------------------------------------------------------------------------
# Secrets
# --------------------------------------------------------------------------------------

def get_secret(secret_id: str) -> str:
    """Fetch a secret value from AWS Secrets Manager using the task role's credentials.

    Deliberately NOT passed as a plain env var in the job definition: anything in
    `containerProperties.environment` is visible to anyone with batch:DescribeJobDefinitions.
    Secrets Manager keeps the value out of the control plane and gives you rotation + audit.
    """
    import boto3  # imported lazily so a Semgrep-only run never pays the boto3 import cost
    client = boto3.client("secretsmanager")
    resp = client.get_secret_value(SecretId=secret_id)
    raw = resp["SecretString"]
    # Accept both a bare string secret and a JSON blob like {"token": "ghp_..."}.
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            for k in ("token", "password", "value", "GITHUB_TOKEN"):
                if k in parsed:
                    return parsed[k]
        return raw
    except json.JSONDecodeError:
        return raw


# --------------------------------------------------------------------------------------
# Phase 1 — clone
# --------------------------------------------------------------------------------------

def clone_repo(repo_url: str, branch: str, token: str | None) -> Path:
    """Shallow-clone the target repository into /workspace/src.

    --depth 1          : fetch only the tip commit. On a large monorepo this is the
                         difference between a 4-second clone and a 4-minute one.
    --single-branch    : do not fetch refs for every other branch.
    --no-tags          : tags are irrelevant to a point-in-time SAST scan.
    GIT_TERMINAL_PROMPT=0 : if auth fails, fail immediately instead of blocking forever
                         on an interactive username prompt — a classic batch-job hang.
    """
    dest = WORKSPACE / "src"
    if dest.exists():
        shutil.rmtree(dest)  # idempotency: Batch retries reuse the same ephemeral volume

    auth_url = repo_url
    if token:
        # Inject the credential into the URL. `x-access-token` is GitHub's convention for
        # PAT/App tokens; GitLab uses `oauth2`. urlsplit/urlunsplit avoids naive string
        # surgery that breaks on URLs that already contain a userinfo component.
        parts = urllib.parse.urlsplit(repo_url)
        auth_url = urllib.parse.urlunsplit((
            parts.scheme,
            f"x-access-token:{token}@{parts.netloc}",
            parts.path, parts.query, parts.fragment,
        ))

    cmd = ["git", "clone", "--depth", "1", "--single-branch", "--no-tags"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [auth_url, str(dest)]

    e = os.environ.copy()
    e["GIT_TERMINAL_PROMPT"] = "0"
    log(f"Cloning {repo_url} (branch={branch or 'default'})")
    proc = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=900)
    if proc.returncode != 0:
        # Scrub the token out of git's error message before it reaches CloudWatch.
        # Git happily echoes the full remote URL on failure — this is a real leak path.
        stderr = proc.stderr.replace(token, "***") if token else proc.stderr
        sys.exit(f"[FATAL] git clone failed:\n{stderr}")

    # Record the exact commit under test. A report without a commit SHA is not evidence.
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=dest,
                         capture_output=True, text=True).stdout.strip()
    log(f"Cloned at commit {sha}")
    return dest, sha


# --------------------------------------------------------------------------------------
# Phase 2 — Semgrep
# --------------------------------------------------------------------------------------

def fetch_source_archive(s3_uri: str) -> Path:
    """Download and extract a source tarball uploaded by the CI workflow.

    Used for PR scans: GitHub Actions has already checked out the exact PR
    commit (including whatever merge-ref semantics GitHub applies), so
    re-cloning via git inside the container would be redundant AND would
    require passing a GitHub token into Batch. Downloading a pre-packaged
    tarball avoids both — nothing in this path ever sees a git credential.
    """
    dest = WORKSPACE / "src"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    import boto3
    bucket, key = s3_uri.replace("s3://", "", 1).split("/", 1)
    tar_path = WORKSPACE / "source.tar.gz"
    log(f"Downloading source archive from {s3_uri}")
    boto3.client("s3").download_file(bucket, key, str(tar_path))

    with tarfile.open(tar_path) as tar:
        # filter="data" (Python 3.12+) blocks path traversal / symlink escapes
        # from a malicious archive — the same class of risk as an untrusted zip.
        tar.extractall(dest, filter="data")
    tar_path.unlink()
    log(f"Extracted source archive to {dest}")
    return dest


def run_semgrep(src: Path, configs: list, timeout_per_rule: int) -> Path:
    """Run Semgrep OSS and emit SARIF.

    SARIF (not Semgrep's native JSON) because it is the OASIS standard consumed by
    GitHub Advanced Security, Azure DevOps, DefectDojo, and AWS Security Hub via
    the ASFF converter. One output format, many downstream sinks.
    """
    sarif_path = OUTDIR / "semgrep.sarif"

    cmd = ["semgrep", "scan"]
    for cfg in configs:
        # One --config flag per ruleset; Semgrep unions them and de-duplicates findings.
        # p/security-audit, p/owasp-top-ten, p/secrets are free registry packs.
        cmd += ["--config", cfg]
    cmd += [
        "--sarif",                          # emit SARIF 2.1.0
        "--output", str(sarif_path),
        "--metrics", "off",                 # no telemetry egress
        "--timeout", str(timeout_per_rule), # per-rule-per-file cap, seconds
        "--timeout-threshold", "3",         # skip a file after 3 rule timeouts on it
        "--max-target-bytes", "2000000",    # skip files >2MB: minified JS/vendored blobs
        "--exclude", "node_modules",
        "--exclude", "vendor",
        "--exclude", ".git",
        "--jobs", str(os.cpu_count() or 2), # parallelism = vCPUs allocated by Fargate
        str(src),
    ]

    proc = run(cmd, timeout=3600)

    # Semgrep exit-code contract: 0 = clean, 1 = findings present, >=2 = the scan itself
    # errored. Only >=2 is a job failure. Treating 1 as failure would break every run
    # against a real codebase and make the report never get generated.
    if proc.returncode >= 2:
        sys.exit(f"[FATAL] Semgrep engine error (exit {proc.returncode})")
    if not sarif_path.exists():
        sys.exit("[FATAL] Semgrep produced no SARIF output")

    log(f"Semgrep complete -> {sarif_path}")
    return sarif_path


# --------------------------------------------------------------------------------------
# Phase 3 — SonarQube
# --------------------------------------------------------------------------------------

def wait_for_sonar(host: str, token: str, max_wait: int = 420) -> None:
    """Block until the SonarQube server reports status UP.

    Only relevant in the ephemeral/sidecar topology, where the server container is
    booting in parallel with this one. /api/system/status is unauthenticated and returns
    STARTING -> DB_MIGRATION_RUNNING -> UP. A cold SonarQube CE with H2 takes 90-150s.
    """
    deadline = time.time() + max_wait
    while time.time() < deadline:
        try:
            r = requests.get(f"{host}/api/system/status", timeout=10)
            status = r.json().get("status")
            if status == "UP":
                log("SonarQube server is UP")
                return
            log(f"SonarQube status={status}, waiting...")
        except requests.RequestException as exc:
            log(f"SonarQube not reachable yet ({exc.__class__.__name__})")
        time.sleep(10)
    sys.exit(f"[FATAL] SonarQube did not reach UP within {max_wait}s")


def bootstrap_sonar_token(host: str, admin_user: str, admin_pass: str) -> str:
    """Mint a short-lived analysis token from admin credentials.

    Only used in the EPHEMERAL topology, where the SonarQube container is created fresh
    for this job and therefore has no pre-provisioned token. For a persistent server you
    generate the token once in the UI and store it in Secrets Manager instead.

    POST /api/user_tokens/generate returns the plaintext token exactly once — SonarQube
    stores only a hash, so there is no way to read it back later.
    """
    name = f"batch-{int(time.time())}"
    r = requests.post(
        f"{host}/api/user_tokens/generate",
        params={"name": name, "type": "GLOBAL_ANALYSIS_TOKEN"},
        auth=(admin_user, admin_pass), timeout=30,
    )
    if r.status_code != 200:
        sys.exit(f"[FATAL] Could not mint Sonar token (HTTP {r.status_code}): {r.text[:300]}")
    log(f"Minted ephemeral Sonar analysis token '{name}'")
    return r.json()["token"]


def run_sonar_scanner(src: Path, host: str, token: str, project_key: str,
                      project_name: str, sha: str) -> str:
    """Invoke sonar-scanner and return the Compute Engine task URL.

    The scanner does NOT analyse locally-and-report. It uploads a payload; the server's
    Compute Engine then processes it ASYNCHRONOUSLY. If you query /api/issues the instant
    the scanner exits, you get an empty set. That async gap is the #1 reason CI Sonar
    integrations silently report zero findings.
    """
    cmd = [
        "sonar-scanner",
        f"-Dsonar.host.url={host}",
        f"-Dsonar.token={token}",              # replaces the deprecated -Dsonar.login
        f"-Dsonar.projectKey={project_key}",
        f"-Dsonar.projectName={project_name}",
        f"-Dsonar.projectVersion={sha[:12]}",  # ties the analysis to the commit
        f"-Dsonar.sources={src}",
        "-Dsonar.sourceEncoding=UTF-8",
        "-Dsonar.scm.disabled=true",           # shallow clone has no usable history;
                                               # leaving SCM on produces blame warnings
        "-Dsonar.exclusions=**/node_modules/**,**/vendor/**,**/*.min.js,**/dist/**",
        f"-Dsonar.working.directory={OUTDIR}/.scannerwork",
    ]
    proc = run(cmd, cwd=src, timeout=3600)
    if proc.returncode != 0:
        sys.exit(f"[FATAL] sonar-scanner failed with exit {proc.returncode}")

    # The scanner drops report-task.txt containing ceTaskId / ceTaskUrl. This is the
    # documented handoff point between the scanner and the server's async processing.
    task_file = OUTDIR / ".scannerwork" / "report-task.txt"
    props = {}
    for line in task_file.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip()
    return props.get("ceTaskUrl")


def wait_for_ce_task(ce_task_url: str, token: str, max_wait: int = 900) -> None:
    """Poll the Compute Engine task until SUCCESS, then it is safe to query the API.

    Auth uses HTTP Basic with the token as the USERNAME and an EMPTY password —
    that is SonarQube's documented token auth scheme, and it trips up everyone once.
    """
    deadline = time.time() + max_wait
    while time.time() < deadline:
        r = requests.get(ce_task_url, auth=(token, ""), timeout=15)
        status = r.json().get("task", {}).get("status")
        log(f"Sonar CE task status={status}")
        if status == "SUCCESS":
            return
        if status in ("FAILED", "CANCELED"):
            sys.exit(f"[FATAL] Sonar Compute Engine task ended as {status}")
        time.sleep(5)
    sys.exit("[FATAL] Sonar CE task did not complete in time")


def fetch_sonar_findings(host: str, token: str, project_key: str) -> dict:
    """Pull issues + security hotspots via the Web API, handling pagination.

    Two separate endpoints, because SonarQube models them differently:
      /api/issues/search   -> bugs, vulnerabilities, code smells (has `impacts` in 10.x+)
      /api/hotspots/search -> security hotspots, which are REVIEW items, not findings
    SonarQube's paging caps at p*ps <= 10000; the loop respects that ceiling.
    """
    issues, page = [], 1
    while True:
        r = requests.get(
            f"{host}/api/issues/search",
            params={"componentKeys": project_key, "ps": 500, "p": page,
                    "resolved": "false"},
            auth=(token, ""), timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        issues.extend(data.get("issues", []))
        total = data.get("paging", {}).get("total", 0)
        if len(issues) >= total or page * 500 >= 10000:
            break
        page += 1

    # Hotspots are fetched best-effort. SonarQube Community Edition has inconsistent
    # behavior authorizing the Hotspots API against an ephemeral admin-minted analysis
    # token — it can 403 even though the identical token/auth scheme just succeeded
    # against /api/issues/search seconds earlier. Hotspots are "needs manual review"
    # items, not confirmed findings, so losing them must never take down a report that
    # already contains real Bugs/Vulnerabilities/Code Smells from the issues endpoint.
    hotspots, page = [], 1
    try:
        while True:
            r = requests.get(
                f"{host}/api/hotspots/search",
                params={"projectKey": project_key, "ps": 500, "p": page},
                auth=(token, ""), timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            hotspots.extend(data.get("hotspots", []))
            total = data.get("paging", {}).get("total", 0)
            if len(hotspots) >= total or page * 500 >= 10000:
                break
            page += 1
    except requests.exceptions.HTTPError as exc:
        log(f"[WARN] Hotspots API returned {exc.response.status_code} — "
            f"continuing without hotspots (issues are unaffected)")
        hotspots = []

    log(f"SonarQube returned {len(issues)} issues, {len(hotspots)} hotspots")
    return {"issues": issues, "hotspots": hotspots}


# --------------------------------------------------------------------------------------
# Phase 5 — publish
# --------------------------------------------------------------------------------------

def upload_to_s3(bucket: str, prefix: str, files: list) -> list:
    """Copy every generated artifact to S3 under a run-scoped prefix.

    Batch tasks are ephemeral — when the container exits, /out is gone. S3 is the only
    durable sink. ServerSideEncryption is set explicitly rather than relying on the
    bucket default, so the object is encrypted even if someone edits the bucket policy.
    """
    import boto3
    s3 = boto3.client("s3")
    uploaded = []
    ctypes = {".html": "text/html", ".json": "application/json",
              ".sarif": "application/json", ".md": "text/markdown"}
    for f in files:
        f = Path(f)
        if not f.exists():
            continue
        key = f"{prefix.rstrip('/')}/{f.name}"
        s3.upload_file(
            str(f), bucket, key,
            ExtraArgs={"ContentType": ctypes.get(f.suffix, "application/octet-stream"),
                       "ServerSideEncryption": "AES256"},
        )
        uri = f"s3://{bucket}/{key}"
        log(f"Uploaded {uri}")
        uploaded.append(uri)
    return uploaded


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------

def main() -> int:
    started = time.time()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    # ---- config ----
    s3_bucket = env("S3_BUCKET")
    # AWS_BATCH_JOB_ID is injected by AWS Batch automatically — free correlation ID
    # that ties the S3 prefix, the CloudWatch log stream, and the report together.
    job_id = env("AWS_BATCH_JOB_ID", f"local-{int(started)}")

    source_s3_uri = env("SOURCE_S3_URI")

    if source_s3_uri:
        # PR-scan mode: CI already checked out the exact commit and packaged
        # it. No git clone, no GitHub token ever enters this container.
        repo_url = env("REPO_FULL_NAME", "")
        branch = env("REPO_BRANCH", "")
        slug = env("REPO_SLUG", "pr-scan").replace(" ", "_")
        sha = env("COMMIT_SHA", "unknown")
        src = fetch_source_archive(source_s3_uri)
    else:
        # Standalone mode: same git-clone path used for manual/demo runs.
        repo_url = env("REPO_URL", required=True)
        branch = env("REPO_BRANCH", "")
        # Derive a safe project slug from the repo URL: "https://github.com/org/repo.git" -> "org-repo"
        slug = repo_url.rstrip("/").removesuffix(".git").split("/")[-2:]
        slug = "-".join(slug).replace(" ", "_")

        # ---- git token ----
        token = None
        if env("GIT_TOKEN_SECRET_ARN"):
            token = get_secret(env("GIT_TOKEN_SECRET_ARN"))
        elif env("GIT_TOKEN"):
            token = env("GIT_TOKEN")  # acceptable for a public-repo demo, not for production

        # ---- clone ----
        src, sha = clone_repo(repo_url, branch, token)

    s3_prefix = env("S3_PREFIX", f"sast-reports/{slug}/{job_id}")

    # ---- semgrep ----
    configs = [c.strip() for c in env(
        "SEMGREP_CONFIGS", "p/security-audit,p/owasp-top-ten,p/secrets"
    ).split(",") if c.strip()]
    sarif_path = run_semgrep(src, configs, int(env("SEMGREP_RULE_TIMEOUT", "60")))

    # ---- sonarqube (optional) ----
    sonar_data = None
    sonar_host = env("SONAR_HOST_URL")
    if sonar_host:
        project_key = env("SONAR_PROJECT_KEY", slug)
        # Readiness gate FIRST — in the ephemeral topology the server container is still
        # booting Elasticsearch when this container starts, so nothing below would work yet.
        wait_for_sonar(sonar_host, "", int(env("SONAR_STARTUP_TIMEOUT", "420")))

        sonar_token = env("SONAR_TOKEN")
        if not sonar_token:
            # No pre-provisioned token -> ephemeral mode: mint one from admin creds.
            sonar_token = bootstrap_sonar_token(
                sonar_host,
                env("SONAR_ADMIN_USER", "admin"),
                env("SONAR_ADMIN_PASSWORD", required=True),
            )
        ce_url = run_sonar_scanner(src, sonar_host, sonar_token,
                                   project_key, slug, sha)
        if ce_url:
            wait_for_ce_task(ce_url, sonar_token)
        sonar_data = fetch_sonar_findings(sonar_host, sonar_token, project_key)
    else:
        log("SONAR_HOST_URL not set — running Semgrep-only mode")

    # ---- report ----
    meta = {
        "repo_url": repo_url, "branch": branch or "default", "commit": sha,
        "job_id": job_id, "project": slug, "pr_number": env("PR_NUMBER"),
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "duration_sec": round(time.time() - started, 1),
        "sonar_host": sonar_host or None,
    }
    artifacts = build_reports(sarif_path, sonar_data, meta, OUTDIR)

    # ---- publish ----
    if s3_bucket:
        upload_to_s3(s3_bucket, s3_prefix, artifacts)
    else:
        log("S3_BUCKET not set — artifacts remain in the container only")

    # ---- quality gate ----
    # FAIL_ON_SEVERITY turns the job red when findings at or above a threshold exist.
    # Default "none" so a demo run always exits 0 and the report always publishes.
    summary = json.loads((OUTDIR / "summary.json").read_text())
    threshold = env("FAIL_ON_SEVERITY", "none").lower()
    order = ["info", "low", "medium", "high", "critical"]
    if threshold in order:
        idx = order.index(threshold)
        blocking = sum(summary["severity_counts"].get(s, 0) for s in order[idx:])
        log(f"Quality gate: {blocking} finding(s) at or above '{threshold}'")
        if blocking:
            log("[GATE] FAILED")
            return 1
    log(f"Done in {meta['duration_sec']}s — {summary['total']} findings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
