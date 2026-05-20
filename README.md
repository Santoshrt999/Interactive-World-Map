# Interactive World Map

A geospatial analytics dashboard with a browser-first interface and an optional hardware-accelerated desktop mode.

**Author:** Santosh Goteti

## Quick Start

```bash
python3 main.py
```

Opens automatically at `http://127.0.0.1:8000`. No extra dependencies needed for the browser version.

## Browser App (default)

Built with Leaflet.js on a dark Night Mode base map. Features:

- **Choropleth overlays** — Population, Climate (avg °C), and GDP with smooth continuous color gradients across all 258 countries
- **Real country data** — 116 major countries use accurate 2022/23 figures; remaining territories use latitude-weighted estimates
- **Search** — Type to find any city or country; press `/` or `Ctrl+F` to focus, `Esc` to clear
- **Region drill-down** — Click a country to see its stats in the sidebar; hover for a quick tooltip
- **Top 3 panel** — Updates live as you switch overlays
- **Base layer switcher** — Toggle between Modern Streets (default) and Night Mode (top-right corner)

## Desktop App (optional)

Hardware-accelerated 2D/3D map using PyQt6 and ModernGL. Requires additional dependencies:

```bash
python3 -m pip install -r requirements.txt
python3 main.py --desktop
```

Features:
- 60 FPS OpenGL canvas with 2D projection and 3D globe toggle
- OpenStreetMap tile rendering with local disk cache
- GeoJSON choropleth overlays with GPU-rendered polygon fills
- Dark-mode glass-panel UI

## Project Structure

```
web/              # Browser app (Leaflet + vanilla JS)
  index.html      # Single-file dashboard
  data/
    countries.geojson   # 258-country geometry (ISO 3166)
worldmap/         # Desktop app (PyQt6 + ModernGL)
browser_main.py   # Python HTTP server for the browser app
main.py           # Entry point — browser by default, --desktop flag for Qt
```
