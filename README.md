# sast-batch-runner

One container image that clones a git repo, runs **Semgrep OSS** and **SonarQube Community Build**, normalizes both into a single finding model, and publishes HTML/Markdown/JSON/SARIF reports to S3. Designed to run as an **AWS Batch job on Fargate**.

---

## Topology decision

| # | Topology | SonarQube | Cost at idle | Cold start | Use it for |
|---|---|---|---|---|---|
| 1 | **Semgrep-only** | none | $0 | ~15 s | Default. Fast, reliable, no server. Your safe demo fallback. |
| 2 | **Ephemeral SonarQube** (multi-container Batch job) | in-task, H2, dies with the job | $0 | 90–180 s | The demo. Both tools, zero standing infrastructure. |
| 3 | **Persistent SonarQube** (ECS service + RDS Postgres + ALB) | long-lived | ~$70–120/mo | 0 s | Production. Trend lines, quality gates, historical baselines. |

Ship 1 and 2. Mention 3 as the production path — it is the same image, you just point `SONAR_HOST_URL` at the real server and supply a pre-provisioned `SONAR_TOKEN`.

### Two non-obvious blockers this repo already solves

1. **Elasticsearch `vm.max_map_count`.** SonarQube 7.8+ embeds Elasticsearch, which refuses to boot unless the host kernel has `vm.max_map_count >= 262144`. That sysctl is **not namespaced**, so on Fargate you cannot set it — not via `--sysctl`, not via task definition `systemControls`. Fix: `SONAR_SEARCH_JAVAADDITIONALOPTS=-Dnode.store.allow_mmap=false`, which switches ES off mmap storage and removes the bootstrap check.
2. **The Compute Engine async gap.** `sonar-scanner` uploads a payload and exits; the server processes it **asynchronously**. Query `/api/issues` immediately and you get zero results. `scan_runner.py` reads `ceTaskUrl` from `.scannerwork/report-task.txt` and polls until `SUCCESS` before pulling findings.

> On the embedded H2 database: current SonarQube docs still ship H2 and explicitly sanction it for development, testing, CI/CD, and trials — not production. Some third-party blogs claim it was removed in 10.2; that is not what the official docs say. Verify against your pinned tag before the demo.

---

## Layout

```
sast-batch/
├── Dockerfile                  # multi-stage; scanner CLI fetched in stage 1
├── requirements.txt
├── entrypoint.sh               # tini -> bash -> exec python
├── scan_runner.py              # orchestrator: clone -> semgrep -> sonar -> report -> S3
├── report_builder.py           # SARIF + Sonar API -> one model -> html/md/json
├── docker-compose.yml          # local parity test, 1:1 with the Fargate topology
└── aws/
    ├── 01_build_push_ecr.sh
    ├── 02_batch_infra.sh
    ├── job-definition-semgrep.json
    ├── job-definition-multicontainer.json
    └── 03_submit_job.sh
```

---

## Configuration surface

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `REPO_URL` | yes | — | Git URL to scan |
| `REPO_BRANCH` | no | repo default | Branch to shallow-clone |
| `GIT_TOKEN_SECRET_ARN` | no | — | Secrets Manager ARN for a private-repo PAT (**preferred**) |
| `GIT_TOKEN` | no | — | Raw PAT. Demo only — visible in the job definition |
| `S3_BUCKET` | no | — | Report destination; omit and reports stay in-container |
| `S3_PREFIX` | no | `sast-reports/<slug>/<jobid>` | Object prefix |
| `SEMGREP_CONFIGS` | no | `p/security-audit,p/owasp-top-ten,p/secrets` | Comma-separated rulesets |
| `SEMGREP_RULE_TIMEOUT` | no | `60` | Per-rule-per-file seconds |
| `SONAR_HOST_URL` | no | — | Unset ⇒ Semgrep-only mode |
| `SONAR_TOKEN` | no | — | Pre-provisioned analysis token (persistent server) |
| `SONAR_ADMIN_PASSWORD` | no | — | Used to mint a token when `SONAR_TOKEN` is unset (ephemeral) |
| `SONAR_PROJECT_KEY` | no | repo slug | Project key on the server |
| `SONAR_STARTUP_TIMEOUT` | no | `420` | Seconds to wait for status `UP` |
| `FAIL_ON_SEVERITY` | no | `none` | `critical`\|`high`\|`medium`\|`low`\|`info` ⇒ exit 1 at/above |

