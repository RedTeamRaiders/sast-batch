# syntax=docker/dockerfile:1.7
# ^ Enables BuildKit frontend features (heredocs, --mount cache). Harmless if BuildKit is off.

# ---------- STAGE 1: fetch the SonarScanner CLI ----------
# Separate stage so the ~50MB zip + unzip tooling never lands in the final image layer set.
FROM debian:bookworm-slim AS scanner-fetch

# SONAR_SCANNER_VERSION is an ARG (build-time only, not present at runtime).
# Pin it. "latest" in a security tool image is how you get non-reproducible scans.
ARG SONAR_SCANNER_VERSION=6.2.1.4610

# Install only what is needed to download + verify + unpack, then delete the apt lists
# in the SAME RUN layer (a separate RUN would leave the lists in the previous layer).
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl unzip ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# The "-linux-x64" variant bundles its own JRE 17, so the final image needs NO system Java.
# That drops ~180MB and removes a whole CVE surface you'd otherwise have to patch.
RUN curl -fsSL -o /tmp/scanner.zip \
      "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux-x64.zip" \
 && unzip -q /tmp/scanner.zip -d /opt \
 && mv "/opt/sonar-scanner-${SONAR_SCANNER_VERSION}-linux-x64" /opt/sonar-scanner \
 && rm /tmp/scanner.zip

# ---------- STAGE 2: the runtime image ----------
FROM python:3.12-slim-bookworm AS runtime

# OCI labels — these show up in `docker inspect` and in ECR. Useful for provenance in an audit.
LABEL org.opencontainers.image.title="sast-batch-runner" \
      org.opencontainers.image.description="Semgrep + SonarQube CE SAST batch job for AWS Batch/Fargate"

# PYTHONUNBUFFERED=1  -> stdout/stderr are not block-buffered, so logs stream to CloudWatch
#                        in real time instead of appearing all at once when the job exits.
# PYTHONDONTWRITEBYTECODE=1 -> no .pyc files; keeps the container filesystem read-only-friendly.
# PIP_NO_CACHE_DIR=1  -> pip does not keep the wheel cache, saving ~150MB in the layer.
# SEMGREP_SEND_METRICS=off -> no telemetry egress. Matters when the job runs in a private subnet
#                        with a locked-down egress policy; otherwise semgrep retries and stalls.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    SEMGREP_SEND_METRICS=off \
    PATH="/opt/sonar-scanner/bin:${PATH}"

# git   -> to clone the target repo
# ca-certificates -> TLS trust store for HTTPS clone + AWS API + Sonar API
# tini  -> PID 1 init that reaps zombies and forwards SIGTERM. Without it, an ECS/Batch
#          task stop leaves orphaned scanner processes and the task lingers until SIGKILL.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates tini \
 && rm -rf /var/lib/apt/lists/*

# Copy the pre-unpacked scanner from stage 1. --from=scanner-fetch means "from that stage".
COPY --from=scanner-fetch /opt/sonar-scanner /opt/sonar-scanner

# Install Python deps in their own layer BEFORE copying source, so editing scan_runner.py
# does not invalidate the pip layer on rebuild. Standard Docker layer-cache ordering.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Now the application code — the layer that changes most often, so it goes last.
COPY batch_script.py report_builder.py entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Create an unprivileged user. Fargate does not give you root escape protection for free;
# running the scanner as UID 10001 means a malicious repo's build hooks can't touch /opt.
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin scanner \
 && mkdir -p /workspace /out \
 && chown -R scanner:scanner /workspace /out /app

# /workspace = cloned source, /out = generated artifacts. Both under the ephemeral task volume.
WORKDIR /app
USER scanner

# tini as ENTRYPOINT (-g forwards signals to the whole process group, not just PID 1).
ENTRYPOINT ["/usr/bin/tini", "-g", "--", "/app/entrypoint.sh"]

# Default CMD is empty: all configuration comes from environment variables set by the
# AWS Batch job definition / job submission overrides. Keeps one image for every repo.
CMD []
