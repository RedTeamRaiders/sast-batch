# RUNBOOK — zero to SAST report

Ten phases, ~2h 15m of wall time, ~$0.30 of AWS spend for a full demo cycle.
Each phase ends with a **CHECKPOINT** — do not proceed past a failed checkpoint.

| Phase | What | Time |
|---|---|---|
| 0 | Create the AWS account | 20 m |
| 1 | Harden root, create an admin identity, set billing guardrails | 25 m |
| 2 | Local toolchain | 15 m |
| 3 | **Local validation — before any AWS spend** | 20 m |
| 4 | AWS prerequisites (S3, log group, network discovery) | 15 m |
| 5 | Build + push to ECR | 15 m |
| 6 | Batch infrastructure (IAM, compute environment, queue) | 10 m |
| 7 | Register job definitions | 5 m |
| 8 | Submit and observe | 10 m |
| 9 | Retrieve the report | 5 m |
| 10 | Teardown | 5 m |

---

## PHASE 0 — Create the AWS account

1. Go to `https://portal.aws.amazon.com/billing/signup`.
2. Root email: use a **distribution list or alias you control long-term** (e.g. `aws-root+sast@yourdomain.com`), never a personal address tied to one employee. Root email cannot be changed without support involvement.
3. Account name: `sast-demo` — it appears in the console header and in every screenshot you take.
4. Provide a credit card. Required even on the Free Plan.
5. Phone/SMS verification.
6. **Plan selection — choose Paid Plan.**

### Why Paid Plan, not Free Plan

AWS replaced the old 12-month model on 2025-07-15. New accounts now pick a plan at signup, get $100 credits immediately, and can earn up to $100 more by completing onboarding activities. The Free Plan is capped at 6 months or credit exhaustion — and critically, it **restricts access to some services** and **closes the account** when credits run out.

For a demo you are presenting to stakeholders, a plan that can block a service or terminate the account mid-cycle is unacceptable risk for a $0.30 workload. Take the Paid Plan, keep the $100 credits (they apply either way), and control spend with a budget alarm in Phase 1.

7. Support plan: **Basic (free)**.

**CHECKPOINT 0** — you can log into the console as root and see the billing dashboard.

---

## PHASE 1 — Harden root, create admin identity, set guardrails

### 1.1 Lock the root user (do this immediately, not later)

```
Console -> top-right account menu -> Security credentials
```

- Enable **MFA** on root. Hardware key or authenticator app. Root MFA is the single control that separates "a demo account" from "a lateral movement target."
- **Do not create root access keys.** If any exist, delete them.
- After this phase, do not use root again except for billing changes and account closure.

### 1.2 Create your working identity

Two options, ranked:

**Option A — IAM Identity Center (recommended).** Short-lived credentials, no long-lived secrets on your laptop.

```
Console -> IAM Identity Center -> Enable
  -> Users -> Add user (yourself)
  -> Permission sets -> Create -> AdministratorAccess
  -> AWS accounts -> assign your user + the permission set
```

Then locally:

```bash
aws configure sso
# SSO start URL:  https://d-xxxxxxxxxx.awsapps.com/start
# SSO region:     us-east-1
# profile name:   sast
export AWS_PROFILE=sast
aws sso login
```

**Option B — IAM user with access keys (faster, weaker).** Acceptable only if the account is disposable and you delete the keys after the demo.

```bash
aws iam create-user --user-name sast-admin
aws iam attach-user-policy --user-name sast-admin \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam create-access-key --user-name sast-admin   # capture output ONCE
aws configure --profile sast
```

> `AdministratorAccess` is deliberate here — you are creating IAM roles, a compute environment, and ECR repos. Scope it down after the demo; the *job* role in `02_batch_infra.sh` is already least-privilege, which is the part that matters for the security story.

### 1.3 Billing guardrails

```bash
export AWS_PROFILE=sast
export AWS_REGION=us-east-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cat > /tmp/budget.json <<JSON
{
  "BudgetName": "sast-demo-monthly",
  "BudgetLimit": { "Amount": "20", "Unit": "USD" },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
JSON

cat > /tmp/notify.json <<JSON
[{
  "Notification": {
    "NotificationType": "ACTUAL",
    "ComparisonOperator": "GREATER_THAN",
    "Threshold": 50,
    "ThresholdType": "PERCENTAGE"
  },
  "Subscribers": [{ "SubscriptionType": "EMAIL", "Address": "you@example.com" }]
}]
JSON

aws budgets create-budget \
  --account-id "$ACCOUNT_ID" \
  --budget file:///tmp/budget.json \
  --notifications-with-subscribers file:///tmp/notify.json
```

