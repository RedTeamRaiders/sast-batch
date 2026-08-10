#!/usr/bin/env python3
"""
report_builder.py — normalizes Semgrep SARIF and SonarQube API output into ONE finding
model, then emits summary.json, findings.json, report.md and report.html.

Why normalize: Semgrep speaks SARIF levels (error/warning/note), SonarQube 10.x speaks
`impacts[].severity` (BLOCKER..INFO) plus a legacy `severity` field. Merging them into a
single 5-level scale is what makes a combined report readable and a quality gate possible.
"""

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

# Canonical severity ladder used everywhere downstream (gate, counts, sort order).
SEVERITIES = ["critical", "high", "medium", "low", "info"]

# Semgrep SARIF encodes severity two ways. The `level` field is coarse (3 values), while
# `properties.severity` carries Semgrep's own ERROR/WARNING/INFO. We prefer the richer
# security-severity property (a CVSS-like float) when the ruleset supplies it.
SARIF_LEVEL_MAP = {"error": "high", "warning": "medium", "note": "low", "none": "info"}

# SonarQube: both the modern MQR `impacts[].severity` and the legacy `severity` field.
SONAR_SEVERITY_MAP = {
    "BLOCKER": "critical", "CRITICAL": "critical",
    "HIGH": "high", "MAJOR": "high",
    "MEDIUM": "medium", "MINOR": "medium",
    "LOW": "low", "INFO": "info",
}


def _sarif_severity(result: dict, rules_by_id: dict) -> str:
    """Resolve one SARIF result to the canonical scale.

    Order of preference:
      1. rule.properties["security-severity"] — a 0.0-10.0 CVSS-style score that Semgrep's
         security packs populate. Most precise signal available.
      2. result.level — the SARIF-standard coarse level.
    """
    rule = rules_by_id.get(result.get("ruleId"), {})
    score = rule.get("properties", {}).get("security-severity")
    if score is not None:
        try:
            s = float(score)
            if s >= 9.0:
                return "critical"
            if s >= 7.0:
                return "high"
            if s >= 4.0:
                return "medium"
            return "low"
        except (TypeError, ValueError):
            pass
    return SARIF_LEVEL_MAP.get(result.get("level", "warning"), "medium")


def parse_sarif(sarif_path: Path) -> list:
    """Flatten SARIF 2.1.0 into a list of normalized finding dicts."""
    doc = json.loads(Path(sarif_path).read_text())
    findings = []
    for run in doc.get("runs", []):
        # Build a ruleId -> rule-object index once per run. SARIF stores rule metadata
        # (description, tags, CWE) separately from results to avoid repetition.
        rules_by_id = {
            r.get("id"): r
            for r in run.get("tool", {}).get("driver", {}).get("rules", [])
        }
        for res in run.get("results", []):
            rule_id = res.get("ruleId", "unknown")
            rule = rules_by_id.get(rule_id, {})

            # A SARIF result can have multiple locations; the first physical location is
            # the primary sink. Deeper locations are dataflow steps in taint-mode rules.
            loc = (res.get("locations") or [{}])[0]
            phys = loc.get("physicalLocation", {})
            region = phys.get("region", {})

            # Pull CWE identifiers out of the rule tags — these are what map the finding
            # to OWASP/ASVS in downstream GRC tooling.
            tags = rule.get("properties", {}).get("tags", [])
            cwes = [t for t in tags if str(t).upper().startswith("CWE")]

            findings.append({
                "source": "semgrep",
                "rule_id": rule_id,
                "severity": _sarif_severity(res, rules_by_id),
                "message": (res.get("message", {}) or {}).get("text", "").strip(),
                "file": phys.get("artifactLocation", {}).get("uri", ""),
                "line": region.get("startLine"),
                "snippet": (region.get("snippet", {}) or {}).get("text", "").strip(),
                "cwe": cwes,
                "help_uri": rule.get("helpUri", ""),
            })
    return findings


