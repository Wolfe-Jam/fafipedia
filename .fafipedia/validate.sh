#!/usr/bin/env bash
# FAFipedia validation orchestrator.
# Runs the linter against every .fafi at repo root (typed-entries + substrate-bundle).
set -euo pipefail

cd "$(dirname "$0")/.."

failed=0
for f in *.fafi; do
  [ -f "$f" ] || continue
  python3 .fafipedia/linter.py "$f" || failed=1
done

if [ "$failed" -ne 0 ]; then
  echo "FAFipedia validation: FAILED"
  exit 1
fi
echo "FAFipedia validation: OK"
