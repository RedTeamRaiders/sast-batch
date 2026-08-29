"""summarize_findings.py — folds Parliament's per-file JSON output into one
combined summary, same severity-table spirit as the SAST report."""
import json
import sys

raw_path, summary_path, findings_path = sys.argv[1], sys.argv[2], sys.argv[3]

all_findings = []
with open(raw_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        for finding in entry["findings"]:
            all_findings.append({
                "file": entry["file"],
                "issue": finding.get("issue", ""),
                "detail": finding.get("detail", ""),
                "severity": finding.get("severity", "UNKNOWN"),
                "location": finding.get("location", {}),
            })

severity_counts = {}
for f in all_findings:
    severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

with open(findings_path, "w") as f:
    json.dump(all_findings, f, indent=2)

with open(summary_path, "w") as f:
    json.dump({"total": len(all_findings), "severity_counts": severity_counts}, f, indent=2)

print(f"Wrote {len(all_findings)} findings to {findings_path}")
