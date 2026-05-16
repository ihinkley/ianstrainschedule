NYC Real-Time Subway Arrival Display
Project Overview

Goal:
Build a wall-mounted, WiFi-connected LED subway arrival board for our NYC apartment that displays real-time upcoming train arrivals for configurable nearby subway stations. The board should feel like a premium modern transit display — part functional utility, part interactive art piece.

Core Experience:
The display continuously shows the next upcoming trains for up to 4 selected subway stations. The board updates automatically in real time using MTA arrival data and can be reconfigured from a phone/web app without touching the hardware.

Example Display:
----------------------------------------
FULTON ST
A ↑ 2m    4 ↑ 3m    5 ↓ 7m

WALL ST
2 ↑ 4m    3 ↓ 8m
----------------------------------------

Key Features:
- Real-time NYC subway arrival data
- Configurable stations and directions
- WiFi-connected
- Brightness controls / night mode
- Clean modern subway-sign aesthetic
- Expandable by chaining additional LED panels
- Remote configuration from phone/web app
- Potential animations for delays / arrivals

Hardware:
Display:
- HUB75 RGB LED Matrix Panel
- Starting with:
  - 64x32 RGB matrix
  - 2.5mm pixel pitch
- Additional panels can be chained later to create larger displays

Controller:
- ESP32-WROOM-32D microcontroller
- Handles:
  - WiFi connectivity
  - Data fetching
  - Display rendering
  - Brightness control

Power:
- 5V external power supply sized appropriately for number of panels

Software Architecture:
1. LED Display
- ESP32 runs firmware that connects to WiFi
- Fetches display data from backend API
- Renders train arrivals onto LED matrix

2. Backend Service
- Polls MTA APIs / GTFS feeds
- Processes upcoming train arrivals
- Stores device configuration
- Exposes lightweight APIs for the display

3. Phone / Web App
- Lets users:
  - Select stations
  - Select train directions
  - Configure up to 4 displayed stations
  - Adjust brightness / modes
- Sends configuration updates to backend

Expansion Possibilities:
- Multi-panel subway ticker
- Full-width living room transit board
- Delay animations
- Ambient light auto-dimming
- Multiple saved station presets
- Weather / transit integration
- Custom themes
- “Leave now” commute notifications
- Arrival countdown animations

Design Goals:
- Minimalist NYC transit-inspired aesthetic
- Matte black frame
- Soft dimmable LED brightness
- Readable from across the room
- Clean typography
- Hidden wiring
- Feels like a premium design object, not a DIY electronics project

Initial MVP:
Phase 1:
- One 64x32 panel
- ESP32 controller
- Basic WiFi connection
- Hardcoded test text
- Simple subway arrival display

Phase 2:
- Live MTA integration
- Configurable stations
- Phone/web configuration app
- Improved layouts and animations

Phase 3:
- Multi-panel expansion
- Final wall-mounted enclosure
- Full apartment installation