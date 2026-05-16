# Lovable Prompt — LED Subway Board Control Website

Build a polished, mobile-first web app for controlling a WiFi-connected NYC subway LED arrival board.

## Product Context

This app controls a wall-mounted 64×32 RGB LED subway display in an apartment. The display shows real-time NYC subway arrivals from the MTA GTFS realtime feeds. The physical board itself will poll a lightweight backend every 30 seconds, so this website is the user-facing control panel for choosing what the board should show.

The UI should feel clean, premium, and transit-inspired: dark background, NYC subway color accents, simple typography, large touch targets, and a layout that works beautifully on a phone.

Style direction: **Blade Runner MTA** for the mobile app, paired with a clean matte-black LED board. It should feel like a custom cyberpunk apartment object, not just a utility app.

## Core User Goal

As a user, I want to open this site on my phone and configure:

- Which subway train lines appear on the board
- Which stations appear on the board
- Which direction(s) to show
- Board brightness
- Display mode
- A reset button to return the board to a safe default configuration

## Pages / Screens

Create a single-page mobile web app with these sections:

1. **Header**
   - App name: `Subway Board`
   - Small status text: `Connected` / `Last updated 12s ago`
   - Optional small LED-board style icon

2. **Board Preview**
   - A compact visual preview that resembles a 64×32 LED matrix.
   - Show example rows like:
     - `FULTON ST`
     - `4 ↑ 2m   5 ↓ 7m`
   - Preview should update when selections change.

3. **Train Selection**
   - Subway line buttons/chips.
   - Include at least: `1 2 3 4 5 6 7 A C E B D F M G J Z L N Q R W`
   - Selected trains should be highlighted using approximate NYC subway route colors.
   - Allow selecting multiple trains.

4. **Station Selection**
   - Searchable station dropdown/input.
   - Mobile-friendly.
   - Use mock station options for now:
     - `Fulton St`
     - `Wall St`
     - `Brooklyn Bridge-City Hall`
     - `14 St-Union Sq`
     - `Grand Central-42 St`
     - `Astor Pl`
     - `Bleecker St`
   - Allow up to 4 selected stations.

5. **Direction Selection**
   - Toggle buttons:
     - `Uptown / Bronx / Queens`
     - `Downtown / Brooklyn`
     - `Both`
   - Store as values: `northbound`, `southbound`, `both`.

6. **Brightness**
   - Slider from `5%` to `100%`.
   - Default `25%`.
   - Show current value.
   - Include quick buttons: `Night`, `Normal`, `Bright`.

7. **Display Mode**
   - Select one:
     - `Arrivals`
     - `Test Pattern`
     - `Clock + Arrivals`
     - `Off`

8. **Actions**
   - Primary button: `Save to Board`
   - Secondary button: `Refresh Preview`
   - Destructive/outline button: `Reset Board`
   - Reset should ask for confirmation and then restore:
     - trains: `4`, `5`, `6`
     - stations: `Fulton St`, `Wall St`
     - direction: `both`
     - brightness: `25`
     - mode: `Arrivals`

## Data Model

Use this config object internally:

```ts
type BoardConfig = {
  trains: string[];
  stations: string[];
  direction: 'northbound' | 'southbound' | 'both';
  brightness: number; // 5-100
  mode: 'arrivals' | 'test_pattern' | 'clock_arrivals' | 'off';
};
```

Default config:

```json
{
  "trains": ["4", "5", "6"],
  "stations": ["Fulton St", "Wall St"],
  "direction": "both",
  "brightness": 25,
  "mode": "arrivals"
}
```

## Backend API Contract

The real backend will be built separately. For now, implement the frontend so it calls these endpoints, but also include graceful mock fallback behavior if the API is not available.

Base API URL should be configurable with an environment variable:

```text
VITE_API_BASE_URL
```

Endpoints:

### `GET /api/config`

Returns current board config:

```json
{
  "trains": ["4", "5", "6"],
  "stations": ["Fulton St", "Wall St"],
  "direction": "both",
  "brightness": 25,
  "mode": "arrivals"
}
```

### `POST /api/config`

Accepts full `BoardConfig` JSON and saves it.

### `POST /api/reset`

Resets board config to defaults.

### `GET /api/board`

Returns board-ready data for preview:

```json
{
  "updated_at": "2026-05-16T15:30:00Z",
  "brightness": 25,
  "mode": "arrivals",
  "stations": [
    {
      "name": "FULTON ST",
      "arrivals": [
        {"route": "4", "direction": "uptown", "minutes": 2},
        {"route": "5", "direction": "downtown", "minutes": 7}
      ]
    },
    {
      "name": "WALL ST",
      "arrivals": [
        {"route": "2", "direction": "uptown", "minutes": 4},
        {"route": "3", "direction": "downtown", "minutes": 8}
      ]
    }
  ]
}
```

## UI Behavior

- Load existing config from `GET /api/config` on page load.
- If API fails, use default config and show a small non-blocking warning: `Using local preview mode`.
- `Save to Board` sends `POST /api/config`.
- `Reset Board` sends `POST /api/reset`, then reloads config.
- `Refresh Preview` calls `GET /api/board`.
- Preview should also update locally as the user changes fields.
- Keep the app usable even before the backend exists.

## Design Requirements

- Mobile-first layout.
- Dark theme.
- Rounded cards.
- Large touch-friendly chips/buttons.
- Subway line chips should use route-inspired colors:
  - 1/2/3: red
  - 4/5/6: green
  - 7: purple
  - A/C/E: blue
  - B/D/F/M: orange
  - G: lime
  - J/Z: brown
  - L: gray
  - N/Q/R/W: yellow
- Avoid clutter.
- Use clean React components.
- Make the code easy to fork and connect to the real backend later.

## Deliverable

Create the full frontend app with:

- Working state management
- Mock fallback data
- API utility functions
- Clean responsive UI
- Board preview component
- Train selector component
- Station selector component
- Direction selector component
- Brightness control component
- Display mode selector
- Save/reset actions

Do not implement the MTA protobuf parsing in this frontend. The backend will handle that.
