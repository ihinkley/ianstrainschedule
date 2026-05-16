# Full app entry — use this after verify mode passes.
# To switch: copy code_app.py over code.py (or use deploy-app.sh)

import display_board

ACTIVE_SCENE = "fun_subway"  # fun_subway | test_pattern | demo | solid

board = display_board.BoardDisplay()

if ACTIVE_SCENE == "demo":
    board.show_demo_arrivals()
elif ACTIVE_SCENE == "fun_subway":
    board.show_fun_subway_test()
elif ACTIVE_SCENE == "test_pattern":
    board.show_test_pattern()
elif ACTIVE_SCENE == "solid":
    board.show_solid(0x002200)
else:
    board.show_test_pattern()

while True:
    board.tick()
