"""Shared utilities for all data fetcher scripts."""

import gzip
import json
import os
import urllib.request
from datetime import datetime, timezone

# Output root — relative to this script's location
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'web', 'data', 'dashboards')

# ISO 3166-1 alpha-2 → alpha-3 (World Bank API returns alpha-2)
ISO2_TO_ISO3 = {
    'AF': 'AFG', 'AL': 'ALB', 'DZ': 'DZA', 'AD': 'AND', 'AO': 'AGO',
    'AG': 'ATG', 'AR': 'ARG', 'AM': 'ARM', 'AU': 'AUS', 'AT': 'AUT',
    'AZ': 'AZE', 'BS': 'BHS', 'BH': 'BHR', 'BD': 'BGD', 'BB': 'BRB',
    'BY': 'BLR', 'BE': 'BEL', 'BZ': 'BLZ', 'BJ': 'BEN', 'BT': 'BTN',
    'BO': 'BOL', 'BA': 'BIH', 'BW': 'BWA', 'BR': 'BRA', 'BN': 'BRN',
    'BG': 'BGR', 'BF': 'BFA', 'BI': 'BDI', 'CV': 'CPV', 'KH': 'KHM',
    'CM': 'CMR', 'CA': 'CAN', 'CF': 'CAF', 'TD': 'TCD', 'CL': 'CHL',
    'CN': 'CHN', 'CO': 'COL', 'KM': 'COM', 'CG': 'COG', 'CD': 'COD',
    'CR': 'CRI', 'CI': 'CIV', 'HR': 'HRV', 'CU': 'CUB', 'CY': 'CYP',
    'CZ': 'CZE', 'DK': 'DNK', 'DJ': 'DJI', 'DM': 'DMA', 'DO': 'DOM',
    'EC': 'ECU', 'EG': 'EGY', 'SV': 'SLV', 'GQ': 'GNQ', 'ER': 'ERI',
    'EE': 'EST', 'SZ': 'SWZ', 'ET': 'ETH', 'FJ': 'FJI', 'FI': 'FIN',
    'FR': 'FRA', 'GA': 'GAB', 'GM': 'GMB', 'GE': 'GEO', 'DE': 'DEU',
    'GH': 'GHA', 'GR': 'GRC', 'GD': 'GRD', 'GT': 'GTM', 'GN': 'GIN',
    'GW': 'GNB', 'GY': 'GUY', 'HT': 'HTI', 'HN': 'HND', 'HU': 'HUN',
    'IS': 'ISL', 'IN': 'IND', 'ID': 'IDN', 'IR': 'IRN', 'IQ': 'IRQ',
    'IE': 'IRL', 'IL': 'ISR', 'IT': 'ITA', 'JM': 'JAM', 'JP': 'JPN',
    'JO': 'JOR', 'KZ': 'KAZ', 'KE': 'KEN', 'KI': 'KIR', 'KW': 'KWT',
    'KG': 'KGZ', 'LA': 'LAO', 'LV': 'LVA', 'LB': 'LBN', 'LS': 'LSO',
    'LR': 'LBR', 'LY': 'LBY', 'LI': 'LIE', 'LT': 'LTU', 'LU': 'LUX',
    'MG': 'MDG', 'MW': 'MWI', 'MY': 'MYS', 'MV': 'MDV', 'ML': 'MLI',
    'MT': 'MLT', 'MH': 'MHL', 'MR': 'MRT', 'MU': 'MUS', 'MX': 'MEX',
    'FM': 'FSM', 'MD': 'MDA', 'MC': 'MCO', 'MN': 'MNG', 'ME': 'MNE',
    'MA': 'MAR', 'MZ': 'MOZ', 'MM': 'MMR', 'NA': 'NAM', 'NR': 'NRU',
    'NP': 'NPL', 'NL': 'NLD', 'NZ': 'NZL', 'NI': 'NIC', 'NE': 'NER',
    'NG': 'NGA', 'NO': 'NOR', 'OM': 'OMN', 'PK': 'PAK', 'PW': 'PLW',
    'PA': 'PAN', 'PG': 'PNG', 'PY': 'PRY', 'PE': 'PER', 'PH': 'PHL',
    'PL': 'POL', 'PT': 'PRT', 'QA': 'QAT', 'RO': 'ROU', 'RU': 'RUS',
    'RW': 'RWA', 'KN': 'KNA', 'LC': 'LCA', 'VC': 'VCT', 'WS': 'WSM',
    'SM': 'SMR', 'ST': 'STP', 'SA': 'SAU', 'SN': 'SEN', 'RS': 'SRB',
    'SC': 'SYC', 'SL': 'SLE', 'SG': 'SGP', 'SK': 'SVK', 'SI': 'SVN',
    'SB': 'SLB', 'SO': 'SOM', 'ZA': 'ZAF', 'SS': 'SSD', 'ES': 'ESP',
    'LK': 'LKA', 'SD': 'SDN', 'SR': 'SUR', 'SE': 'SWE', 'CH': 'CHE',
    'SY': 'SYR', 'TJ': 'TJK', 'TZ': 'TZA', 'TH': 'THA', 'TL': 'TLS',
    'TG': 'TGO', 'TO': 'TON', 'TT': 'TTO', 'TN': 'TUN', 'TR': 'TUR',
    'TM': 'TKM', 'TV': 'TUV', 'UG': 'UGA', 'UA': 'UKR', 'AE': 'ARE',
    'GB': 'GBR', 'US': 'USA', 'UY': 'URY', 'UZ': 'UZB', 'VU': 'VUT',
    'VE': 'VEN', 'VN': 'VNM', 'YE': 'YEM', 'ZM': 'ZMB', 'ZW': 'ZWE',
    'KP': 'PRK', 'KR': 'KOR', 'XK': 'XKX', 'TW': 'TWN', 'HK': 'HKG',
    'MO': 'MAC', 'PS': 'PSE',
}


