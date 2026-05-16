"""Small station map for the first 4/5/6 MVP.

MTA realtime stop IDs use a stop code plus direction suffix:
N = northbound / uptown, S = southbound / downtown.
"""

STATION_STOP_IDS = {
    "Fulton St": ["418N", "418S"],
    "Wall St": ["419N", "419S"],
    "Brooklyn Bridge-City Hall": ["640N", "640S"],
    "Grand Central-42 St": ["631N", "631S"],
    "14 St-Union Sq": ["635N", "635S"],
    "Astor Pl": ["636N", "636S"],
    "Bleecker St": ["637N", "637S"],
}


def direction_for_stop_id(stop_id: str) -> str:
    return "uptown" if stop_id.endswith("N") else "downtown"
