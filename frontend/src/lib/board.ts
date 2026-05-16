export type Direction = "northbound" | "southbound" | "both";
export type DisplayMode = "arrivals" | "test_pattern" | "clock_arrivals" | "off";

export type BoardConfig = {
  trains: string[];
  stations: string[];
  direction: Direction;
  brightness: number;
  mode: DisplayMode;
};

export type Arrival = {
  route: string;
  direction: "uptown" | "downtown";
  minutes: number;
};

export type BoardStation = {
  name: string;
  arrivals: Arrival[];
};

export type BoardData = {
  updated_at: string;
  brightness: number;
  mode: DisplayMode;
  stations: BoardStation[];
};

export const DEFAULT_CONFIG: BoardConfig = {
  trains: ["4", "5", "6"],
  stations: ["Fulton St", "Wall St"],
  direction: "both",
  brightness: 25,
  mode: "arrivals",
};

export const ALL_TRAINS = [
  "1","2","3","4","5","6","7","A","C","E","B","D","F","M","G","J","Z","L","N","Q","R","W",
];

export const STATIONS = [
  "Fulton St",
  "Wall St",
  "Brooklyn Bridge-City Hall",
  "14 St-Union Sq",
  "Grand Central-42 St",
  "Astor Pl",
  "Bleecker St",
];

export const MAX_STATIONS = 4;

export function trainColorVar(route: string): string {
  if (["1","2","3"].includes(route)) return "var(--mta-red)";
  if (["4","5","6"].includes(route)) return "var(--mta-green)";
  if (route === "7") return "var(--mta-purple)";
  if (["A","C","E"].includes(route)) return "var(--mta-blue)";
  if (["B","D","F","M"].includes(route)) return "var(--mta-orange)";
  if (route === "G") return "var(--mta-lime)";
  if (["J","Z"].includes(route)) return "var(--mta-brown)";
  if (route === "L") return "var(--mta-gray)";
  if (["N","Q","R","W"].includes(route)) return "var(--mta-yellow)";
  return "var(--muted)";
}

export function trainTextOnColor(route: string): string {
  // yellow needs dark text for legibility
  if (["N","Q","R","W"].includes(route)) return "#111";
  return "#fff";
}
