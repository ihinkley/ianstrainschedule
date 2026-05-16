# VERIFY MODE — minimal firmware to confirm the panel still works.
# Cycles full-screen red → green → blue every 3 seconds.
# When this looks stable, set ACTIVE_SCENE in code_app.py and deploy app.

import time
import displayio
from adafruit_matrixportal.matrix import Matrix

WIDTH = 64
HEIGHT = 32
MATRIX_OPTS = {
    "width": WIDTH,
    "height": HEIGHT,
    "bit_depth": 2,
    "serpentine": False,
    "rotation": 0,
    "color_order": "RbG",  # required for Adafruit 5036 panel
}

COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
COLOR_NAMES = ("RED", "GREEN", "BLUE")

matrix = Matrix(**MATRIX_OPTS)
palette = displayio.Palette(1)
bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
for _x in range(WIDTH):
    for _y in range(HEIGHT):
        bitmap[_x, _y] = 0

grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(grid)
matrix.display.root_group = group

_index = 0
palette[0] = COLORS[0]
print("VERIFY:", COLOR_NAMES[0], MATRIX_OPTS)

while True:
    time.sleep(3)
    _index = (_index + 1) % len(COLORS)
    palette[0] = COLORS[_index]
    print("VERIFY:", COLOR_NAMES[_index])
