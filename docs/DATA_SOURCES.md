# Data Sources

All data used in Visual Geography Intelligence comes from official, open-access sources. No proprietary or scraped data.

---

## Climate

| Dataset | Source | URL | License | Update Frequency |
|---------|--------|-----|---------|-----------------|
| Global Temperature Anomaly | NASA GISS | https://data.giss.nasa.gov/gistemp/ | Public Domain | Monthly |
| CO2 Emissions by Country | IEA Global Energy Data | https://www.iea.org/data-and-statistics | IEA Terms | Annual |
| Renewable Energy % | IEA / REN21 | https://www.ren21.net/reports/ | Open | Annual |
| Deforestation Rate | Global Forest Watch | https://www.globalforestwatch.org/ | CC BY 4.0 | Annual |
| Sea Level Rise | NOAA | https://tidesandcurrents.noaa.gov/ | Public Domain | Monthly |
| Carbon Footprint | Global Carbon Project | https://www.globalcarbonproject.org/ | CC BY 4.0 | Annual |

---

## Public Health

| Dataset | Source | URL | License | Update Frequency |
|---------|--------|-----|---------|-----------------|
| Vaccination Coverage | Our World in Data (WHO) | https://ourworldindata.org/vaccination | CC BY 4.0 | Weekly |
| Life Expectancy | World Bank | https://data.worldbank.org/indicator/SP.DYN.LE00.IN | CC BY 4.0 | Annual |
| Healthcare Access | WHO GHO | https://www.who.int/data/gho | CC BY-NC-SA | Annual |
| Maternal Mortality | UNICEF | https://data.unicef.org/ | Open | Annual |
| Disease Distribution (Malaria, TB, HIV) | WHO | https://www.who.int/data | CC BY-NC-SA | Annual |
| Disease Outbreaks (real-time) | CDC | https://wwwnc.cdc.gov/travel/notices | Public Domain | As-needed |

---

## Humanitarian

| Dataset | Source | URL | License | Update Frequency |
|---------|--------|-----|---------|-----------------|
| Refugees & Displaced Persons | UNHCR | https://www.unhcr.org/refugee-statistics/ | Open | Monthly |
| Extreme Poverty Rate | World Bank | https://data.worldbank.org/poverty | CC BY 4.0 | Annual |
| Food Security | FAO | https://www.fao.org/faostat/ | CC BY-NC-SA | Annual |
| Education Access | World Bank / UNESCO | https://data.worldbank.org/topic/education | CC BY 4.0 | Annual |
| Water & Sanitation | WHO/UNICEF JMP | https://washdata.org/ | Open | Annual |
| Active Conflicts | UCDP Uppsala | https://ucdp.uu.se/ | CC BY 4.0 | Near real-time |
| Humanitarian Emergencies | UN OCHA | https://data.humdata.org/ | CC BY IGO | As-needed |
| Natural Disaster Risk | GDACS | https://www.gdacs.org/ | Open | Real-time |

---

## Base Geography

| Dataset | Source | URL | Notes |
|---------|--------|-----|-------|
| Country Geometry (GeoJSON) | Natural Earth | https://www.naturalearthdata.com/ | 258 countries, ISO 3166 |

---

## APIs

These sources offer free APIs for programmatic access:

- **Our World in Data** — CSV download, no API key needed
- **World Bank** — REST API, no key needed: `https://api.worldbank.org/v2/`
- **WHO GHO** — REST API: `https://ghoapi.azureedge.net/api/`
- **UNHCR** — REST API: `https://api.unhcr.org/`
- **FAO STAT** — REST API: `https://fenixservices.fao.org/faostat/api/`

See `/scripts/` for working data fetcher implementations.

---

## Data Quality

We rate each metric's data quality:

- **Official** — Direct from the primary organization (WHO, NASA, World Bank)
- **Aggregated** — Compiled from official sources by a trusted intermediary (Our World in Data)
- **Estimated** — Model-based where direct measurement isn't available
- **Outdated** — Last updated more than 2 years ago (flagged in UI)

---

## Adding a New Source

See [CONTRIBUTING.md](CONTRIBUTING.md) for the standards a data source must meet and how to add it.
