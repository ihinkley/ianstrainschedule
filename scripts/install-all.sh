#!/usr/bin/env bash
# Download deps, flash CircuitPython if bootloader is open, then deploy
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

"$ROOT/scripts/bootstrap.sh"

if [[ -d /Volumes/MATRXS3BOOT ]]; then
  "$ROOT/scripts/flash-circuitpython.sh"
  echo "Waiting for CIRCUITPY (up to 30s)..."
  for _ in $(seq 1 30); do
    [[ -d /Volumes/CIRCUITPY ]] && break
    sleep 1
  done
fi

if [[ -d /Volumes/CIRCUITPY ]]; then
  "$ROOT/scripts/deploy.sh"
else
  echo ""
  echo "CIRCUITPY not mounted yet."
  echo "1. Double-tap Reset (purple → green NeoPixel)"
  echo "2. Run: ./scripts/flash-circuitpython.sh"
  echo "3. Run: ./scripts/deploy.sh"
  exit 1
fi
