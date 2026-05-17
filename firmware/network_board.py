import os
import ssl
import time

import adafruit_requests
import socketpool
import wifi


DEFAULT_POLL_SECONDS = 10


def _arrival_signature(arrival):
    return (
        arrival.get("route"),
        arrival.get("direction"),
        arrival.get("minutes"),
    )


def _station_signature(station):
    return (
        station.get("name"),
        tuple(_arrival_signature(arrival) for arrival in station.get("arrivals", [])),
    )


def _board_signature(data):
    return (
        data.get("brightness"),
        data.get("mode"),
        tuple(_station_signature(station) for station in data.get("stations", [])),
    )


class BoardApiClient:
    def __init__(self):
        self.api_url = os.getenv("BOARD_API_URL")
        self.poll_seconds = int(os.getenv("BOARD_POLL_SECONDS") or DEFAULT_POLL_SECONDS)
        self._pool = None
        self._requests = None
        self._last_poll = 0
        self._last_data = None
        self._last_signature = None

    def connect(self):
        ssid = os.getenv("CIRCUITPY_WIFI_SSID")
        password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
        if not ssid or not password:
            raise RuntimeError("Missing WiFi credentials in settings.toml")
        if not self.api_url:
            raise RuntimeError("Missing BOARD_API_URL in settings.toml")

        if not wifi.radio.connected:
            wifi.radio.connect(ssid, password)

        self._pool = socketpool.SocketPool(wifi.radio)
        self._requests = adafruit_requests.Session(self._pool, ssl.create_default_context())

    def poll(self, force=False):
        now = time.monotonic()
        if not force and self._last_data is not None and now - self._last_poll < self.poll_seconds:
            return self._last_data

        if self._requests is None:
            self.connect()

        response = None
        try:
            response = self._requests.get(self.api_url)
            data = response.json()
            signature = _board_signature(data)
            self._last_poll = now
            if self._last_data is not None and signature == self._last_signature:
                return self._last_data

            self._last_data = data
            self._last_signature = signature
            return data
        finally:
            if response:
                response.close()
