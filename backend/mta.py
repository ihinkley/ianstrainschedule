import math
import time
from dataclasses import dataclass
from typing import Any

import httpx
from google.transit import gtfs_realtime_pb2

from transit_config import (
    FEEDS,
    direction_for_stop_id,
    feed_keys_for_routes,
    display_name_for_station,
    stop_ids_for_station,
)

CACHE_SECONDS = 30


@dataclass
class FeedCache:
    fetched_at: float = 0
    feed: gtfs_realtime_pb2.FeedMessage | None = None


_caches: dict[str, FeedCache] = {}


async def fetch_mta_feed(feed_key: str) -> gtfs_realtime_pb2.FeedMessage:
    now = time.time()
    cache = _caches.setdefault(feed_key, FeedCache())
    if cache.feed is not None and now - cache.fetched_at < CACHE_SECONDS:
        return cache.feed

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(FEEDS[feed_key]["url"])
        response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    cache.feed = feed
    cache.fetched_at = now
    return feed


async def fetch_mta_feeds(selected_routes: set[str]) -> list[gtfs_realtime_pb2.FeedMessage]:
    feed_keys = feed_keys_for_routes(selected_routes)
    feeds = []
    for feed_key in feed_keys:
        feeds.append(await fetch_mta_feed(feed_key))
    return feeds


def parse_board_arrivals(feeds: list[gtfs_realtime_pb2.FeedMessage], config: dict[str, Any]) -> dict[str, Any]:
    now = int(time.time())
    selected_routes = set(config.get("trains") or ["4", "5", "6"])
    selected_stations = (config.get("stations") or ["Fulton St", "Wall St"])[:4]
    selected_direction = config.get("direction", "both")

    arrivals_by_stop: dict[str, list[dict[str, Any]]] = {}

    for feed in feeds:
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
        stop_ids = stop_ids_for_station(station_name, selected_routes)
        arrivals = []
        for stop_id in stop_ids:
            arrivals.extend(arrivals_by_stop.get(stop_id, []))

        arrivals.sort(key=lambda item: (item["minutes"], item["route"]))
        stations.append(
            {
                "name": display_name_for_station(station_name),
                "arrivals": arrivals[:5],
            }
        )

    return {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "brightness": config.get("brightness", 25),
        "mode": config.get("mode", "arrivals"),
        "stations": stations,
    }
