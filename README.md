# Visual Geography Intelligence

**An open-source platform for understanding and visualizing global challenges.**

See climate change, public health crises, and humanitarian emergencies through real data — from NASA, WHO, the UN, and the World Bank.

**Author:** Santosh Goteti

---

## What is this?

An interactive world map that transforms complex global datasets into clear, visual stories. Built for anyone who needs to understand our world's most pressing challenges.

**Who uses it:**
- **Journalists** — embed interactive maps in data-driven stories
- **Teachers** — show students real-world data with context
- **Researchers** — access clean, open datasets in one place
- **Activists** — share compelling visualizations to raise awareness
- **NGOs** — track impact areas and communicate need

---

## Quick Start

```bash
python3 main.py
```

Opens automatically at `http://127.0.0.1:8000`. No extra dependencies needed for the browser version.

---

## Dashboards

### Climate Crisis
Temperature anomalies, CO2 emissions, renewable energy progress, and deforestation hotspots across 258 countries.
- Data: NASA GISS, IEA, Global Forest Watch

### Public Health
Vaccination coverage, healthcare access, disease distribution, and life expectancy disparities.
- Data: WHO, Our World in Data, CDC

### Humanitarian
Refugee flows, extreme poverty, food security, education access, and active conflict zones.
- Data: UNHCR, World Bank, UN OCHA, UCDP

---

## Features

- **Choropleth overlays** — Population, Climate (avg °C), and GDP with smooth color gradients across all 258 countries
- **Real country data** — 116 major countries use accurate 2022/23 figures
- **Search** — Type to find any city or country; press `/` or `Ctrl+F` to focus, `Esc` to clear
- **Region drill-down** — Click a country to see its stats in the sidebar; hover for a tooltip
- **Top 3 panel** — Updates live as you switch overlays
- **Base layer switcher** — Toggle between Modern Streets and Night Mode

---

## Desktop App (optional)

Hardware-accelerated 2D/3D map using PyQt6 and ModernGL:

```bash
python3 -m pip install -r requirements.txt
python3 main.py --desktop
```

- 60 FPS OpenGL canvas with 2D projection and 3D globe toggle
- OpenStreetMap tile rendering with local disk cache
- GeoJSON choropleth overlays with GPU-rendered polygon fills

---

## Project Structure

```
web/                    # Browser app (Leaflet + vanilla JS)
  index.html            # Single-file dashboard
  data/
    countries.geojson   # 258-country geometry (ISO 3166)
    dashboards/         # Dataset JSON files by category
      climate/
      health/
      humanitarian/
scripts/                # Data pipeline (fetch + clean datasets)
worldmap/               # Desktop app (PyQt6 + ModernGL)
docs/                   # Documentation
  CONTRIBUTING.md
  DATA_SOURCES.md
  ROADMAP.md
  API.md
browser_main.py         # Python HTTP server
main.py                 # Entry point
```

---

## Data Sources

All data from official, openly licensed sources:

| Category | Sources |
|----------|---------|
| Climate | NASA GISS, NOAA, IEA, Global Forest Watch |
| Health | WHO, CDC, Our World in Data, UNICEF |
| Humanitarian | UNHCR, World Bank, UN OCHA, UCDP |

See [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for full details and API links.

---

## Contributing

We need:
- **Data contributors** — find and integrate new datasets
- **Visualization designers** — improve charts and map styling
- **Backend developers** — automate the data pipeline
- **Writers** — add context, translate stories
- **Translators** — make the platform accessible globally

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) to get started.

---

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full plan.

**Phase 1 (Now):** 3 core dashboards — Climate, Health, Humanitarian  
**Phase 2:** Comparison tool, embed API, CSV export  
**Phase 3:** Mobile, internationalization, community data program

---

## License

[MIT](LICENSE)
