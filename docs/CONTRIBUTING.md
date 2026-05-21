# Contributing Guide

Thank you for helping build Visual Geography Intelligence. This project runs on open data and open collaboration.

---

## Ways to Contribute

### Add a New Dataset
1. Find an open, officially licensed source (government, UN, NGO, academic)
2. Open an issue: "Add [dataset name] — [category]"
3. Fork the repo and create a data fetcher in `/scripts/`
4. Convert the data to JSON format matching the structure in `web/data/dashboards/`
5. Update `docs/DATA_SOURCES.md` with the source link and update frequency
6. Submit a pull request linking to the issue

### Improve Visualizations
- Better color scales, legends, or tooltip designs
- New chart types in the sidebar
- Accessibility improvements (contrast, keyboard nav)

### Improve the Data Pipeline
- Automate fetching for existing scripts in `/scripts/`
- Add error handling and data validation
- Add scheduling support

### Write or Translate
- Add "why this matters" context to existing metrics
- Translate the UI or data stories to other languages (Spanish, French, Mandarin are priorities)
- Write explainer text for new datasets

### Report Issues
- Broken data or outdated figures → open an issue with "Data:" prefix
- UI bugs → open an issue with "Bug:" prefix
- Feature ideas → open a GitHub Discussion

---

## Dataset Standards

When adding a dataset, it should:
- Come from an official, openly licensed source (no scraped or paywalled data)
- Cover at least 50 countries
- Be updated at least annually
- Include a `metadata.json` next to the data file:

```json
{
  "name": "dataset_name",
  "source": "Source Organization",
  "url": "https://direct-link-to-data",
  "license": "CC BY 4.0",
  "updated": "2024-01",
  "update_frequency": "Annual",
  "countries_covered": 180,
  "unit": "per 1000 people"
}
```

---

## Data File Format

All dashboard data goes in `web/data/dashboards/<category>/<dataset>.json`:

```json
{
  "updated": "2024-01-15",
  "source": "WHO Global Health Observatory",
  "unit": "doses per 100 people",
  "data": {
    "USA": 189.4,
    "IND": 87.2,
    "NGA": 31.0
  }
}
```

Keys must be ISO 3166-1 alpha-3 country codes (matching `countries.geojson`).

---

## What We Need Most

| Category | Dataset | Status |
|----------|---------|--------|
| Climate | CO2 emissions by country | Needed |
| Climate | Deforestation rate | Needed |
| Climate | Sea level rise | Needed |
| Health | Vaccination coverage | Needed |
| Health | Maternal mortality | Needed |
| Humanitarian | Refugee count by origin | Needed |
| Humanitarian | Extreme poverty rate | Needed |
| Humanitarian | Active conflicts | Needed |

---

## Local Setup

```bash
git clone https://github.com/Santoshrt999/Interactive-World-Map
cd Interactive-World-Map
python3 main.py
```

The browser app runs without any extra dependencies. Open `http://127.0.0.1:8000`.

For the desktop app:
```bash
python3 -m pip install -r requirements.txt
python3 main.py --desktop
```

---

## Questions?

Open a GitHub Discussion or file an issue. We respond to everything.
