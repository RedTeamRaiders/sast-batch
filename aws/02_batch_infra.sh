#!/usr/bin/env bash
# 02_batch_infra.sh — stand up IAM roles, a Fargate compute environment, and a job queue.
# Run once. Everything is idempotent (`|| true` on creates that fail when already present).
set -Eeuo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
S3_BUCKET="${S3_BUCKET:?export S3_BUCKET=your-sast-reports-bucket}"
SUBNETS="${SUBNETS:?export SUBNETS=subnet-aaa,subnet-bbb}"          # PRIVATE subnets w/ NAT preferred
SECURITY_GROUPS="${SECURITY_GROUPS:?export SECURITY_GROUPS=sg-xxx}" # egress 443 only is sufficient
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"

# ======================================================================================
# 1. EXECUTION ROLE — used by the ECS agent, NOT by your code.
#    It pulls the image from ECR and writes the log stream. Fargate REQUIRES it.
# ======================================================================================
cat > /tmp/ecs-trust.json <<'JSON'
{"Version":"2012-10-17","Statement":[{
  "Effect":"Allow",
  "Principal":{"Service":"ecs-tasks.amazonaws.com"},
  "Action":"sts:AssumeRole"}]}
JSON
# ^ The trust policy names ecs-tasks.amazonaws.com because AWS Batch on Fargate runs your
#   job as an ECS task. Getting this principal wrong is the most common setup failure.

aws iam create-role --role-name sastBatchExecutionRole \
  --assume-role-policy-document file:///tmp/ecs-trust.json >/dev/null 2>&1 || true

aws iam attach-role-policy --role-name sastBatchExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy || true

# ======================================================================================
# 2. JOB ROLE — the credentials YOUR container code receives. Least privilege lives here.
#    Scoped to one bucket prefix and one secret. Never attach S3FullAccess.
# ======================================================================================
aws iam create-role --role-name sastBatchJobRole \
  --assume-role-policy-document file:///tmp/ecs-trust.json >/dev/null 2>&1 || true

cat > /tmp/job-policy.json <<JSON
{"Version":"2012-10-17","Statement":[
 {"Sid":"WriteReportsOnly",
  "Effect":"Allow",
  "Action":["s3:PutObject","s3:PutObjectAcl"],
  "Resource":"arn:aws:s3:::${S3_BUCKET}/sast-reports/*"},
 {"Sid":"ReadGitTokenOnly",
  "Effect":"Allow",
  "Action":["secretsmanager:GetSecretValue"],
  "Resource":"arn:aws:secretsmanager:${AWS_REGION}:${ACCOUNT_ID}:secret:sast/git-token-*"}]}
JSON
# Note: PutObject only — no GetObject, no ListBucket, no DeleteObject. A compromised
# scanner container (think: malicious repo with a build hook) can write reports and
# nothing else. It cannot read other teams' findings or destroy evidence.

aws iam put-role-policy --role-name sastBatchJobRole \
  --policy-name sastBatchJobInline --policy-document file:///tmp/job-policy.json

# ======================================================================================
# 3. COMPUTE ENVIRONMENT — MANAGED + FARGATE means AWS provisions capacity per job.
#    No EC2 instances, no ASG, no AMI patching, zero cost when idle.
# ======================================================================================
aws batch create-compute-environment \
  --compute-environment-name sast-fargate-ce \
  --type MANAGED \
  --state ENABLED \
  --region "${AWS_REGION}" \
  --compute-resources "type=FARGATE,maxvCpus=32,subnets=${SUBNETS},securityGroupIds=${SECURITY_GROUPS}" \
  >/dev/null 2>&1 || echo "compute environment already exists"
#   maxvCpus=32 is the concurrency ceiling: with a 4-vCPU job definition that is 8 repos
#   scanned in parallel. Raise it and Batch fans out further; it is your cost blast radius.
#   Use FARGATE_SPOT instead of FARGATE for ~70% savings — but Spot reclaims mid-scan, so
#   only do that once retryStrategy is proven.

echo "==> waiting for compute environment to become VALID"
# A job queue attached to an INVALID/CREATING compute environment silently accepts jobs
# that then sit in RUNNABLE forever. Wait for VALID before creating the queue.
for i in $(seq 1 30); do
  STATUS="$(aws batch describe-compute-environments \
    --compute-environments sast-fargate-ce --region "${AWS_REGION}" \
    --query 'computeEnvironments[0].status' --output text)"
  echo "    status=${STATUS}"
  [ "${STATUS}" = "VALID" ] && break
  sleep 10
done

# ======================================================================================
# 4. JOB QUEUE — jobs are submitted here, then dispatched to the compute environment.
# ======================================================================================
aws batch create-job-queue \
  --job-queue-name sast-queue \
  --state ENABLED \
  --priority 1 \
  --region "${AWS_REGION}" \
  --compute-environment-order "order=1,computeEnvironment=sast-fargate-ce" \
  >/dev/null 2>&1 || echo "job queue already exists"
#   priority matters only when several queues share one compute environment; higher
#   number wins. Add a second queue at priority 10 later for on-demand PR scans that
#   must jump ahead of the nightly full-portfolio sweep.

echo "==> Done."
echo "    executionRoleArn = arn:aws:iam::${ACCOUNT_ID}:role/sastBatchExecutionRole"
echo "    jobRoleArn       = arn:aws:iam::${ACCOUNT_ID}:role/sastBatchJobRole"
