#!/usr/bin/env python3
"""
Fetch climate datasets and write to web/data/dashboards/climate/.

Datasets
--------
co2         CO2 per capita — Our World in Data / Global Carbon Project (CC BY 4.0)
            https://github.com/owid/co2-data
renewable   Renewable energy share — Our World in Data / IEA (CC BY 4.0)
            https://github.com/owid/energy-data
temperature Each country's cumulative contribution to global warming (°C) from GHG emissions
            Our World in Data / Global Carbon Project (CC BY 4.0)
            https://github.com/owid/co2-data  column: temperature_change_from_ghg
"""

import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from utils import fetch_url, write_dataset

OWID_CO2_CSV = (
    'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv'
)
OWID_ENERGY_CSV = (
    'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv'
)


def _latest_by_iso(reader, iso_col, year_col, value_col):
    """Return {iso3: (year, value)} keeping the most-recent row per country."""
    latest = {}
    for row in reader:
        iso3 = row.get(iso_col, '').strip()
        if not iso3 or len(iso3) != 3 or iso3.upper().startswith('OWID'):
            continue
        try:
            year = int(row[year_col])
            val = float(row[value_col])
        except (KeyError, ValueError, TypeError):
            continue
        if iso3 not in latest or year > latest[iso3][0]:
            latest[iso3] = (year, round(val, 3))
    return latest


def fetch_co2():
    print('  Fetching CO2/capita (OWID / Global Carbon Project, CC BY 4.0)...')
    raw = fetch_url(OWID_CO2_CSV).decode('utf-8')
    reader = csv.DictReader(io.StringIO(raw))
    latest = _latest_by_iso(reader, 'iso_code', 'year', 'co2_per_capita')
    if not latest:
        print('    WARNING: no data parsed — skipping co2')
        return
    data = {iso3: v for iso3, (_, v) in latest.items()}
    max_year = max(y for y, _ in latest.values())
    write_dataset(
        'climate', 'co2', data,
        source='Our World in Data / Global Carbon Project',
        source_url='https://github.com/owid/co2-data',
        unit='t CO₂ per capita per year',
        license='CC BY 4.0',
        year=max_year,
    )


def fetch_renewable():
    print('  Fetching renewable energy share (OWID / IEA, CC BY 4.0)...')
    raw = fetch_url(OWID_ENERGY_CSV).decode('utf-8')
    reader = csv.DictReader(io.StringIO(raw))
    latest = _latest_by_iso(reader, 'iso_code', 'year', 'renewables_share_energy')
    if not latest:
        print('    WARNING: no data parsed — skipping renewable')
        return
    data = {iso3: v for iso3, (_, v) in latest.items()}
    max_year = max(y for y, _ in latest.values())
    write_dataset(
        'climate', 'renewable', data,
        source='Our World in Data / IEA',
        source_url='https://github.com/owid/energy-data',
        unit='% of primary energy from renewables',
        license='CC BY 4.0',
        year=max_year,
    )


def fetch_temperature():
    """Each country's cumulative contribution to global warming from GHG emissions.

    Column: temperature_change_from_ghg in the OWID CO2 dataset (CC BY 4.0).
    This shows how much global temperature has risen due to each country's
    cumulative historical emissions — a direct measure of climate impact.
    """
    print('  Fetching warming contribution by country (OWID / Global Carbon Project, CC BY 4.0)...')
    try:
        raw = fetch_url(OWID_CO2_CSV, timeout=30).decode('utf-8')
    except Exception as exc:
        print(f'    WARNING: could not fetch CO2 data for temperature ({exc})')
        return

    reader = csv.DictReader(io.StringIO(raw))
    latest = _latest_by_iso(reader, 'iso_code', 'year', 'temperature_change_from_ghg')
    if not latest:
        print('    WARNING: no temperature_change_from_ghg data parsed — skipping')
        return

    data = {iso3: v for iso3, (_, v) in latest.items()}
    max_year = max(y for y, _ in latest.values())
    write_dataset(
        'climate', 'temperature', data,
        source='Our World in Data / Global Carbon Project',
        source_url='https://github.com/owid/co2-data',
        unit='°C warming contribution from cumulative GHG emissions',
        license='CC BY 4.0',
        year=max_year,
    )


if __name__ == '__main__':
    fetch_co2()
    fetch_renewable()
    fetch_temperature()
    print('  Climate data complete.')
