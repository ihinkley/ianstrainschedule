#!/usr/bin/env bash
# Flash CircuitPython UF2 when MATRXS3BOOT is mounted
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UF2="$ROOT/downloads/matrixportal_s3.uf2"
BOOT="/Volumes/MATRXS3BOOT"

if [[ ! -f "$UF2" ]]; then
  echo "Missing $UF2 — run ./scripts/bootstrap.sh first"
  exit 1
fi

if [[ ! -d "$BOOT" ]]; then
  echo "MATRXS3BOOT not found."
  echo "Put board in bootloader mode:"
  echo "  Double-tap Reset until NeoPixel is purple, tap again until green."
  echo "  MATRXS3BOOT should appear in Finder."
  exit 1
fi

echo "==> Flashing CircuitPython..."
cp "$UF2" "$BOOT/"
sync
echo "Board is rebooting. Wait for CIRCUITPY drive (~10 seconds)."