def parse_sonar(sonar_data: dict) -> list:
    """Flatten SonarQube issues + hotspots into the same normalized shape."""
    if not sonar_data:
        return []
    findings = []

    for issue in sonar_data.get("issues", []):
        # SonarQube 10.x+ Multi-Quality Rule mode: take the highest impact severity
        # across the software qualities (SECURITY / RELIABILITY / MAINTAINABILITY).
        impacts = issue.get("impacts") or []
        if impacts:
            sev = min(
                (SONAR_SEVERITY_MAP.get(i.get("severity", "MEDIUM"), "medium")
                 for i in impacts),
                key=SEVERITIES.index,   # min by ladder index = most severe
            )
        else:
            sev = SONAR_SEVERITY_MAP.get(issue.get("severity", "MAJOR"), "medium")

        # `component` is "projectKey:path/to/File.java" — strip the project prefix.
        component = issue.get("component", "")
        file_path = component.split(":", 1)[1] if ":" in component else component

        findings.append({
            "source": "sonarqube",
            "rule_id": issue.get("rule", ""),
            "severity": sev,
            "message": issue.get("message", ""),
            "file": file_path,
            "line": issue.get("line"),
            "snippet": "",
            "cwe": [t.upper() for t in issue.get("tags", []) if t.lower().startswith("cwe")],
            "help_uri": "",
            "type": issue.get("type", ""),
        })

    for hs in sonar_data.get("hotspots", []):
        # Hotspots are "security-sensitive code requiring manual review", not confirmed
        # vulnerabilities. They are mapped one notch down so they never dominate the gate.
        component = hs.get("component", "")
        file_path = component.split(":", 1)[1] if ":" in component else component
        prob = hs.get("vulnerabilityProbability", "LOW")
        findings.append({
            "source": "sonarqube-hotspot",
            "rule_id": hs.get("ruleKey", ""),
            "severity": {"HIGH": "medium", "MEDIUM": "low", "LOW": "info"}.get(prob, "info"),
            "message": hs.get("message", ""),
            "file": file_path,
            "line": hs.get("line"),
            "snippet": "",
            "cwe": [],
            "help_uri": "",
            "type": "SECURITY_HOTSPOT",
        })

    return findings


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

_CSS = """
:root{
  --bg:#101319; --panel:#171c25; --line:#242c38; --ink:#dde3ec; --dim:#7d8798;
  --critical:#ff5f56; --high:#ff9a3c; --medium:#e8c547; --low:#5aa9e6; --info:#6b7688;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:14px/1.55 ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;}
.wrap{max-width:1080px;margin:0 auto;padding:40px 20px 80px}
h1{font-size:26px;letter-spacing:-.02em;margin:0 0 4px;font-weight:600}
h1 span{color:var(--dim);font-weight:400}
h2{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);
  margin:40px 0 12px;font-weight:600}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);margin-top:24px}
.meta div{background:var(--panel);padding:11px 13px}
.meta dt{color:var(--dim);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.meta dd{margin:3px 0 0;word-break:break-all}
/* Severity spine: proportional stacked bar that doubles as the legend. */
.spine{display:flex;height:34px;border:1px solid var(--line);overflow:hidden;margin-bottom:10px}
.spine i{display:block}
.legend{display:flex;flex-wrap:wrap;gap:18px;color:var(--dim);font-size:12px}
.legend b{color:var(--ink)}
.dot{display:inline-block;width:9px;height:9px;margin-right:6px}
table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}
th{text-align:left;color:var(--dim);font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;padding:8px 10px;border-bottom:1px solid var(--line)}
td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}
tr:hover td{background:var(--panel)}
.sev{font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;
  white-space:nowrap;border-left:3px solid;padding-left:8px}
.rule{color:var(--dim);font-size:12px;word-break:break-all}
.loc{color:var(--low);font-size:12px;word-break:break-all}
pre{margin:6px 0 0;padding:8px 10px;background:#0b0e13;border:1px solid var(--line);
  overflow-x:auto;font-size:12px;color:#aab4c4;white-space:pre-wrap}
.empty{padding:34px;border:1px dashed var(--line);color:var(--dim);text-align:center}
footer{margin-top:56px;color:var(--dim);font-size:12px;border-top:1px solid var(--line);padding-top:16px}
"""