Also enable **Cost Explorer** (`Billing -> Cost Explorer -> Enable`). It takes ~24h to populate, so turn it on now, not the day of the demo.

**CHECKPOINT 1**

```bash
aws sts get-caller-identity     # returns your Account, Arn, UserId
aws budgets describe-budgets --account-id "$ACCOUNT_ID"
```

---

## PHASE 2 — Local toolchain

```bash
# AWS CLI v2 (v1 lacks `aws sso login` and several batch options)
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o AWSCLIV2.pkg   # macOS
sudo installer -pkg AWSCLIV2.pkg -target /
aws --version        # expect aws-cli/2.x

# Docker Desktop (macOS/Windows) or docker-ce + buildx (Linux)
docker --version
docker buildx version

git --version
python3 --version    # 3.10+ only needed if you run the scanner outside a container
```

**Apple Silicon users:** confirm buildx can emit amd64. Fargate runs X86_64 by default and an arm64 image fails at task start with a manifest/platform mismatch.

```bash
docker buildx inspect --bootstrap | grep -i platforms
# must include linux/amd64
```

**CHECKPOINT 2** — `aws sts get-caller-identity` works and `docker run --rm hello-world` succeeds.

---

## PHASE 3 — Local validation (do this before spending a cent)

```bash
cd sast-batch
docker compose up --build --abort-on-container-exit scanner
```

Expected timeline in the logs:

| t+ | Event |
|---|---|
| 0:00 | banner, `Cloning https://github.com/juice-shop/juice-shop.git` |
| 0:20 | `Cloned at commit <sha>` |
| 0:25 | `SonarQube status=STARTING` (repeats) |
| 1:30–3:00 | `SonarQube server is UP` |
| 1:35 | `Minted ephemeral Sonar analysis token` |
| 1:40 | Semgrep rule download, then scan |
| 5:00 | `sonar-scanner` upload |
| 6:00 | `Sonar CE task status=SUCCESS` |
| 6:10 | `SonarQube returned N issues, M hotspots` |
| 6:15 | `Done in ###s — N findings` |

```bash
open ./out/report.html
cat ./out/summary.json | python3 -m json.tool | head -30
```

Semgrep-only smoke test (validates the path you will fall back to on stage):

```bash
docker compose run --rm -e SONAR_HOST_URL= scanner
```

**CHECKPOINT 3** — `report.html` renders with a non-zero finding count from **both** sources in `findings_by_source`. If SonarQube never reaches UP locally, it will not on Fargate either — fix it here, where iteration costs seconds.

Common local failure: the `admin/admin` token mint returns 401 because your pinned SonarQube tag forces a password change. Fix by adding `SONAR_FORCEAUTHENTICATION: "false"` to the sonarqube service env in `docker-compose.yml`, or pre-set the admin password.

---

## PHASE 4 — AWS prerequisites

```bash
export AWS_PROFILE=sast
export AWS_REGION=us-east-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export S3_BUCKET="sast-reports-${ACCOUNT_ID}"     # bucket names are globally unique
```

### 4.1 Reports bucket — private, encrypted, versioned

```bash
aws s3api create-bucket --bucket "$S3_BUCKET" --region "$AWS_REGION"
# NOTE: outside us-east-1 you must add:
#   --create-bucket-configuration LocationConstraint=$AWS_REGION

aws s3api put-public-access-block --bucket "$S3_BUCKET" \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

aws s3api put-bucket-encryption --bucket "$S3_BUCKET" \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

aws s3api put-bucket-versioning --bucket "$S3_BUCKET" \
  --versioning-configuration Status=Enabled
```

Versioning matters for the security story: scan reports are evidence, and an attacker with `PutObject` should not be able to silently overwrite a prior finding set.

### 4.2 CloudWatch log group

```bash
aws logs create-log-group --log-group-name /aws/batch/sast --region "$AWS_REGION"
aws logs put-retention-policy --log-group-name /aws/batch/sast --retention-in-days 30
```

**Batch will not create this for you.** Without it, jobs fail during `STARTING` with a log-driver error that looks nothing like the real cause.

### 4.3 Network discovery

