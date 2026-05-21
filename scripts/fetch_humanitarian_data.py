#!/usr/bin/env python3
"""
Fetch humanitarian datasets and write to web/data/dashboards/humanitarian/.

Datasets
--------
poverty    Poverty headcount at $2.15/day — World Bank (CC BY 4.0)
           Indicator: SI.POV.DDAY  (mrv=5 because survey data lags)
refugees   Refugee population by country of origin — UNHCR (Open / UNHCR)
           UNHCR Population Statistics API, falls back to World Bank SM.POP.REFG.OR
conflicts  Battle-related deaths per 100k — World Bank / UCDP Uppsala (CC BY 4.0)
           Indicator: VC.BTL.DETH  (derived from UCDP Armed Conflict Dataset)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from utils import fetch_json, wb_indicator, write_dataset


def fetch_poverty():
    print('  Fetching poverty rate (World Bank SI.POV.DDAY, CC BY 4.0)...')
    # mrv=10: national poverty surveys are conducted every few years; need a wide lookback window
    data = wb_indicator('SI.POV.DDAY', mrv=10)
    if not data:
        print('    WARNING: no data returned — skipping poverty')
        return
    write_dataset(
        'humanitarian', 'poverty', data,
        source='World Bank',
        source_url='https://data.worldbank.org/indicator/SI.POV.DDAY',
        unit='% population below $2.15/day (2017 PPP)',
        license='CC BY 4.0',
        year=2022,
    )


def fetch_refugees():
    print('  Fetching refugee data (UNHCR, Open / UNHCR)...')
    url = (
        'https://api.unhcr.org/population/v1/population/'
        '?limit=300&dataset=refugees&yearFrom=2023&yearTo=2023&download=false'
    )
    data = {}
    try:
        raw = fetch_json(url, timeout=20)
        for item in raw.get('items', []):
            iso3 = item.get('coo_iso', '').strip()
            count = item.get('refugees', 0)
            if iso3 and len(iso3) == 3 and count:
                data[iso3] = data.get(iso3, 0) + int(count)
    except Exception as exc:
        print(f'    UNHCR API unavailable ({exc}), falling back to World Bank SM.POP.REFG.OR...')

    if data:
        source, source_url, license_, year = (
            'UNHCR', 'https://www.unhcr.org/refugee-statistics/', 'Open (UNHCR)', 2023
        )
    else:
        # World Bank re-publishes UNHCR refugee counts under CC BY 4.0
        data = wb_indicator('SM.POP.REFG.OR')
        source, source_url, license_, year = (
            'World Bank / UNHCR',
            'https://data.worldbank.org/indicator/SM.POP.REFG.OR',
            'CC BY 4.0',
            2022,
        )

    if not data:
        print('    WARNING: no refugee data available — skipping')
        return

    write_dataset(
        'humanitarian', 'refugees', data,
        source=source,
        source_url=source_url,
        unit='refugee population by country of origin',
        license=license_,
        year=year,
    )


def fetch_conflicts():
    print('  Fetching conflict deaths (World Bank / UCDP VC.BTL.DETH, CC BY 4.0)...')
    # mrv=3: conflict data may lag 1-2 years
    data = wb_indicator('VC.BTL.DETH', mrv=3)
    if not data:
        print('    WARNING: no data returned — skipping conflicts')
        return
    write_dataset(
        'humanitarian', 'conflicts', data,
        source='World Bank / UCDP Uppsala',
        source_url='https://data.worldbank.org/indicator/VC.BTL.DETH',
        unit='battle-related deaths per 100,000 population',
        license='CC BY 4.0',
        year=2022,
    )


if __name__ == '__main__':
    fetch_poverty()
    fetch_refugees()
    fetch_conflicts()
    print('  Humanitarian data complete.')
