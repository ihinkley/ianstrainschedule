"""Supported subway routes, feeds, and station platform stop IDs.

MTA realtime stop IDs use a base stop code plus a direction suffix:
N = northbound / uptown, S = southbound / downtown.
"""

NUMBERED_FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
ACE_FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"

FEEDS = {
    "numbered": {
        "url": NUMBERED_FEED_URL,
        "routes": ["1", "2", "3", "4", "5", "6", "7", "S"],
    },
    "ace": {
        "url": ACE_FEED_URL,
        "routes": ["A", "C", "E"],
    },
}

SUPPORTED_TRAINS = {
    "1": {"feed": "numbered", "color": "red"},
    "2": {"feed": "numbered", "color": "red"},
    "3": {"feed": "numbered", "color": "red"},
    "4": {"feed": "numbered", "color": "green"},
    "5": {"feed": "numbered", "color": "green"},
    "6": {"feed": "numbered", "color": "green"},
    "7": {"feed": "numbered", "color": "purple"},
    "S": {"feed": "numbered", "color": "gray"},
    "A": {"feed": "ace", "color": "blue"},
    "C": {"feed": "ace", "color": "blue"},
    "E": {"feed": "ace", "color": "blue"},
}

SUPPORTED_STATIONS = {
    "Fulton St": {
        "display_name": "FULTON ST",
        "platforms": [
            {"label": "A/C", "routes": ["A", "C"], "stop_ids": ["A38N", "A38S"]},
            {"label": "2/3", "routes": ["2", "3"], "stop_ids": ["229N", "229S"]},
            {"label": "4/5", "routes": ["4", "5"], "stop_ids": ["418N", "418S"]},
        ],
    },
    "Wall St": {
        "display_name": "WALL ST",
        "platforms": [
            {"label": "2/3", "routes": ["2", "3"], "stop_ids": ["230N", "230S"]},
            {"label": "4/5", "routes": ["4", "5"], "stop_ids": ["419N", "419S"]},
        ],
    },
    "Park Place": {
        "display_name": "PARK PLACE",
        "platforms": [
            {"label": "2/3", "routes": ["2", "3"], "stop_ids": ["228N", "228S"]},
        ],
    },
    "Brooklyn Bridge-City Hall": {
        "display_name": "BK BRIDGE",
        "platforms": [
            {"label": "4/5/6", "routes": ["4", "5", "6"], "stop_ids": ["640N", "640S"]},
        ],
    },
    "Grand Central-42 St": {
        "display_name": "GRAND CTRL",
        "platforms": [
            {"label": "4/5/6", "routes": ["4", "5", "6"], "stop_ids": ["631N", "631S"]},
            {"label": "7", "routes": ["7"], "stop_ids": ["723N", "723S"]},
            {"label": "S", "routes": ["S"], "stop_ids": ["901N", "901S"]},
        ],
    },
    "14 St-Union Sq": {
        "display_name": "UNION SQ",
        "platforms": [
            {"label": "4/5/6", "routes": ["4", "5", "6"], "stop_ids": ["635N", "635S"]},
        ],
    },
    "Astor Pl": {
        "display_name": "ASTOR PL",
        "platforms": [
            {"label": "6", "routes": ["6"], "stop_ids": ["636N", "636S"]},
        ],
    },
    "Bleecker St": {
        "display_name": "BLEECKER",
        "platforms": [
            {"label": "6", "routes": ["6"], "stop_ids": ["637N", "637S"]},
        ],
    },
}


def direction_for_stop_id(stop_id: str) -> str:
    return "uptown" if stop_id.endswith("N") else "downtown"


def stop_ids_for_station(station_name: str, selected_routes: set[str]) -> list[str]:
    station = SUPPORTED_STATIONS.get(station_name)
    if not station:
        return []

    stop_ids = []
    for platform in station["platforms"]:
        platform_routes = set(platform["routes"])
        if platform_routes.isdisjoint(selected_routes):
            continue
        stop_ids.extend(platform["stop_ids"])
    return stop_ids


def feed_keys_for_routes(selected_routes: set[str]) -> list[str]:
    feed_keys = {
        SUPPORTED_TRAINS[route]["feed"]
        for route in selected_routes
        if route in SUPPORTED_TRAINS
    }
    return sorted(feed_keys)


def display_name_for_station(station_name: str) -> str:
    station = SUPPORTED_STATIONS.get(station_name)
    if not station:
        return station_name.upper()
    return station["display_name"]
