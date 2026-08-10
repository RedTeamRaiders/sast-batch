#!/usr/bin/env bash
# 03_submit_job.sh — submit one scan and tail it to completion.
set -Eeuo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
JOB_QUEUE="${JOB_QUEUE:-sast-queue}"
JOB_DEF="${JOB_DEF:-sast-semgrep-only}"
REPO_URL="${1:?usage: ./03_submit_job.sh <repo-url> [branch]}"
BRANCH="${2:-}"

# Job names must match ^[a-zA-Z0-9_-]{1,128}$ — a raw repo URL will be REJECTED.
# tr squeezes every disallowed character into a hyphen.
SAFE_NAME="scan-$(echo "${REPO_URL}" | tr -cs 'a-zA-Z0-9' '-' | tail -c 60)-$(date +%s)"

# --container-overrides injects per-run values on top of the job definition defaults.
# This is what lets ONE job definition serve every repository in the portfolio.
JOB_ID="$(aws batch submit-job \
  --job-name "${SAFE_NAME}" \
  --job-queue "${JOB_QUEUE}" \
  --job-definition "${JOB_DEF}" \
  --region "${AWS_REGION}" \
  --container-overrides "environment=[{name=REPO_URL,value=${REPO_URL}},{name=REPO_BRANCH,value=${BRANCH}}]" \
  --query jobId --output text)"

echo "==> submitted jobId=${JOB_ID}"

# Poll the job state machine: SUBMITTED -> PENDING -> RUNNABLE -> STARTING -> RUNNING -> SUCCEEDED/FAILED
# A job stuck in RUNNABLE almost always means: no route to ECR (no NAT / no VPC endpoint),
# or maxvCpus already saturated by other jobs.
while true; do
  read -r STATUS REASON <<<"$(aws batch describe-jobs --jobs "${JOB_ID}" --region "${AWS_REGION}" \
      --query 'jobs[0].[status,statusReason]' --output text)"
  echo "    ${STATUS} ${REASON}"
  case "${STATUS}" in
    SUCCEEDED) echo "==> SUCCEEDED"; break ;;
    FAILED)    echo "==> FAILED: ${REASON}"; break ;;
  esac
  sleep 10
done

# Resolve the CloudWatch log stream for this exact attempt and dump it.
STREAM="$(aws batch describe-jobs --jobs "${JOB_ID}" --region "${AWS_REGION}" \
  --query 'jobs[0].container.logStreamName' --output text)"
[ "${STREAM}" != "None" ] && aws logs tail /aws/batch/sast --log-stream-names "${STREAM}" \
  --region "${AWS_REGION}" --since 1h
