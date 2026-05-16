#!/usr/bin/env bash
# Deploy full app (display_board + text) after verify mode passes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CIRCUITPY="/Volumes/CIRCUITPY"

if [[ ! -d "$CIRCUITPY" ]]; then
  echo "CIRCUITPY not found."
  exit 1
fi

cp "$ROOT/firmware/code_app.py" "$CIRCUITPY/code.py"
"$ROOT/scripts/deploy.sh" 2>/dev/null || true

# deploy.sh copies all .py including code.py — do in correct order
cp "$ROOT/firmware/code_app.py" "$CIRCUITPY/code.py"
sync
echo "App firmware deployed (test_pattern). Edit code_app.py ACTIVE_SCENE as needed."
