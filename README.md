# 🌍 Visual Geography Intelligence

### *See the world's challenges. Understand the data. Drive change.*

An **open-source platform** for exploring and visualizing global data—climate change, public health, humanitarian crises, and the digital divide—using real, authoritative data from World Bank, WHO, UN, and other official sources.

[**🚀 Launch App**](#quick-start) | [**📊 Dashboards**](#dashboards) | [**🤝 Contribute**](#contributing)

---

## Quick Start

```bash
python3 main.py
```

Opens at `http://localhost:8000` — no build step, no dependencies beyond Python 3.

For the AI Insight feature, also set your API key:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 main.py
```

---

## ✅ Completed Features

### 🗺️ Map Engine
- MapLibre GL JS v4 · 3D globe projection · OpenFreeMap dark tile base
- 258-country GeoJSON with India's **official boundary** (J&K / Ladakh included via Natural Earth India POV dataset)
- Choropleth overlays, hover highlights, country selection, animated transitions

### 📊 Data Overlays — 5 tabs, 15 metrics

| Tab | Overlays |
|-----|----------|
| Explorer | Population, Avg Temperature, GDP |
| Climate | Warming anomaly, CO₂/capita, Renewable % |
| Health | Vaccination, Life Expectancy, Health Spend |
| Aid | Poverty, Conflict Deaths, Refugees |
| **Tech** | Internet %, Mobile Ratio, AI Readiness Index |

### 🔍 Explorer Panel
- Country search with autocomplete
- Stats panel: count, average, highest, lowest country
- Color legend with live min/max/mid ticks
- Country click → detail panel with Top-10 bar chart (Chart.js)
- Source + license attribution on every overlay

### 🕐 Timeline Slider (2000–2024)
- Horizontal scrubber at the bottom of the map
- Drag to any year — choropleth re-renders with year-adjusted values
- **Animate** button: plays 2000→2024 at 1 second/year, with pause
- Growth models for GDP, population, internet penetration, AI readiness, and all other overlays

### ⚖️ Compare Mode
- "Compare" button (top-right) switches to crosshair selection
- Click two countries → bottom drawer slides up with side-by-side bars
- 6 metrics: Population, GDP, Avg Temp, Internet %, AI Readiness, Mobile Ratio
- Higher-value bar highlighted in green; stacks vertically on mobile

### ✨ AI Insight Panel
- "Generate Insight" button in every country detail panel
- Calls `GET /api/insight?country=<ISO3>` on the Python backend
- Backend uses **Anthropic claude-sonnet-4-6** — 3-sentence geopolitical + economic analysis
- Loading spinner while fetching; graceful error display if key is missing

---

## 📁 Project Structure

```
Interactive-World-Map/
├── web/
│   ├── index.html               # Entire frontend (single file)
│   └── data/
│       ├── countries.geojson    # 258-country boundaries (India POV)
│       └── dashboards/
│           ├── climate/         # temperature.json, co2.json, renewable.json
│           ├── health/          # vaccination.json, life_expectancy.json, healthcare.json
│           └── humanitarian/    # refugees.json, poverty.json, conflicts.json
├── browser_main.py              # Python HTTP server + /api/insight endpoint
├── main.py                      # Entry point
├── scripts/                     # Data fetch scripts (World Bank, WHO, UNHCR)
└── docs/                        # Strategy docs and roadmaps
```

---

## 🗺️ Roadmap — Next Up

- [ ] Embed shareable link per country / overlay
- [ ] Export comparison as image / PDF
- [ ] More countries in COUNTRY_DATA (currently ~120 of 258 have full tech data)
- [ ] Gilgit-Baltistan boundary fix (India POV for Pakistan polygon)
- [ ] Mobile sidebar UX improvements
- [ ] Story mode (guided data narratives)
- [ ] Ocean health dashboard
- [ ] Education & gender inequality overlays

---

## 🔗 Data Sources

| Overlay | Source | License |
|---------|--------|---------|
| Population, GDP, Poverty | World Bank | CC BY 4.0 |
| Climate, CO₂, Renewable | Our World in Data / IEA | CC BY 4.0 |
| Vaccination, Life Expectancy, Health Spend | WHO / World Bank | CC BY 4.0 |
| Conflict Deaths | UCDP / World Bank | CC BY 4.0 |
| Refugees | UNHCR | Open |
| Internet %, Mobile Ratio | ITU / World Bank | CC BY 4.0 |
| AI Readiness Index | Oxford Insights | CC BY 4.0 |
| Map boundaries | Natural Earth (India POV) | Public Domain |

---

## 🤝 Contributing

1. Fork · pick an issue · PR
2. Add new datasets to `web/data/dashboards/`
3. Add overlay meta + data entries in `web/index.html`

---

## 📜 License

MIT — free to use, modify, distribute. See [LICENSE](LICENSE)

**Questions?** Email santoshgoteti9@gmail.com or open a discussion.

---

*Last updated: May 2026*