def _render_html(findings: list, counts: Counter, meta: dict) -> str:
    """Build a fully self-contained HTML report (no external CSS/JS/fonts).

    Self-contained matters: the artifact is read from an S3 presigned URL or an email
    attachment, often on a network that cannot reach a CDN.
    """
    total = sum(counts.values()) or 1
    colors = {s: f"var(--{s})" for s in SEVERITIES}

    # Proportional severity bar. Segments with zero findings are simply omitted.
    spine = "".join(
        f'<i style="width:{counts[s]/total*100:.2f}%;background:{colors[s]}" '
        f'title="{s}: {counts[s]}"></i>'
        for s in SEVERITIES if counts[s]
    ) or '<i style="width:100%;background:var(--line)"></i>'

    legend = "".join(
        f'<span><span class="dot" style="background:{colors[s]}"></span>'
        f'{s} <b>{counts[s]}</b></span>'
        for s in SEVERITIES
    )

    meta_html = "".join(
        f"<div><dt>{html.escape(k.replace('_',' '))}</dt>"
        f"<dd>{html.escape(str(v))}</dd></div>"
        for k, v in meta.items() if v is not None
    )

    if findings:
        rows = []
        for f in findings:
            loc = html.escape(f["file"] or "-")
            if f.get("line"):
                loc += f':{f["line"]}'
            snippet = (f'<pre>{html.escape(f["snippet"][:400])}</pre>'
                       if f.get("snippet") else "")
            cwe = (" · " + ", ".join(html.escape(c) for c in f["cwe"])) if f.get("cwe") else ""
            rows.append(f"""<tr>
  <td class="sev" style="border-color:{colors[f['severity']]};color:{colors[f['severity']]}">{f['severity']}</td>
  <td>{html.escape(f['message'])}{snippet}
      <div class="rule">{html.escape(f['rule_id'])}{cwe} · {html.escape(f['source'])}</div></td>
  <td class="loc">{loc}</td>
</tr>""")
        body = ("<table><tr><th>Severity</th><th>Finding</th><th>Location</th></tr>"
                + "".join(rows) + "</table>")
    else:
        body = '<div class="empty">No findings returned by the configured rulesets.</div>'

    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SAST Report · {html.escape(meta.get('project',''))}</title><style>{_CSS}</style>
</head><body><div class="wrap">
<h1>SAST Report <span>/ {html.escape(meta.get('project',''))}</span></h1>
<dl class="meta">{meta_html}</dl>
<h2>Severity distribution</h2>
<div class="spine">{spine}</div>
<div class="legend">{legend}</div>
<h2>Findings ({sum(counts.values())})</h2>
{body}
<footer>Generated by sast-batch-runner · Semgrep OSS + SonarQube Community Build</footer>
</div></body></html>"""


def _render_markdown(findings: list, counts: Counter, meta: dict) -> str:
    """Markdown variant — this is the one you paste into a PR comment or a Jira ticket."""
    lines = [f"# SAST Report — {meta.get('project')}", ""]
    for k, v in meta.items():
        if v is not None:
            lines.append(f"- **{k.replace('_',' ')}**: `{v}`")
    lines += ["", "## Severity summary", "",
              "| Severity | Count |", "|---|---:|"]
    lines += [f"| {s} | {counts[s]} |" for s in SEVERITIES]
    lines += ["", f"**Total: {sum(counts.values())}**", "", "## Findings", ""]
    if not findings:
        lines.append("_No findings._")
    else:
        lines += ["| Sev | Rule | Location | Message |", "|---|---|---|---|"]
        for f in findings[:500]:  # cap: a 5000-row markdown table helps nobody
            loc = f'{f["file"]}:{f["line"]}' if f.get("line") else f["file"]
            msg = f["message"].replace("|", "\\|")[:160]
            lines.append(f'| {f["severity"]} | `{f["rule_id"]}` | `{loc}` | {msg} |')
    return "\n".join(lines)


def build_reports(sarif_path: Path, sonar_data: dict, meta: dict, outdir: Path) -> list:
    """Entry point called by scan_runner. Returns the list of artifact paths written."""
    findings = parse_sarif(sarif_path) + parse_sonar(sonar_data)

    # Deterministic ordering: severity descending, then file, then line. Deterministic
    # output means two runs on the same commit diff cleanly — required for a
    # "new findings only" gate later.
    findings.sort(key=lambda f: (SEVERITIES.index(f["severity"]),
                                 f["file"] or "", f["line"] or 0))

    counts = Counter({s: 0 for s in SEVERITIES})
    counts.update(f["severity"] for f in findings)

    by_source = Counter(f["source"] for f in findings)
    top_rules = Counter(f["rule_id"] for f in findings).most_common(10)

    summary = {
        **meta,
        "total": len(findings),
        "severity_counts": dict(counts),
        "findings_by_source": dict(by_source),
        "top_rules": [{"rule": r, "count": c} for r, c in top_rules],
    }

    outdir = Path(outdir)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))
    (outdir / "findings.json").write_text(json.dumps(findings, indent=2))
    (outdir / "report.md").write_text(_render_markdown(findings, counts, meta))
    (outdir / "report.html").write_text(_render_html(findings, counts, meta))

    return [outdir / "report.html", outdir / "report.md",
            outdir / "summary.json", outdir / "findings.json",
            Path(sarif_path)]
