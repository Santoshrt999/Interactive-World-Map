#!/usr/bin/env python3
"""
Master data pipeline — fetches all datasets for all three dashboards.

Usage
-----
    python3 scripts/fetch_data.py              # fetch everything
    python3 scripts/fetch_data.py climate      # fetch one category
    python3 scripts/fetch_data.py health humanitarian

Schedule (monthly cron example):
    0 0 1 * * cd /path/to/repo && python3 scripts/fetch_data.py >> logs/fetch.log 2>&1

Output
------
    web/data/dashboards/
      climate/
        co2.json           CO2 per capita (OWID / Global Carbon Project, CC BY 4.0)
        renewable.json     Renewable energy share (OWID / IEA, CC BY 4.0)
        temperature.json   Temperature anomaly (OWID / Berkeley Earth, CC BY 4.0)
      health/
        life_expectancy.json  Life expectancy (World Bank, CC BY 4.0)
        vaccination.json      Measles immunization rate (World Bank / WHO, CC BY 4.0)
        healthcare.json       Health expenditure per capita (World Bank / WHO, CC BY 4.0)
      humanitarian/
        poverty.json       Poverty headcount <$2.15/day (World Bank, CC BY 4.0)
        refugees.json      Refugees by origin (UNHCR / World Bank, Open)
        conflicts.json     Battle deaths per 100k (World Bank / UCDP, CC BY 4.0)

All data comes from official, openly licensed sources. See docs/DATA_SOURCES.md.
    web/data/
      country_data.json  GDP, population, internet penetration (World Bank, CC BY 4.0)

All data comes from official, openly licensed sources. See docs/DATA_SOURCES.md.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))


def run_country():
    from fetch_country_data import fetch
    print('\nCountry core metrics (GDP, population, internet):')
    fetch()


def run_climate():
    from fetch_climate_data import fetch_co2, fetch_renewable, fetch_temperature
    print('\nClimate datasets:')
    fetch_co2()
    fetch_renewable()
    fetch_temperature()


def run_health():
    from fetch_health_data import fetch_life_expectancy, fetch_vaccination, fetch_healthcare
    print('\nHealth datasets:')
    fetch_life_expectancy()
    fetch_vaccination()
    fetch_healthcare()


def run_humanitarian():
    from fetch_humanitarian_data import fetch_poverty, fetch_refugees, fetch_conflicts
    print('\nHumanitarian datasets:')
    fetch_poverty()
    fetch_refugees()
    fetch_conflicts()


RUNNERS = {
    'country':      run_country,
    'climate':      run_climate,
    'health':       run_health,
    'humanitarian': run_humanitarian,
}

if __name__ == '__main__':
    targets = sys.argv[1:] or list(RUNNERS)
    invalid = [t for t in targets if t not in RUNNERS]
    if invalid:
        print(f'Unknown category: {invalid}. Choose from: {list(RUNNERS)}')
        sys.exit(1)

    print(f'Fetching: {", ".join(targets)}')
    start = time.time()
    errors = []
    for category in targets:
        try:
            RUNNERS[category]()
        except Exception as exc:
            errors.append((category, exc))
            print(f'  ERROR in {category}: {exc}')

    elapsed = time.time() - start
    print(f'\nDone in {elapsed:.1f}s.')
    if errors:
        print(f'Completed with {len(errors)} error(s). Check output above.')
        sys.exit(1)
    else:
        print('All datasets updated successfully.')
