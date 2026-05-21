#!/usr/bin/env python3
"""
Fetch health datasets and write to web/data/dashboards/health/.

Datasets
--------
life_expectancy  Life expectancy at birth — World Bank (CC BY 4.0)
                 Indicator: SP.DYN.LE00.IN
vaccination      Measles immunization rate — World Bank / WHO (CC BY 4.0)
                 Indicator: SH.IMM.MEAS
                 (Measles coverage is the standard universal vaccination proxy;
                 unlike COVID data it covers all ages and is updated annually.)
healthcare       Health expenditure per capita (USD) — World Bank / WHO (CC BY 4.0)
                 Indicator: SH.XPD.CHEX.PC.CD
                 (Used as a proxy for healthcare access where direct indices
                 are unavailable without registration.)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from utils import wb_indicator, write_dataset


def fetch_life_expectancy():
    print('  Fetching life expectancy (World Bank SP.DYN.LE00.IN, CC BY 4.0)...')
    data = wb_indicator('SP.DYN.LE00.IN')
    if not data:
        print('    WARNING: no data returned — skipping life_expectancy')
        return
    write_dataset(
        'health', 'life_expectancy', data,
        source='World Bank',
        source_url='https://data.worldbank.org/indicator/SP.DYN.LE00.IN',
        unit='years at birth',
        license='CC BY 4.0',
        year=2022,
    )


def fetch_vaccination():
    print('  Fetching measles immunization rate (World Bank SH.IMM.MEAS, CC BY 4.0)...')
    data = wb_indicator('SH.IMM.MEAS')
    if not data:
        print('    WARNING: no data returned — skipping vaccination')
        return
    write_dataset(
        'health', 'vaccination', data,
        source='World Bank / WHO',
        source_url='https://data.worldbank.org/indicator/SH.IMM.MEAS',
        unit='% of children (12–23 months) immunized against measles',
        license='CC BY 4.0',
        year=2022,
    )


def fetch_healthcare():
    print('  Fetching health expenditure (World Bank SH.XPD.CHEX.PC.CD, CC BY 4.0)...')
    # mrv=5: health expenditure data often lags 2-3 years; wider window improves coverage
    data = wb_indicator('SH.XPD.CHEX.PC.CD', mrv=5)
    if not data:
        print('    WARNING: no data returned — skipping healthcare')
        return
    write_dataset(
        'health', 'healthcare', data,
        source='World Bank / WHO',
        source_url='https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD',
        unit='current health expenditure per capita (USD)',
        license='CC BY 4.0',
        year=2021,
    )


if __name__ == '__main__':
    fetch_life_expectancy()
    fetch_vaccination()
    fetch_healthcare()
    print('  Health data complete.')
