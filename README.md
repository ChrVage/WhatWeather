# WhatWeather

Testing different weather APIs for Norwegian coastal weather data.

## Overview

This project fetches Norwegian coastal weather data from multiple APIs and displays the responses in various formats (HTML, Excel, YAML, and Plain Text) for testing and comparison. It is designed for local development to understand API data structures for future web application development.

## APIs Implemented

### MET Norway APIs
- **Oceanforecast 2.0**: Ocean and coastal weather forecasts
- **Locationforecast 2.0**: Location-specific weather forecasts
- **Textforecast 2.0**: Text-based weather forecasts (Norwegian)
- **Nowcast 2.0**: Short-term precipitation forecasts

### Other APIs
- **Kartverket Tide API**: Norwegian tide predictions from Kartverket's Sehavnivå API
- **BarentsWatch**: Norwegian coastal and marine data (demo implementation)
- **Nominatim**: OpenStreetMap geocoding service for converting place names to coordinates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ChrVage/WhatWeather.git
cd WhatWeather
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Testing

To quickly test the Kartverket Tide API:

```bash
cd scripts
python quick_test_tide.py
```

This will:
- Display all available Norwegian tide stations
- Fetch tide predictions for Bergen (3-day forecast)
- Show tide heights for the next 12 hours
- Use sample data if the API is unavailable

### Fetch All Weather Data

Run the main script to fetch data from all APIs and generate outputs in all formats:

```bash
cd scripts
python fetch_weather_data.py
```

This will:
1. Fetch data from all configured APIs
2. Generate outputs in four formats: HTML, Excel, YAML, and Plain Text
3. Save outputs to the `outputs/` directory with timestamps

### Individual API Scripts

Each API has its own script that can be run independently:

```bash
cd scripts

# MET Norway APIs
python met_oceanforecast.py      # Ocean forecast
python met_locationforecast.py   # Location forecast
python met_textforecast.py       # Text forecast
python met_nowcast.py            # Nowcast

# Other APIs
python kartverket_tide.py        # Kartverket tide predictions
python barentswatch_api.py       # BarentsWatch (demo)
python nominatim_api.py          # Nominatim geocoding

# Test Scripts
python quick_test_tide.py        # Quick test for Kartverket Tide API
python test_tide.py              # Full test with multiple stations
```

## Output Formats

All API responses are saved in four formats:

1. **HTML** (`outputs/html/`): Styled web pages with formatted JSON
2. **Excel** (`outputs/excel/`): Spreadsheets with metadata and data
3. **YAML** (`outputs/yaml/`): Human-readable YAML format
4. **Plain Text** (`outputs/txt/`): Simple text format with formatted JSON

## Project Structure

```
WhatWeather/
├── scripts/                    # Python scripts
│   ├── met_oceanforecast.py   # MET Norway Oceanforecast API
│   ├── met_locationforecast.py # MET Norway Locationforecast API
│   ├── met_textforecast.py    # MET Norway Textforecast API
│   ├── met_nowcast.py         # MET Norway Nowcast API
│   ├── kartverket_tide.py     # Kartverket Tide API
│   ├── barentswatch_api.py    # BarentsWatch API
│   ├── nominatim_api.py       # Nominatim Geocoding API
│   ├── test_tide.py           # Tide API test script
│   ├── quick_test_tide.py     # Quick tide API test
│   ├── format_html.py         # HTML formatter
│   ├── format_excel.py        # Excel formatter
│   ├── format_yaml.py         # YAML formatter
│   ├── format_text.py         # Plain text formatter
│   └── fetch_weather_data.py  # Main orchestrator script
├── outputs/                    # Generated outputs (gitignored)
│   ├── html/
│   ├── excel/
│   ├── yaml/
│   └── txt/
├── requirements.txt           # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

## API Documentation

### MET Norway
- [API Terms of Service](https://api.met.no/doc/TermsOfService)
- [Oceanforecast 2.0](https://api.met.no/weatherapi/oceanforecast/2.0/documentation)
- [Locationforecast 2.0](https://api.met.no/weatherapi/locationforecast/2.0/documentation)
- [Textforecast 2.0](https://api.met.no/weatherapi/textforecast/2.0/documentation)
- [Nowcast 2.0](https://api.met.no/weatherapi/nowcast/2.0/documentation)

### BarentsWatch
- [API Documentation](https://www.barentswatch.no/en/articles/api-documentation/)
- Note: Requires API key for full access (demo implementation included)

### Kartverket
- [Sehavnivå API](https://api.sehavniva.no/)
- [API Documentation](https://api.sehavniva.no/tideapi.php)
- Norwegian tide predictions for coastal locations

### Nominatim
- [Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- Note: Rate limited to 1 request per second

## Notes

- **MET Norway APIs** require a proper User-Agent header (included in scripts)
- **BarentsWatch** requires authentication for real data (demo mode available)
- **Nominatim** has rate limits (1 request/second) - automatically handled
- All API responses include metadata with timestamps and coordinates
- Output files are timestamped to prevent overwrites
- The `outputs/` directory is gitignored to keep repository clean

## Purpose

This project is designed for:
- Understanding API data structures
- Comparing different weather data sources
- Testing API responses in multiple formats
- Local development and experimentation
- Future web application development

## License

See LICENSE file for details.
