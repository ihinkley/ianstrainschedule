from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mta import fetch_mta_feed, parse_board_arrivals

CONFIG_PATH = Path(__file__).with_name("config.json")


class BoardConfig(BaseModel):
    trains: list[str] = Field(default_factory=lambda: ["4", "5", "6"])
    stations: list[str] = Field(default_factory=lambda: ["Fulton St", "Wall St"])
    direction: Literal["northbound", "southbound", "both"] = "both"
    brightness: int = Field(default=25, ge=5, le=100)
    mode: Literal["arrivals", "test_pattern", "clock_arrivals", "off"] = "arrivals"


DEFAULT_CONFIG = BoardConfig()

app = FastAPI(title="Ian's Train Board API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_config() -> BoardConfig:
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG
    return BoardConfig.model_validate_json(CONFIG_PATH.read_text())


def save_config(config: BoardConfig) -> BoardConfig:
    CONFIG_PATH.write_text(config.model_dump_json(indent=2))
    return config


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/config")
def get_config() -> BoardConfig:
    return load_config()


@app.post("/api/config")
def post_config(config: BoardConfig) -> BoardConfig:
    return save_config(config)


@app.post("/api/reset")
def reset_config() -> BoardConfig:
    return save_config(DEFAULT_CONFIG)


@app.get("/api/board")
async def get_board() -> dict:
    config = load_config()
    feed = await fetch_mta_feed()
    return parse_board_arrivals(feed, config.model_dump())
