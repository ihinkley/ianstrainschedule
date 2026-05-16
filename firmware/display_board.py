# Display & animation for the subway LED board.
# Edit this file to change layouts, colors, scenes, and motion.

import displayio
import time
import terminalio
from adafruit_display_text import bitmap_label
from adafruit_matrixportal.matrix import Matrix

# --- Panel geometry (64 wide × 32 tall, landscape) ---
PANEL_WIDTH = 64
PANEL_HEIGHT = 32

# Visible area sits ~4px below the framebuffer top on the 5036 panel.
Y_OFFSET = 4
FONT_HEIGHT = 8
# Physical matrix stays 64x32; use the full lower edge for test labels.
MAX_Y = PANEL_HEIGHT - FONT_HEIGHT
BRIGHTNESS = 0.25

# Calibrated for Adafruit 5036 (2.5mm 64x32): A3/A4 green/blue + A2 red (RbG).
# Corner-pixel tests (B1–B5) are not reliable on this panel; full fills are.
MATRIX_OPTS = {
    "width": PANEL_WIDTH,
    "height": PANEL_HEIGHT,
    "bit_depth": 2,  # lower = less flicker on ESP32-S3
    "serpentine": False,
    "rotation": 0,
    "color_order": "RbG",
}

# --- Palette (RGB hex) ---
COLOR_STATION = 0xFFFFFF
COLOR_ARRIVAL = 0x00FF00
COLOR_DIM = 0x444444
COLOR_ALERT = 0xFF3300
COLOR_ROUTE_A = 0x2850AD
COLOR_ROUTE_4 = 0x00933C
COLOR_ROUTE_2 = 0xEE352E

# --- Demo content (replace with live MTA data later) ---
DEMO_STATIONS = (
    {
        "name": "FULTON ST",
        "lines": (
            ("A", "up", 2),
            ("4", "up", 3),
            ("5", "down", 7),
        ),
    },
    {
        "name": "WALL ST",
        "lines": (
            ("2", "up", 4),
            ("3", "down", 8),
        ),
    },
)


def _dir_arrow(direction):
    return "\u2191" if direction == "up" else "\u2193"


def _format_arrival(route, direction, minutes):
    return f"{route} {_dir_arrow(direction)} {minutes}m"


class BoardDisplay:
    """Owns the matrix hardware and everything drawn on it."""

    def __init__(self):
        self._matrix = Matrix(**MATRIX_OPTS)
        self.display = self._matrix.display
        self.display.brightness = BRIGHTNESS
        self._root = displayio.Group()
        self.display.root_group = self._root
        self._labels = []
        self._anim_frame = 0
        self._last_tick = time.monotonic()
        self._mode = None
        self._train = None
        self._blink_label = None

    def clear(self):
        self._root = displayio.Group()
        self.display.root_group = self._root
        self._labels = []

    def _add_label(self, text, x, y, color):
        y = max(0, min(y, MAX_Y))
        label = bitmap_label.Label(
            terminalio.FONT,
            text=text,
            color=color,
            x=x,
            y=y + Y_OFFSET,
        )
        self._root.append(label)
        self._labels.append(label)
        return label

    def show_demo_arrivals(self, stations=DEMO_STATIONS):
        """Two-station layout — kept within 32px height."""
        self.clear()
        y = 0
        row_h = 7

        for block in stations:
            self._add_label(block["name"], 0, y, COLOR_STATION)
            y += row_h
            line_text = "  ".join(
                _format_arrival(route, direction, mins)
                for route, direction, mins in block["lines"]
            )
            self._add_label(line_text, 0, y, COLOR_ARRIVAL)
            y += row_h

    def show_solid(self, color):
        """Full-panel color — useful for testing wiring and scan settings."""
        self.clear()
        palette = displayio.Palette(1)
        palette[0] = color
        bitmap = displayio.Bitmap(PANEL_WIDTH, PANEL_HEIGHT, 1)
        for x in range(PANEL_WIDTH):
            for y in range(PANEL_HEIGHT):
                bitmap[x, y] = 0
        self._root.append(
            displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
        )

    def show_test_pattern(self):
        """Corner markers to verify the full 64×32 area is mapped."""
        self.clear()
        self._add_label("TL", 0, 0, COLOR_STATION)
        self._add_label("TR", PANEL_WIDTH - 11, 0, COLOR_STATION)
        self._add_label("BL", 0, MAX_Y, COLOR_ARRIVAL)
        self._add_label("BR", PANEL_WIDTH - 11, MAX_Y, COLOR_ARRIVAL)
        self._add_label("64x32", 18, 10, COLOR_DIM)

    def show_fun_subway_test(self):
        """Animated subway-board style demo without needing live API data."""
        self.clear()
        self._mode = "fun_subway"
        self._anim_frame = 0
        self._last_tick = time.monotonic()

        self._add_label("FULTON ST", 0, 0, COLOR_STATION)
        self._add_label("A 2m  4 3m", 0, 8, COLOR_ARRIVAL)
        self._add_label("WALL ST", 0, 16, COLOR_STATION)
        self._blink_label = self._add_label("2 4m  3 8m", 0, 24, COLOR_ROUTE_2)
        self._train = self._add_label(">", 0, MAX_Y, COLOR_DIM)

    def tick(self):
        """Advance animations. Call every loop from code.py."""
        if self._mode != "fun_subway":
            return

        now = time.monotonic()
        if now - self._last_tick < 0.12:
            return

        self._last_tick = now
        self._anim_frame += 1

        if self._train:
            self._train.x = self._anim_frame % PANEL_WIDTH

        if self._blink_label:
            self._blink_label.color = (
                COLOR_ROUTE_2 if (self._anim_frame // 4) % 2 == 0 else COLOR_ALERT
            )