```bash
VPC_ID=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true \
  --query 'Vpcs[0].VpcId' --output text)

export SUBNETS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID \
  --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text | tr '\t' ',')

export SECURITY_GROUPS=$(aws ec2 describe-security-groups \
  --filters Name=vpc-id,Values=$VPC_ID Name=group-name,Values=default \
  --query 'SecurityGroups[0].GroupId' --output text)

echo "VPC=$VPC_ID"; echo "SUBNETS=$SUBNETS"; echo "SG=$SECURITY_GROUPS"
```

**Public subnets on purpose.** The job definitions set `assignPublicIp: ENABLED`, which gives Fargate outbound reach to ECR, S3, Semgrep's rule registry, and GitHub with **no NAT gateway**. A NAT gateway is ~$32/month plus data processing — 100x the cost of the entire demo. No inbound ports are opened; the default SG permits egress only.

For a production deployment, move to private subnets with VPC endpoints for `ecr.api`, `ecr.dkr`, `s3` (gateway), `logs`, `secretsmanager`, plus NAT for the git host and Semgrep registry.

### 4.4 Private repo token (skip for a public-repo demo)

```bash
aws secretsmanager create-secret \
  --name sast/git-token-github \
  --secret-string '{"token":"ghp_REPLACE"}' \
  --region "$AWS_REGION"
```

The secret name must match the `sast/git-token-*` wildcard in the job role policy. Then set `GIT_TOKEN_SECRET_ARN` on the job instead of `GIT_TOKEN`.

**CHECKPOINT 4** — `aws s3 ls s3://$S3_BUCKET` succeeds, and `$SUBNETS` / `$SECURITY_GROUPS` are non-empty.

---

## PHASE 5 — Build and push to ECR

```bash
cd aws
./01_build_push_ecr.sh
```

The script creates an ECR repo with `scanOnPush=true` and `IMMUTABLE` tags, authenticates Docker, builds `--platform linux/amd64`, pushes, and prints the digest.

```bash
export IMAGE_TAG=<tag printed by the script>
```

**CHECKPOINT 5**

```bash
aws ecr describe-images --repository-name sast-batch-runner \
  --region "$AWS_REGION" --query 'imageDetails[0].[imageTags,imageSizeInBytes]'
```

Expect ~450–650 MB. Also check the ECR scan result on your own image — being able to say "and yes, I scanned the scanner" is worth thirty seconds of your demo.

---

## PHASE 6 — Batch infrastructure

```bash
./02_batch_infra.sh
```

Creates `sastBatchExecutionRole`, `sastBatchJobRole` (scoped to one bucket prefix and one secret), the `sast-fargate-ce` Fargate compute environment, and the `sast-queue` job queue. The script polls until the compute environment reaches `VALID` — attaching a queue to a `CREATING` environment produces jobs that sit in `RUNNABLE` forever with no error.

**CHECKPOINT 6**

```bash
aws batch describe-compute-environments --compute-environments sast-fargate-ce \
  --query 'computeEnvironments[0].[status,state]' --output text     # VALID ENABLED
aws batch describe-job-queues --job-queues sast-queue \
  --query 'jobQueues[0].[status,state]' --output text               # VALID ENABLED
```

---

## PHASE 7 — Register job definitions

Register **both**. The Semgrep-only definition is your stage fallback.

```bash
for JD in job-definition-semgrep job-definition-multicontainer; do
  sed -e "s/REPLACE_ACCOUNT/$ACCOUNT_ID/g" \
      -e "s/REPLACE_REGION/$AWS_REGION/g" \
      -e "s/REPLACE_BUCKET/$S3_BUCKET/g" \
      -e "s/REPLACE_TAG/$IMAGE_TAG/g" \
      "${JD}.json" > "/tmp/${JD}.rendered.json"
  aws batch register-job-definition \
    --cli-input-json "file:///tmp/${JD}.rendered.json" \
    --region "$AWS_REGION" --query 'jobDefinitionArn' --output text
done
```

```bash
grep -c REPLACE_ /tmp/job-definition-semgrep.rendered.json   # must be 0
```

An unrendered `REPLACE_ACCOUNT` produces a `CannotPullContainerError` at `STARTING`, several minutes after submit.

**CHECKPOINT 7** — `aws batch describe-job-definitions --status ACTIVE --query 'jobDefinitions[].[jobDefinitionName,revision]' --output table` lists both at revision 1.

---

## PHASE 8 — Submit and observe

Warm-up run first — never let the audience watch a cold start:

```bash
./03_submit_job.sh https://github.com/juice-shop/juice-shop.git master
```

The demo run:

