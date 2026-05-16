#!/usr/bin/env bash
# Clean recovery: re-download libs, deploy minimal color-cycle verify firmware.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Step 1: refresh libraries"
"$ROOT/scripts/bootstrap.sh"

echo ""
echo "==> Step 2: deploy VERIFY firmware (solid red/green/blue cycle)"
cp "$ROOT/firmware/code.py" "$ROOT/firmware/.code_verify.py"
# code.py is already verify mode; deploy copies it

if [[ ! -d /Volumes/CIRCUITPY ]]; then
  echo ""
  echo "CIRCUITPY not found. Plug in the board."
  echo "Optional full flash: double-tap Reset, then:"
  echo "  ./scripts/flash-circuitpython.sh"
  exit 1
fi

"$ROOT/scripts/deploy.sh"

echo ""
echo "VERIFY deployed."
echo "  Expect: steady full-screen RED → GREEN → BLUE (3s each), minimal flicker."
echo ""
echo "Power checklist:"
echo "  - Panel 5V on Matrix Portal screw terminals (not USB-only)"
echo "  - 4A-capable 5V supply recommended"
echo "  - Data cable on panel IN port"
echo ""
echo "When verify passes, restore the app:"
echo "  ./scripts/deploy-app.sh"
