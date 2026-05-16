#!/usr/bin/env bash
# Copy code.py, settings.toml, and lib/ to CIRCUITPY
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CIRCUITPY="/Volumes/CIRCUITPY"

if [[ ! -d "$CIRCUITPY" ]]; then
  echo "CIRCUITPY not found. Is the board plugged in and running CircuitPython?"
  echo "If still on factory firmware, run ./scripts/flash-circuitpython.sh first."
  exit 1
fi

if [[ ! -d "$ROOT/firmware/lib" ]]; then
  echo "Missing firmware/lib — run ./scripts/bootstrap.sh first"
  exit 1
fi

echo "==> Deploying to $CIRCUITPY ..."

for py in "$ROOT/firmware"/*.py; do
  base="$(basename "$py")"
  # App entry lives in code_app.py until deploy-app.sh is used
  [[ "$base" == "code_app.py" ]] && continue
  cp "$py" "$CIRCUITPY/$base"
done

if [[ -f "$ROOT/firmware/settings.toml" ]]; then
  cp "$ROOT/firmware/settings.toml" "$CIRCUITPY/settings.toml"
fi

rm -rf "$CIRCUITPY/lib"
mkdir -p "$CIRCUITPY/lib"
cp -R "$ROOT/firmware/lib/"* "$CIRCUITPY/lib/"

sync
echo "Deploy complete. Board should reboot and show the test message."
echo "If display is still garbled, see SETUP.md troubleshooting."