```bash
JOB_DEF=sast-semgrep-sonarqube \
  ./03_submit_job.sh https://github.com/juice-shop/juice-shop.git master
```

State machine: `SUBMITTED -> PENDING -> RUNNABLE -> STARTING -> RUNNING -> SUCCEEDED`

| Stuck at | Almost always |
|---|---|
| `RUNNABLE` | No route to ECR, or `maxvCpus` saturated, or compute environment not `VALID` |
| `STARTING` then `FAILED` | Missing log group; unrendered `REPLACE_*`; arm64 image |
| `RUNNING` then exit 137 | OOMKilled — raise `MEMORY` or lower the Sonar JVM heaps |
| `RUNNING` then exit 1 | Working as designed if `FAIL_ON_SEVERITY` is set |

Live logs in a second terminal:

```bash
aws logs tail /aws/batch/sast --follow --region "$AWS_REGION"
```

**CHECKPOINT 8** — job status `SUCCEEDED`, and the log tail ends with `Done in ###s — N findings`.

---

## PHASE 9 — Retrieve the report

```bash
aws s3 ls "s3://$S3_BUCKET/sast-reports/" --recursive

aws s3 cp "s3://$S3_BUCKET/sast-reports/juice-shop-juice-shop/<jobId>/" ./reports/ --recursive
open ./reports/report.html
```

For a shareable link during the presentation (15-minute expiry, no bucket policy change):

```bash
aws s3 presign "s3://$S3_BUCKET/sast-reports/juice-shop-juice-shop/<jobId>/report.html" \
  --expires-in 900
```

Then show the gate:

```bash
aws batch submit-job --job-name sast-gate-demo --job-queue sast-queue \
  --job-definition sast-semgrep-only --region "$AWS_REGION" \
  --container-overrides 'environment=[
    {name=REPO_URL,value=https://github.com/juice-shop/juice-shop.git},
    {name=REPO_BRANCH,value=master},
    {name=FAIL_ON_SEVERITY,value=high}]'
```

Same artifact, job now `FAILED` with exit 1 — that is the CI gate, and it is the beat that lands with engineering leadership.

**CHECKPOINT 9** — `report.html` opens from S3 and shows findings from both engines.

---

## PHASE 10 — Teardown

Run this the day after the demo. Order matters — the queue must be disabled before the compute environment.

```bash
aws batch update-job-queue --job-queue sast-queue --state DISABLED
sleep 30
aws batch delete-job-queue --job-queue sast-queue
sleep 60
aws batch update-compute-environment --compute-environment sast-fargate-ce --state DISABLED
sleep 30
aws batch delete-compute-environment --compute-environment sast-fargate-ce

aws ecr delete-repository --repository-name sast-batch-runner --force
aws s3 rm "s3://$S3_BUCKET" --recursive && aws s3api delete-bucket --bucket "$S3_BUCKET"
aws logs delete-log-group --log-group-name /aws/batch/sast

aws iam delete-role-policy --role-name sastBatchJobRole --policy-name sastBatchJobInline
aws iam delete-role --role-name sastBatchJobRole
aws iam detach-role-policy --role-name sastBatchExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam delete-role --role-name sastBatchExecutionRole

# If you used Option B in Phase 1, delete the access key now.
aws iam list-access-keys --user-name sast-admin
```

---

## Cost model (us-east-1)

| Item | Rate | Demo usage | Cost |
|---|---|---:|---:|
| Fargate vCPU | $0.04048 / vCPU-hr | 4 vCPU × 10 min | $0.027 |
| Fargate memory | $0.004445 / GB-hr | 16 GB × 10 min | $0.012 |
| ECR storage | $0.10 / GB-mo | 0.6 GB × 1 mo | $0.060 |
| S3 storage + requests | — | a few MB | ~$0.001 |
| CloudWatch Logs | $0.50 / GB ingest | ~5 MB | ~$0.003 |
| Data transfer out | $0.09 / GB after 100 GB free | negligible | $0.000 |
| **Per full demo cycle** | | | **≈ $0.10** |
| NAT gateway **if** you use private subnets | $0.045 / hr | 720 hr | **$32.40 / mo** |

The NAT gateway is the only line item that can hurt you. The delivered configuration avoids it.

Ceiling check: `maxvCpus=32` with a 4-vCPU job definition caps you at 8 concurrent scans ≈ $1.86/hr if you somehow saturated it continuously. The $20 budget alarm from Phase 1 fires long before that matters.
