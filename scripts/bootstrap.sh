#!/usr/bin/env bash
# Download CircuitPython UF2 + library bundle and stage firmware/lib/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOWNLOADS="$ROOT/downloads"
LIB_DIR="$ROOT/firmware/lib"
UF2_URL="https://downloads.circuitpython.org/bin/adafruit_matrixportal_s3/en_US/adafruit-circuitpython-adafruit_matrixportal_s3-en_US-10.2.1.uf2"
BUNDLE_URL="https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20260508/adafruit-circuitpython-bundle-10.x-mpy-20260508.zip"

LIB_DIRS=(
  adafruit_matrixportal
  adafruit_portalbase
  adafruit_bitmap_font
  adafruit_display_text
)
LIB_MPY=(
  adafruit_requests.mpy
  adafruit_connection_manager.mpy
  adafruit_ticks.mpy
)

mkdir -p "$DOWNLOADS" "$LIB_DIR"

echo "==> Downloading CircuitPython for Matrix Portal S3..."
curl -fsSL "$UF2_URL" -o "$DOWNLOADS/matrixportal_s3.uf2"

echo "==> Downloading CircuitPython 10.x library bundle..."
curl -fsSL "$BUNDLE_URL" -o "$DOWNLOADS/bundle-10.x-mpy.zip"

echo "==> Extracting required libraries..."
rm -rf "$DOWNLOADS/bundle_extract"
unzip -q -o "$DOWNLOADS/bundle-10.x-mpy.zip" -d "$DOWNLOADS/bundle_extract"
rm -rf "$LIB_DIR"
mkdir -p "$LIB_DIR"
BUNDLE_ROOT="$(find "$DOWNLOADS/bundle_extract" -maxdepth 1 -type d -name 'adafruit-circuitpython-bundle-*' | head -1)"
BUNDLE_LIB="$BUNDLE_ROOT/lib"
if [[ ! -d "$BUNDLE_LIB" ]]; then
  echo "Could not find lib/ in bundle (got: $BUNDLE_LIB)"
  exit 1
fi
for lib in "${LIB_DIRS[@]}"; do
  if [[ -d "$BUNDLE_LIB/$lib" ]]; then
    cp -R "$BUNDLE_LIB/$lib" "$LIB_DIR/"
    echo "    copied $lib/"
  else
    echo "    WARNING: missing $lib in bundle"
  fi
done
for mpy in "${LIB_MPY[@]}"; do
  if [[ -f "$BUNDLE_LIB/$mpy" ]]; then
    cp "$BUNDLE_LIB/$mpy" "$LIB_DIR/"
    echo "    copied $mpy"
  else
    echo "    WARNING: missing $mpy in bundle"
  fi
done

if [[ ! -f "$ROOT/firmware/settings.toml" ]]; then
  cp "$ROOT/firmware/settings.toml.example" "$ROOT/firmware/settings.toml"
  echo "==> Created firmware/settings.toml from example (edit WiFi when ready)"
fi

echo ""
echo "Bootstrap complete."
echo "  UF2:     $DOWNLOADS/matrixportal_s3.uf2"
echo "  Libraries staged in: $LIB_DIR"
echo ""
echo "Next:"
echo "  1. Plug in board, double-tap Reset for bootloader (green NeoPixel)"
echo "  2. ./scripts/flash-circuitpython.sh"
echo "  3. ./scripts/deploy.sh"
