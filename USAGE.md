# Usage Examples

This document provides examples of how to use the Norwegian coastal weather API scripts.

## Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Fetch All Weather Data

The easiest way to get started is to run the main script that fetches from all APIs:

```bash
cd scripts
python fetch_weather_data.py
```

This will:
1. Fetch data from all 6 APIs (MET Norway x4, BarentsWatch, Nominatim)
2. Generate outputs in 4 formats (HTML, Excel, YAML, Text)
3. Save timestamped files to `../outputs/` directory

## Individual API Usage

### MET Norway - Oceanforecast

Fetch ocean and coastal weather forecasts:

```python
from met_oceanforecast import OceanforecastAPI

api = OceanforecastAPI()

# Fetch for Bergen area (Norwegian west coast)
data = api.fetch(lat=60.39, lon=5.32)

if 'error' not in data:
    print(f"Fetched at: {data['_metadata']['fetched_at']}")
    print(f"Properties: {list(data.get('properties', {}).keys())}")
```

### MET Norway - Locationforecast

Fetch location-specific weather forecasts:

```python
from met_locationforecast import LocationforecastAPI

api = LocationforecastAPI()

# Fetch for Oslo
data = api.fetch(lat=59.91, lon=10.75, altitude=5)

if 'error' not in data:
    # Access weather data
    timeseries = data.get('properties', {}).get('timeseries', [])
    if timeseries:
        first_forecast = timeseries[0]
        print(f"Time: {first_forecast['time']}")
        details = first_forecast['data']['instant']['details']
        print(f"Temperature: {details.get('air_temperature')}°C")
        print(f"Wind speed: {details.get('wind_speed')} m/s")
```

### MET Norway - Textforecast

Fetch text-based weather forecasts in Norwegian or English:

```python
from met_textforecast import TextforecastAPI

api = TextforecastAPI()

# Fetch in English
data_en = api.fetch(language='en')

# Fetch in Norwegian Bokmål
data_nb = api.fetch(language='nb')

# Fetch in Norwegian Nynorsk
data_nn = api.fetch(language='nn')
```

### MET Norway - Nowcast

Fetch short-term precipitation forecasts (next 2 hours):

```python
from met_nowcast import NowcastAPI

api = NowcastAPI()

# Fetch for Trondheim
data = api.fetch(lat=63.43, lon=10.39)

if 'error' not in data:
    timeseries = data.get('properties', {}).get('timeseries', [])
    for entry in timeseries[:5]:  # Next 5 time points
        details = entry['data']['instant']['details']
        precip = details.get('precipitation_rate', 0)
        print(f"{entry['time']}: {precip} mm/h")
```

### BarentsWatch

Fetch Norwegian coastal and marine data (requires API key for full access):

```python
from barentswatch_api import BarentsWatchAPI

# Demo mode (no API key)
api = BarentsWatchAPI()
data = api.fetch_coastal_info()
print(f"Available features: {data.get('features', [])}")

# With API key (when you have one)
api = BarentsWatchAPI(api_key='your-api-key-here')
data = api.fetch_coastal_info()
```

### Nominatim Geocoding

Convert place names to coordinates and vice versa:

```python
from nominatim_api import NominatimAPI

api = NominatimAPI()

# Search for a place
search_results = api.search("Bergen, Norway", limit=3)
if 'error' not in search_results:
    for result in search_results['results']:
        print(f"{result['display_name']}")
        print(f"  Lat: {result['lat']}, Lon: {result['lon']}")

# Reverse geocoding (coordinates to place name)
reverse_result = api.reverse(lat=60.39, lon=5.32)
if 'error' not in reverse_result:
    print(f"Location: {reverse_result['result']['display_name']}")
```

## Output Formatters

You can use the formatters independently to convert API data to different formats:

### HTML Formatter

```python
from format_html import HTMLFormatter

formatter = HTMLFormatter()
html_content = formatter.format(data, title="My Weather Data")

with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
```

### Excel Formatter

```python
from format_excel import ExcelFormatter

formatter = ExcelFormatter()
formatter.format(data, 'output.xlsx', title="My Weather Data")
```

### YAML Formatter

```python
from format_yaml import YAMLFormatter

formatter = YAMLFormatter()
yaml_content = formatter.format(data)

with open('output.yaml', 'w', encoding='utf-8') as f:
    f.write(yaml_content)
```

### Plain Text Formatter

```python
from format_text import TextFormatter

formatter = TextFormatter()
text_content = formatter.format(data, title="My Weather Data")

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(text_content)
```

## Coastal Weather Locations

Here are some popular Norwegian coastal locations with their coordinates:

```python
locations = {
    'Oslo': (59.91, 10.75),
    'Bergen': (60.39, 5.32),
    'Trondheim': (63.43, 10.39),
    'Stavanger': (58.97, 5.73),
    'Tromsø': (69.65, 18.96),
    'Kristiansand': (58.15, 8.00),
    'Bodø': (67.28, 14.41),
    'Ålesund': (62.47, 6.15)
}

# Use any location
from met_locationforecast import LocationforecastAPI
api = LocationforecastAPI()

for city, (lat, lon) in locations.items():
    data = api.fetch(lat=lat, lon=lon)
    print(f"\nWeather for {city}")
    # Process data...
```

## Testing

Run the test script to verify all formatters work correctly:

```bash
cd scripts
python test_formatters.py
```

This will create test output files in all four formats using mock data.

## API Rate Limits and Best Practices

### MET Norway
- Requires proper User-Agent header (already configured)
- Be respectful with request frequency
- Cache responses when possible

### Nominatim
- Maximum 1 request per second (automatically handled)
- Provide proper User-Agent
- Cache geocoding results

### BarentsWatch
- Requires API key for most endpoints
- Check specific rate limits in their documentation

## Error Handling

All API calls return a dictionary with error information if something goes wrong:

```python
data = api.fetch(lat=60.39, lon=5.32)

if 'error' in data:
    print(f"Error occurred: {data['error']}")
    print(f"API: {data['api']}")
    print(f"Timestamp: {data['timestamp']}")
else:
    # Process successful response
    print(f"Data fetched successfully!")
```

## Notes

- All timestamps are in ISO 8601 format
- All API responses include a `_metadata` section with fetch information
- Output files are timestamped to prevent overwrites
- The `outputs/` directory is gitignored (not committed to version control)
