#!/bin/bash
set -Eeuo pipefail
: "${REPO_URL:?REPO_URL is required}"
: "${S3_BUCKET:?S3_BUCKET is required}"
: "${NVD_API_KEY:?NVD_API_KEY is required ? see https://nvd.nist.gov/developers/request-an-api-key}"

JOB_ID="${AWS_BATCH_JOB_ID:-local-$(date +%s)}"
SLUG="${REPO_SLUG:-dependency-scan}"

echo "[$(date +%H:%M:%S)] Cloning ${REPO_URL}"
git clone --depth 1 "${REPO_URL}" /workspace/src

echo "[$(date +%H:%M:%S)] Running Dependency-Check (this syncs the NVD database ? can take several minutes)"
mkdir -p /out
dependency-check.sh --scan /workspace/src --format ALL --project "${SLUG}" \
  --out /out --enableExperimental --nvdApiKey "${NVD_API_KEY}" --disableOssIndex \
  || SCAN_EXIT=$?
SCAN_EXIT="${SCAN_EXIT:-0}"
echo "[$(date +%H:%M:%S)] Dependency-Check finished, exit code ${SCAN_EXIT}"

shopt -s nullglob
PREFIX="dependency-reports/${SLUG}/${JOB_ID}"
for f in /out/*; do
  aws s3 cp "$f" "s3://${S3_BUCKET}/${PREFIX}/$(basename "$f")"
done
if [ -z "$(ls -A /out 2>/dev/null)" ]; then
  echo "[$(date +%H:%M:%S)] No report files were produced (scan likely failed before writing output)"
fi
echo "[$(date +%H:%M:%S)] Uploaded reports to s3://${S3_BUCKET}/${PREFIX}/"

exit "$SCAN_EXIT"
