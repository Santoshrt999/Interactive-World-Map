# API Reference

Visual Geography Intelligence serves its data as static JSON files. There is no authentication required — all endpoints are public and free to use.

---

## Base URL

When running locally:
```
http://127.0.0.1:8000
```

---

## Endpoints

### Country Geometry

```
GET /data/countries.geojson
```

Returns a GeoJSON FeatureCollection of all 258 countries (ISO 3166-1). Each feature includes `ISO_A3`, `NAME`, and `ADMIN` properties.

---

### Dashboard Data

All dashboard datasets follow the same structure:

```
GET /data/dashboards/<category>/<dataset>.json
```

**Categories:** `climate`, `health`, `humanitarian`

**Response format:**
```json
{
  "updated": "2024-01-15",
  "source": "Source Organization",
  "url": "https://original-source-link",
  "unit": "human-readable unit",
  "data": {
    "USA": 16.5,
    "IND": 1.9,
    "CHN": 7.4
  }
}
```

Keys in `data` are ISO 3166-1 alpha-3 country codes.

---

### Available Datasets

#### Climate

| Endpoint | Description | Unit |
|----------|-------------|------|
| `/data/dashboards/climate/temperature.json` | Temperature anomaly vs 1880 baseline | °C |
| `/data/dashboards/climate/co2.json` | CO2 emissions per capita | tonnes/year |
| `/data/dashboards/climate/renewable.json` | Renewable energy share | % of total |
| `/data/dashboards/climate/deforestation.json` | Forest cover change | % annual |

#### Health

| Endpoint | Description | Unit |
|----------|-------------|------|
| `/data/dashboards/health/vaccination.json` | COVID-19 vaccination doses | per 100 people |
| `/data/dashboards/health/life_expectancy.json` | Life expectancy at birth | years |
| `/data/dashboards/health/healthcare_access.json` | Healthcare access index | 0–100 |

#### Humanitarian

| Endpoint | Description | Unit |
|----------|-------------|------|
| `/data/dashboards/humanitarian/refugees.json` | Refugee population | count |
| `/data/dashboards/humanitarian/poverty.json` | Extreme poverty rate | % population |
| `/data/dashboards/humanitarian/conflicts.json` | Active armed conflicts | count |

---

### Metadata

Each dataset has a corresponding metadata file:

```
GET /data/dashboards/<category>/metadata.json
```

```json
{
  "datasets": [
    {
      "name": "temperature",
      "source": "NASA GISS",
      "url": "https://data.giss.nasa.gov/gistemp/",
      "license": "Public Domain",
      "updated": "2024-01",
      "update_frequency": "Monthly",
      "countries_covered": 180,
      "unit": "°C anomaly vs 1880"
    }
  ]
}
```

---

## Embedding

You can embed individual dashboard panels on any website using an iframe:

```html
<iframe
  src="http://127.0.0.1:8000?dashboard=climate&overlay=temperature"
  width="800"
  height="500"
  frameborder="0">
</iframe>
```

URL parameters:
- `dashboard` — `climate`, `health`, or `humanitarian`
- `overlay` — dataset name within that dashboard
- `country` — pre-select a country (ISO 3166-1 alpha-3)

---

## Data Pipeline

To fetch and update all datasets locally:

```bash
python3 scripts/fetch_data.py
```

This pulls from all upstream sources and writes updated JSON files to `web/data/dashboards/`. See `/scripts/` for individual fetchers per category.

---

## Rate Limits

There are no rate limits on the static file server. If you are making heavy use of the data, please consider:
- Downloading the dataset once and hosting it yourself
- Contributing back if you improve or extend the data

---

## Questions

Open a GitHub issue or Discussion. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new datasets.
