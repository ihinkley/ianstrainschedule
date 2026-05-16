import type { BoardConfig, BoardData } from "./board";
import { DEFAULT_CONFIG } from "./board";

const BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "") ?? "";

async function safeFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.json()) as T;
}

export async function getConfig(): Promise<BoardConfig> {
  return safeFetch<BoardConfig>("/api/config");
}

export async function saveConfig(config: BoardConfig): Promise<void> {
  await safeFetch<unknown>("/api/config", {
    method: "POST",
    body: JSON.stringify(config),
  });
}

export async function resetConfig(): Promise<BoardConfig> {
  await safeFetch<unknown>("/api/reset", { method: "POST" });
  return getConfig().catch(() => DEFAULT_CONFIG);
}

export async function getBoard(): Promise<BoardData> {
  return safeFetch<BoardData>("/api/board");
}

/** Generate a mock board data preview from the current config. */
export function mockBoardData(config: BoardConfig): BoardData {
  const pickTrains = config.trains.length ? config.trains : ["4", "5", "6"];
  const stations = (config.stations.length ? config.stations : ["Fulton St"]).slice(0, 4);
  return {
    updated_at: new Date().toISOString(),
    brightness: config.brightness,
    mode: config.mode,
    stations: stations.map((name, idx) => ({
      name: name.toUpperCase(),
      arrivals: ([
        {
          route: pickTrains[idx % pickTrains.length],
          direction: "uptown" as const,
          minutes: 2 + idx,
        },
        {
          route: pickTrains[(idx + 1) % pickTrains.length],
          direction: "downtown" as const,
          minutes: 5 + idx * 2,
        },
      ]).filter((a) =>
        config.direction === "both"
          ? true
          : config.direction === "northbound"
          ? a.direction === "uptown"
          : a.direction === "downtown",
      ),
    })),
  };
}
