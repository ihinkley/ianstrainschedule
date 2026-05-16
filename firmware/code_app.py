# Full app entry — use this after verify mode passes.
# To switch: copy code_app.py over code.py (or use deploy-app.sh)

import display_board
import time

ACTIVE_SCENE = "live_board"  # live_board | claude_trapped | fun_subway | test_pattern | demo | solid

board = display_board.BoardDisplay()
last_live_data = None

if ACTIVE_SCENE == "live_board":
    import network_board

    client = network_board.BoardApiClient()
    while last_live_data is None:
        try:
            board.show_status("WIFI", "CONNECT", display_board.COLOR_CYAN)
            client.connect()
            board.show_status("API", "POLL", display_board.COLOR_CYAN)
            last_live_data = client.poll(force=True)
            board.show_live_board(last_live_data)
        except Exception:
            board.show_status("NET ERR", "RETRY", display_board.COLOR_ALERT)
            time.sleep(5)
elif ACTIVE_SCENE == "demo":
    board.show_demo_arrivals()
elif ACTIVE_SCENE == "claude_trapped":
    board.show_claude_trapped()
elif ACTIVE_SCENE == "fun_subway":
    board.show_fun_subway_test()
elif ACTIVE_SCENE == "test_pattern":
    board.show_test_pattern()
elif ACTIVE_SCENE == "solid":
    board.show_solid(0x002200)
else:
    board.show_test_pattern()

while True:
    if ACTIVE_SCENE == "live_board":
        try:
            data = client.poll()
            if data is not last_live_data:
                last_live_data = data
                board.show_live_board(data)
        except Exception:
            board.show_status("API ERR", "RETRYING", display_board.COLOR_ALERT)
    board.tick()
    if ACTIVE_SCENE == "live_board":
        time.sleep(1)
