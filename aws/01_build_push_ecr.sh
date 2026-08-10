#!/usr/bin/env bash
# 01_build_push_ecr.sh — build the scanner image and push it to Amazon ECR.
set -Eeuo pipefail

# ----- inputs (override by exporting before you run) -----
AWS_REGION="${AWS_REGION:-us-east-1}"
REPO_NAME="${REPO_NAME:-sast-batch-runner}"
IMAGE_TAG="${IMAGE_TAG:-$(git rev-parse --short HEAD 2>/dev/null || date +%Y%m%d%H%M)}"
#           ^ tag with the commit SHA, never `latest`. A Batch job definition pinned to
#             `:latest` is unauditable — you cannot prove which scanner produced a report.

# Resolve the account ID from the caller's credentials instead of hardcoding it.
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}"

echo "==> Target: ${ECR_URI}:${IMAGE_TAG}"

# ----- 1. create the ECR repository (idempotent) -----
# `describe-repositories` succeeds if it exists; the || short-circuits to create.
aws ecr describe-repositories --repository-names "${REPO_NAME}" --region "${AWS_REGION}" >/dev/null 2>&1 \
  || aws ecr create-repository \
       --repository-name "${REPO_NAME}" \
       --region "${AWS_REGION}" \
       --image-scanning-configuration scanOnPush=true \
       --image-tag-mutability IMMUTABLE \
       --encryption-configuration encryptionType=AES256 >/dev/null
#      scanOnPush=true   -> ECR runs its own CVE scan on the scanner image. Yes, you scan
#                           the scanner. An auditor will ask.
#      IMMUTABLE         -> a tag can never be repointed at different bytes. This is what
#                           makes "job X ran image sha256:abc" a defensible statement.

# ----- 2. authenticate the local Docker daemon to ECR -----
# get-login-password emits a 12-hour token on stdout; piping into `--password-stdin`
# keeps it out of the process list and out of ~/.bash_history.
aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# ----- 3. build -----
# --platform linux/amd64 is MANDATORY when you build on an Apple Silicon Mac. Without it
# you push an arm64 image, and Fargate's X86_64 runtime platform fails at task start with
# "image Manifest does not contain descriptor matching platform" — a 20-minute head-scratch.
# --provenance=false avoids pushing an OCI attestation manifest that older ECS agents choke on.
docker build \
  --platform linux/amd64 \
  --provenance=false \
  -t "${REPO_NAME}:${IMAGE_TAG}" \
  ..

# ----- 4. tag and push -----
docker tag "${REPO_NAME}:${IMAGE_TAG}" "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:${IMAGE_TAG}"

# Print the immutable digest — this is the value you cite in the demo and pin in the job def.
DIGEST="$(aws ecr describe-images --repository-name "${REPO_NAME}" \
  --image-ids imageTag="${IMAGE_TAG}" --region "${AWS_REGION}" \
  --query 'imageDetails[0].imageDigest' --output text)"

echo "==> Pushed ${ECR_URI}:${IMAGE_TAG}"
echo "==> Digest ${DIGEST}"
echo "export IMAGE_URI=${ECR_URI}:${IMAGE_TAG}"
