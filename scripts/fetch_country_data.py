#!/usr/bin/env python3
"""
Fetch live country metrics from World Bank API and update web/data/country_data.json.

Updates: GDP (current USD), population, internet penetration.
Other fields (climate, mobileRatio, aiReadiness) are not available from
a free real-time API and stay at their last manually curated values.

Usage:
    python3 scripts/fetch_country_data.py
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from utils import wb_indicator

DATA_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'web', 'data', 'country_data.json'
)

# World Bank indicators
WB_GDP        = 'NY.GDP.MKTP.CD'   # current USD → divide by 1e9 for $B
WB_POPULATION = 'SP.POP.TOTL'      # persons → divide by 1e6 for M
WB_INTERNET   = 'IT.NET.USER.ZS'   # % of population


def fetch():
    print('Fetching country data from World Bank...')

    print('  GDP (NY.GDP.MKTP.CD)...')
    gdp_raw = wb_indicator(WB_GDP, mrv=2)
    gdp = {k: round(v / 1e9, 1) for k, v in gdp_raw.items() if v}
    print(f'    → {len(gdp)} countries')

    print('  Population (SP.POP.TOTL)...')
    pop_raw = wb_indicator(WB_POPULATION, mrv=2)
    population = {k: round(v / 1e6, 1) for k, v in pop_raw.items() if v}
    print(f'    → {len(population)} countries')

    print('  Internet penetration (IT.NET.USER.ZS)...')
    internet = wb_indicator(WB_INTERNET, mrv=3)
    internet = {k: round(v, 1) for k, v in internet.items() if v is not None}
    print(f'    → {len(internet)} countries')

    # Load existing data (preserves climate, mobileRatio, aiReadiness)
    with open(DATA_FILE) as f:
        country_data = json.load(f)

    updated = 0
    all_isos = set(gdp) | set(population) | set(internet)
    for iso3 in all_isos:
        entry = country_data.get(iso3, {})
        if iso3 in gdp:
            entry['gdp'] = gdp[iso3]
        if iso3 in population:
            entry['population'] = population[iso3]
        if iso3 in internet:
            entry['internet'] = internet[iso3]
        if entry:
            country_data[iso3] = entry
            updated += 1

    country_data['_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    country_data['_source'] = 'World Bank Open Data (CC BY 4.0)'

    with open(DATA_FILE, 'w') as f:
        json.dump(country_data, f, indent=2)

    print(f'  Updated {updated} country entries → {os.path.relpath(DATA_FILE)}')
    return updated


if __name__ == '__main__':
    fetch()