---

## Local test first

```bash
docker compose up --build --abort-on-container-exit scanner
open ./out/report.html
```

Never debug a container for the first time inside Batch. The compose file is deliberately 1:1 with the Fargate multi-container topology — the only difference is `SONAR_HOST_URL` (`http://sonarqube:9000` in compose, `http://localhost:9000` on Fargate, where both containers share a network namespace).

---

## AWS onboarding

```bash
export AWS_REGION=us-east-1
export S3_BUCKET=my-sast-reports
export SUBNETS=subnet-aaa,subnet-bbb
export SECURITY_GROUPS=sg-xxxxxxxx

# 1. log group (Batch will NOT create this for you — jobs fail at STARTING without it)
aws logs create-log-group --log-group-name /aws/batch/sast --region $AWS_REGION

# 2. build + push
cd aws && ./01_build_push_ecr.sh          # prints IMAGE_URI and the immutable digest

# 3. IAM + compute environment + queue
./02_batch_infra.sh

# 4. render the job definition placeholders and register
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
sed -e "s/REPLACE_ACCOUNT/$ACCOUNT_ID/g" \
    -e "s/REPLACE_REGION/$AWS_REGION/g" \
    -e "s/REPLACE_BUCKET/$S3_BUCKET/g" \
    -e "s/REPLACE_TAG/$IMAGE_TAG/g" \
    job-definition-semgrep.json > /tmp/jd.json
aws batch register-job-definition --cli-input-json file:///tmp/jd.json --region $AWS_REGION

# 5. run
./03_submit_job.sh https://github.com/juice-shop/juice-shop.git master
```

For the both-tools run, repeat step 4 with `job-definition-multicontainer.json` and submit with `JOB_DEF=sast-semgrep-sonarqube`.

### Networking

Fargate must reach ECR, S3, CloudWatch Logs, Secrets Manager, `semgrep.dev` (rule packs), and the git host.

- **Public subnet:** set `assignPublicIp: ENABLED` (already set in both job definitions).
- **Private subnet:** requires a NAT gateway, or VPC endpoints for `ecr.api`, `ecr.dkr`, `s3` (gateway), `logs`, `secretsmanager` — plus NAT for the registry and git host regardless.
- **A job stuck in `RUNNABLE` forever** is nearly always no route to ECR, or `maxvCpus` saturated.

---

## Demo runbook

| Beat | What you show | Point you make |
|---|---|---|
| 1 | `aws batch submit-job` against Juice Shop | One image, per-run overrides, no infrastructure touched |
| 2 | CloudWatch log stream, live | Phase timing is visible: clone → semgrep → sonar CE polling |
| 3 | `report.html` from a presigned S3 URL | Two engines, one severity ladder, commit-pinned evidence |
| 4 | `summary.json` | Machine-readable — this is what feeds Security Hub / DefectDojo next |
| 5 | Set `FAIL_ON_SEVERITY=high`, resubmit | Same artifact, job now exits 1 — the CI gate |

Pre-warm the ECR image and do one throwaway run before you present: the first Semgrep run downloads rule packs, and cold Fargate ENI attachment adds 30–60 s.

---

## Hardening backlog (say this out loud in the demo — it shows roadmap thinking)

1. **Baseline diffing** — persist `findings.json` per commit in S3, gate on *new* findings only. Kills alert fatigue on legacy code.
2. **Security Hub** — convert SARIF to ASFF and `BatchImportFindings`, so SAST lands in the same pane as GuardDuty and Inspector.
3. **Array jobs** — `--array-properties size=50` to fan out across a repo portfolio in one submit.
4. **FARGATE_SPOT** — ~70% cheaper; safe once `retryStrategy` handles reclaim.
5. **Offline rules** — vendor the Semgrep packs into the image so scans work in an air-gapped VPC and are byte-reproducible.
6. **Sign the image** — cosign + ECR, and verify at job start.
