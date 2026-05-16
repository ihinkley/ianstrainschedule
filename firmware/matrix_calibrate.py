# Matrix calibration for Adafruit 64x32 2.5mm panel (product 5036).
# That panel swaps green/blue vs standard HUB75 — use color_order "RbG".
# Press BUTTON_UP to skip to the next test.

import time

import board
import displayio
from digitalio import DigitalInOut, Pull
from adafruit_matrixportal.matrix import Matrix

HOLD_SECONDS = 6

# pattern: "solid" = full screen one color | "corners" = 4 corner pixels only
CALIBRATION_PROFILES = (
    # --- Step 1: find correct color wiring (5036 needs RbG) ---
    {"id": "A1", "pattern": "solid", "color": 0xFF0000, "width": 64, "height": 32, "serpentine": False, "rotation": 0, "color_order": "RGB"},
    {"id": "A2", "pattern": "solid", "color": 0xFF0000, "width": 64, "height": 32, "serpentine": False, "rotation": 0, "color_order": "RbG"},
    {"id": "A3", "pattern": "solid", "color": 0x00FF00, "width": 64, "height": 32, "serpentine": False, "rotation": 0, "color_order": "RbG"},
    {"id": "A4", "pattern": "solid", "color": 0x0000FF, "width": 64, "height": 32, "serpentine": False, "rotation": 0, "color_order": "RbG"},
    # --- Step 2: corner dots (should be tiny lights, not big blocks) ---
    {"id": "B1", "pattern": "corners", "width": 64, "height": 32, "serpentine": False, "rotation": 0, "color_order": "RbG"},
    {"id": "B2", "pattern": "corners", "width": 64, "height": 32, "serpentine": True, "rotation": 0, "color_order": "RbG"},
    {"id": "B3", "pattern": "corners", "width": 64, "height": 32, "serpentine": False, "rotation": 90, "color_order": "RbG"},
    {"id": "B4", "pattern": "corners", "width": 64, "height": 32, "serpentine": False, "rotation": 180, "color_order": "RbG"},
    {"id": "B5", "pattern": "corners", "width": 64, "height": 32, "serpentine": False, "rotation": 270, "color_order": "RbG"},
)


def _solid_bitmap(width, height, color_rgb):
    palette = displayio.Palette(1)
    palette[0] = color_rgb
    bitmap = displayio.Bitmap(width, height, 1)
    for x in range(width):
        for y in range(height):
            bitmap[x, y] = 0
    return displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)


def _corners_bitmap(width, height):
    # TL=red, TR=green, BL=blue, BR=yellow — one pixel per corner
    colors = (0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00)
    palette = displayio.Palette(len(colors))
    for i, c in enumerate(colors):
        palette[i] = c
    bitmap = displayio.Bitmap(width, height, len(colors))
    for x in range(width):
        for y in range(height):
            bitmap[x, y] = 0
    corners = ((0, 0, 0), (width - 1, 0, 1), (0, height - 1, 2), (width - 1, height - 1, 3))
    for x, y, idx in corners:
        bitmap[x, y] = idx
    return displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)


def _color_name(rgb):
    if rgb == 0xFF0000:
        return "RED"
    if rgb == 0x00FF00:
        return "GREEN"
    if rgb == 0x0000FF:
        return "BLUE"
    return "COLOR"


class MatrixCalibrator:
    def __init__(self):
        self._profile_index = 0
        self._last_advance = time.monotonic()
        self._button = DigitalInOut(board.BUTTON_UP)
        self._button.switch_to_input(pull=Pull.UP)
        self._button_was_pressed = True
        self._apply_profile(0)

    def _apply_profile(self, index):
        profile = CALIBRATION_PROFILES[index % len(CALIBRATION_PROFILES)]
        displayio.release_displays()

        opts = {
            "bit_depth": 4,
            "width": profile["width"],
            "height": profile["height"],
            "serpentine": profile["serpentine"],
            "rotation": profile["rotation"],
            "color_order": profile["color_order"],
        }
        matrix = Matrix(**opts)
        display = matrix.display

        w, h = profile["width"], profile["height"]
        if profile["pattern"] == "solid":
            tile = _solid_bitmap(w, h, profile["color"])
            label = _color_name(profile["color"])
        else:
            tile = _corners_bitmap(w, h)
            label = "CORNERS"

        root = displayio.Group()
        root.append(tile)
        display.root_group = root

        self._profile_index = index % len(CALIBRATION_PROFILES)
        self._last_advance = time.monotonic()
        print("PROFILE", profile["id"], label, profile["pattern"], opts)

    def _advance(self):
        self._apply_profile(self._profile_index + 1)

    def tick(self):
        now = time.monotonic()
        pressed = not self._button.value
        if pressed and not self._button_was_pressed:
            self._advance()
        self._button_was_pressed = pressed
        if now - self._last_advance >= HOLD_SECONDS:
            self._advance()


def winning_profile_hint():
    print("5036 panel: use color_order RbG. Note best B-profile id for serpentine/rotation.")
