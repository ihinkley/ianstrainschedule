# LED Subway Board — Hardware Setup Guide

Wall-mounted NYC subway arrival display using a **64×32 HUB75 RGB matrix** and **Adafruit Matrix Portal S3**.

## What you have

| Part | Role |
|------|------|
| 64×32 HUB75 RGB matrix (2.5 mm pitch) | Display panel |
| 16-pin IDC ribbon cable | Data connection (panel ↔ controller) |
| Adafruit Matrix Portal S3 | WiFi controller + HUB75 driver |
| 5V power supply | Powers the LED panel (required) |
| USB-C cable | Powers controller + programming |

The Matrix Portal S3 **replaces** a bare ESP32 dev board. It is the controller only — not a second display.

- Product: [Adafruit Matrix Portal S3](https://www.adafruit.com/product/5778)
- Guide: [Adafruit MatrixPortal S3 Learning Guide](https://learn.adafruit.com/adafruit-matrixportal-s3)

## Wiring checklist

1. **Data cable** → panel **`IN`** port (not `OUT`).
2. **Panel 5V power** → Matrix Portal screw terminals (red = +5V, black = GND).
3. **USB-C** → Mac (data-capable cable, not charge-only).
4. Start at **low brightness** until the display looks correct.

If the Matrix Portal LEDs are on but the matrix is black → panel power or wrong port (`OUT` instead of `IN`).

## Garbled display? (expected on first boot)

The factory demo is configured for **32×64**. Your panel is **64×32** (same pixels, swapped dimensions).

**Garbled colors = wiring is probably fine.** Fix by flashing CircuitPython and deploying the project `code.py` in this repo (64×32).

## One-time software setup (Mac)

### Option A — automated (recommended)

**Already done on your Mac (if you ran bootstrap):** CircuitPython UF2 and libraries are cached in `downloads/` and staged in `firmware/lib/`.

1. Plug in the Matrix Portal S3 via USB-C.
2. Put the board in **bootloader mode** (first time only):
   - Double-tap **Reset** until the NeoPixel is **purple**, tap once more until **green**.
   - A drive named **MATRXS3BOOT** should appear in Finder.
3. From this folder, run either:

```bash
./scripts/install-all.sh
```

or step by step:

```bash
./scripts/bootstrap.sh      # download UF2 + libs (safe to re-run)
./scripts/flash-circuitpython.sh
./scripts/deploy.sh
```

4. After deploy, the matrix should show readable text (`FULTON ST` test).

**Note:** Flashing requires bootloader mode — that step cannot be done remotely; you must double-tap Reset once.

### Option B — manual

1. Download CircuitPython UF2: [circuitpython.org/board/adafruit_matrixportal_s3](https://circuitpython.org/board/adafruit_matrixportal_s3)
2. Bootloader → drag `.uf2` onto **MATRXS3BOOT**.
3. Copy `firmware/lib/` → `CIRCUITPY/lib/`
4. Copy `firmware/code.py` → `CIRCUITPY/code.py`
5. Copy `firmware/settings.toml` → `CIRCUITPY/settings.toml` (edit WiFi when ready)

## WiFi (later)

Edit `firmware/settings.toml` before deploy, or edit on the board:

```toml
CIRCUITPY_WIFI_SSID = "your-wifi-name"
CIRCUITPY_WIFI_PASSWORD = "your-wifi-password"
BOARD_API_URL = "https://ianstrainschedule.onrender.com/api/board"
BOARD_POLL_SECONDS = "10"
```

## If text is still wrong after deploy

Edit `firmware/code.py` and try one change at a time:

```python
matrixportal = MatrixPortal(
    width=64,
    height=32,
    serpentine=False,  # try True if still garbled
    bit_depth=4,
    rotation=0,        # try 90, 180, 270 if sideways
)
```

Save → board auto-restarts.

## Serial console (debug)

```bash
# Find port (example)
ls /dev/cu.usbmodem*

# Screen (exit: Ctrl+A then K)
screen /dev/cu.usbmodem111301 115200
```

Or use the Arduino IDE **Serial Monitor** at 115200 baud after installing board support.

## Recovery (garbled / flickering red noise)

If the display shows random red bands or heavy flicker:

1. **Check power first** — panel needs **5V on the screw terminals** (4A supply recommended). USB alone often causes exactly this symptom.
2. Run verify firmware (known-good solid colors from calibration):

```bash
./scripts/reset-verify.sh
```

You should see steady **full-screen red → green → blue** (3 seconds each). No text.

3. If verify **fails** → hardware: reseat ribbon cable on **IN**, check 5V power, try `./scripts/flash-circuitpython.sh` then reset-verify again.
4. If verify **passes** → text layer was the problem; restore the app:

```bash
./scripts/deploy-app.sh
```

**Do not throw away hardware** — A3 green and A4 blue already proved the panel + `RbG` config is correct.

## Reset / start fresh

| Goal | Action |
|------|--------|
| Redeploy app only | `./scripts/deploy.sh` |
| Re-flash CircuitPython | Bootloader + `./scripts/flash-circuitpython.sh` |
| Factory-ish demo | Re-flash UF2, do not run `deploy.sh` |

## Display & animation

All visuals live in **`firmware/display_board.py`**:

- Panel size and matrix tuning (`MATRIX_OPTS`)
- Colors, demo station/arrival copy
- Scenes: `show_demo_arrivals()`, `show_test_pattern()`, `show_solid()`
- `tick()` for future animations

`firmware/code.py` only picks which scene to run (`ACTIVE_SCENE`).

### Matrix calibration (garbled / partial display)

1. In `firmware/code.py`, set `ACTIVE_SCENE = "calibrate"`.
2. Run `./scripts/deploy.sh`.
3. Watch the panel — it cycles **14 profiles** every 5 seconds (or press **BUTTON_UP** to skip ahead).

**Adafruit 5036 panel note:** The [2.5mm 64×32 matrix](https://www.adafruit.com/product/5036) swaps green and blue vs standard HUB75. Firmware must use `color_order = "RbG"` (not plain `RGB`), or everything looks red/wrong.

**Calibration tests (in order):**

| Profiles | What you should see |
|----------|---------------------|
| A1–A2 | Full-screen **red** (A2 with RbG should look more correct than A1) |
| A3 | Full-screen **green** |
| A4 | Full-screen **blue** |
| B1–B5 | **Four tiny dots** in the corners (red TL, green TR, blue BL, yellow BR) — not big blocks |

If solids are the right color but corners are still blocky, note which **B** profile (B1–B5) is closest.

**Calibrated result (5036 panel):** `64×32`, `color_order="RbG"`, `serpentine=False`, `rotation=0`. Full-screen green (A3) and blue (A4) confirm this. Red = profile **A2** (not A1). Corner-dot tests (B1–B5) often show as lines on this hardware — ignore them if full fills look correct.

4. Note the profile **id** printed in the serial console (e.g. `PROFILE 02`).
5. Copy that profile's settings into `display_board.py` → `MATRIX_OPTS`.
6. Set `ACTIVE_SCENE = "test_pattern"`, deploy again, and confirm corner labels look right.

Serial console (115200 baud): `screen /dev/cu.usbmodem* 115200`

To try the corner-label test after calibration:

```python
ACTIVE_SCENE = "test_pattern"
```

Then `./scripts/deploy.sh`.

## Project layout

```
Led-Board-Fun/
├── SETUP.md              ← this file
├── project_plan.md       ← product vision
├── led_panel.md          ← hardware links
├── firmware/
│   ├── code.py           ← boot / scene selector
│   ├── display_board.py  ← display & animation (edit this)
│   ├── settings.toml     ← WiFi secrets (not for git)
│   └── lib/              ← CircuitPython libraries (staged)
├── scripts/
│   ├── bootstrap.sh      ← download UF2 + libs
│   ├── flash-circuitpython.sh
│   └── deploy.sh
└── downloads/            ← cached UF2 + bundle zips
```

## Next steps (after display works)

1. Phase 1: static / hardcoded arrival text layouts
2. Phase 2: backend + MTA API + WiFi polling
3. Phase 3: multi-panel chain + enclosure

See `project_plan.md` for full roadmap.
