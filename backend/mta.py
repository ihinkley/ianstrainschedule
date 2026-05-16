import math
import time
from dataclasses import dataclass
from typing import Any

import httpx
from google.transit import gtfs_realtime_pb2

from stations import STATION_STOP_IDS, direction_for_stop_id

MTA_456_FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
CACHE_SECONDS = 30


@dataclass
class FeedCache:
    fetched_at: float = 0
    feed: gtfs_realtime_pb2.FeedMessage | None = None


_cache = FeedCache()


async def fetch_mta_feed() -> gtfs_realtime_pb2.FeedMessage:
    now = time.time()
    if _cache.feed is not None and now - _cache.fetched_at < CACHE_SECONDS:
        return _cache.feed

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(MTA_456_FEED_URL)
        response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    _cache.feed = feed
    _cache.fetched_at = now
    return feed


def parse_board_arrivals(feed: gtfs_realtime_pb2.FeedMessage, config: dict[str, Any]) -> dict[str, Any]:
    now = int(time.time())
    selected_routes = set(config.get("trains") or ["4", "5", "6"])
    selected_stations = (config.get("stations") or ["Fulton St", "Wall St"])[:4]
    selected_direction = config.get("direction", "both")

    arrivals_by_stop: dict[str, list[dict[str, Any]]] = {}

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update
        route = trip_update.trip.route_id
        if route not in selected_routes:
            continue

        for stop_update in trip_update.stop_time_update:
            stop_id = stop_update.stop_id
            if not stop_id:
                continue

            timestamp = 0
            if stop_update.HasField("arrival") and stop_update.arrival.time:
                timestamp = stop_update.arrival.time
            elif stop_update.HasField("departure") and stop_update.departure.time:
                timestamp = stop_update.departure.time

            if timestamp <= now:
                continue

            direction = direction_for_stop_id(stop_id)
            if selected_direction == "northbound" and direction != "uptown":
                continue
            if selected_direction == "southbound" and direction != "downtown":
                continue

            arrivals_by_stop.setdefault(stop_id, []).append(
                {
                    "route": route,
                    "direction": direction,
                    "minutes": max(0, math.ceil((timestamp - now) / 60)),
                }
            )

    stations = []
    for station_name in selected_stations:
        stop_ids = STATION_STOP_IDS.get(station_name, [])
        arrivals = []
        for stop_id in stop_ids:
            arrivals.extend(arrivals_by_stop.get(stop_id, []))

        arrivals.sort(key=lambda item: (item["minutes"], item["route"]))
        stations.append(
            {
                "name": station_name.upper(),
                "arrivals": arrivals[:3],
            }
        )

    return {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "brightness": config.get("brightness", 25),
        "mode": config.get("mode", "arrivals"),
        "stations": stations,
    }
