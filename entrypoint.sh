#!/usr/bin/env bash
# entrypoint.sh — thin shell wrapper in front of the Python orchestrator.

# -E : ERR trap is inherited by functions and subshells
# -e : exit immediately on any non-zero command
# -u : treat an unset variable as an error (catches typo'd env var names)
# -o pipefail : a pipeline fails if ANY stage fails, not just the last one.
#               Without this, `sonar-scanner | tee log` would mask a scanner failure.
set -Eeuo pipefail

# Print a banner with the values that determine what this run actually scanned.
# ${VAR:-default} expands to `default` when VAR is unset — required under `set -u`.
echo "=================================================="
echo " SAST batch runner"
echo " job id : ${AWS_BATCH_JOB_ID:-local}"
echo " repo   : ${REPO_URL:-<unset>}"
echo " branch : ${REPO_BRANCH:-<default>}"
echo " sonar  : ${SONAR_HOST_URL:-disabled}"
echo "=================================================="

# `exec` REPLACES the shell process with Python rather than forking it.
# This makes Python PID 1's direct child, so SIGTERM from ECS/Batch on task stop
# reaches the scanner instead of dying in a shell that ignores it.
exec python3 /app/scan_runner.py "$@"
