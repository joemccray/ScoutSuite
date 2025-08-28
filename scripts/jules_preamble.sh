#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
mkdir -p docs scripts .github/workflows
python3 scripts/restore_docs.py --write both 2>/dev/null || python scripts/restore_docs.py --write both
python3 scripts/verify_manifest.py --check || python scripts/verify_manifest.py --check
echo "[jules] preflight OK"