def fetch_url(url, timeout=30):
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Visual-Geography-Intelligence/1.0 (open-source data project)',
            'Accept-Encoding': 'gzip, identity',
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        if resp.headers.get('Content-Encoding') == 'gzip' or (data[:2] == b'\x1f\x8b'):
            data = gzip.decompress(data)
        return data


def fetch_json(url, timeout=30):
    return json.loads(fetch_url(url, timeout))


def write_dataset(category, name, data_dict, *, source, source_url, unit, license, year):
    """Write {iso3: value} dict to web/data/dashboards/<category>/<name>.json."""
    out_dir = os.path.join(DATA_DIR, category)
    os.makedirs(out_dir, exist_ok=True)
    payload = {
        'updated': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'source': source,
        'url': source_url,
        'unit': unit,
        'license': license,
        'year': str(year),
        'data': data_dict,
    }
    path = os.path.join(out_dir, f'{name}.json')
    with open(path, 'w') as f:
        json.dump(payload, f, separators=(',', ':'))
    print(f'    wrote {len(data_dict):3d} countries → {os.path.relpath(path)}')
    return len(data_dict)


def wb_indicator(indicator, *, per_page=300, mrv=1):
    """Fetch one World Bank indicator, return {iso3: float} for most-recent year available.

    per_page is automatically scaled by mrv so that all countries fit in one page
    (each country can have up to mrv rows; World Bank API max is 10000).
    """
    effective = min(per_page * max(mrv, 1), 10000)
    url = (
        f'https://api.worldbank.org/v2/country/all/indicator/{indicator}'
        f'?format=json&mrv={mrv}&per_page={effective}'
    )
    raw = fetch_json(url)
    if len(raw) < 2 or not raw[1]:
        return {}
    result = {}
    for entry in raw[1]:
        iso2 = entry.get('country', {}).get('id', '')
        iso3 = ISO2_TO_ISO3.get(iso2)
        val = entry.get('value')
        if iso3 and val is not None:
            # Keep the most recent non-null value per country
            if iso3 not in result:
                result[iso3] = round(float(val), 3)
    return result
