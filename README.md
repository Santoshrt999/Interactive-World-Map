# Interactive-World-Map
A hardware-accelerated desktop atlas built with `PyQt6` and `ModernGL`.

**Author:** Santosh Goteti

**Built with:** Python + AI-assisted design using Raptor mini (Preview)

## Features
- Fluid 60FPS map canvas with 2D projection and 3D globe modes
- Dynamic OpenStreetMap tile rendering with local caching
- GeoJSON-based choropleth overlays for population, climate, and GDP
- Search autocomplete for major cities and countries
- Dark-mode cyberpunk minimalist UI with translucent glass panels

## Install
```bash
python3 -m pip install -r requirements.txt
```

## Browser Run
```bash
python3 main.py
```

Then open the browser page automatically at `http://127.0.0.1:8000`.

## Optional Desktop Run
If you want the original desktop UI, install Qt and ModernGL and run:
```bash
python3 main.py --desktop
```

## Notes
- The browser version uses Leaflet and OSM tiles for a fast interactive map experience
- Hover and click regions to see choropleth overlay colors for population, climate, and GDP
- Search suggestions update instantly for cities and countries
