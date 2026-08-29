#!/bin/bash
set -Eeuo pipefail
: "${REPO_URL:?REPO_URL is required}"
: "${S3_BUCKET:?S3_BUCKET is required}"

JOB_ID="${AWS_BATCH_JOB_ID:-local-$(date +%s)}"
SLUG="${REPO_SLUG:-iam-scan}"
mkdir -p /out

echo "[$(date +%H:%M:%S)] Cloning ${REPO_URL}"
git clone --depth 1 ${REPO_BRANCH:+--branch "$REPO_BRANCH"} "${REPO_URL}" /workspace/src

echo "[$(date +%H:%M:%S)] Scanning JSON files for IAM policy documents"
> /out/raw_findings.jsonl
for f in $(find /workspace/src -maxdepth 2 -name "*.json"); do
  result=$(python3 /app/scan_iam_policy.py "$f")
  is_valid=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin)['valid'])")
  if [ "$is_valid" = "True" ]; then
    findings=$(echo "$result" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['findings']))")
    echo "{\"file\": \"${f#/workspace/src/}\", \"findings\": ${findings}}" >> /out/raw_findings.jsonl
    echo "  scanned: $f"
  else
    echo "  skip: $f (not a valid IAM policy document)"
  fi
done

python3 /app/summarize_findings.py /out/raw_findings.jsonl /out/iam-summary.json /out/iam-findings.json

TOTAL=$(python3 -c "import json; print(json.load(open('/out/iam-summary.json'))['total'])")
echo "[$(date +%H:%M:%S)] IAM scan complete: ${TOTAL} finding(s) across all policy files"

PREFIX="iam-reports/${SLUG}/${JOB_ID}"
for f in /out/iam-summary.json /out/iam-findings.json; do
  aws s3 cp "$f" "s3://${S3_BUCKET}/${PREFIX}/$(basename "$f")"
done
echo "[$(date +%H:%M:%S)] Uploaded reports to s3://${S3_BUCKET}/${PREFIX}/"

if [ "$TOTAL" -gt 0 ]; then
  exit 1
fi
