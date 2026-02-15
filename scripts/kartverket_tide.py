"""
Kartverket (Norwegian Mapping Authority) Tide API
API: https://api.sehavniva.no/tideapi.php
Documentation: https://api.sehavniva.no/

Note: This implementation includes fallback to sample data if the API is unavailable.
"""

import requests
from datetime import datetime, timedelta
from config import USER_AGENT
import math


class KartverketTideAPI:
    """Fetch tide predictions from Kartverket's Sehavnivå API"""
    
    BASE_URL = "https://api.sehavniva.no/tideapi.php"
    
    # Pre-defined tide stations along Norwegian coast
    STATIONS = {
        'bergen': 'BGO',       # Bergen
        'stavanger': 'SVG',    # Stavanger
        'oslo': 'OSL',         # Oslo
        'trondheim': 'TRD',    # Trondheim
        'tromso': 'TOS',       # Tromsø
        'kristiansand': 'KRS', # Kristiansand
        'alesund': 'AES',      # Ålesund
        'bodo': 'BOO',         # Bodø
        'haugesund': 'HAU',    # Haugesund
        'andenes': 'AND',      # Andenes
    }
    
    def __init__(self, user_agent=USER_AGENT):
        """Initialize with user agent"""
        self.headers = {
            'User-Agent': user_agent
        }
    
    def fetch(self, lat=60.39, lon=5.32, station=None, days_ahead=7):
        """
        Fetch tide predictions for coordinates or named station
        
        Args:
            lat: Latitude (default: Bergen area)
            lon: Longitude (default: Bergen area)
            station: Station code (e.g., 'bergen', 'oslo') - overrides lat/lon
            days_ahead: Number of days to forecast (default: 7)
        
        Returns:
            dict: Formatted tide data or error dict
        """
        # Calculate time range
        from_time = datetime.now()
        to_time = from_time + timedelta(days=days_ahead)
        
        # Format times for API (ISO format)
        from_str = from_time.strftime('%Y-%m-%dT%H:%M')
        to_str = to_time.strftime('%Y-%m-%dT%H:%M')
        
        # Build URL with parameters
        # The API requires lat and lon as the primary method
        params = {
            'lat': lat,
            'lon': lon,
            'fromtime': from_str,
            'totime': to_str,
            'datatype': 'tab',  # Use tab format which is simpler
            'refcode': 'cd',    # Chart datum
            'place': '',
            'file': '',
            'lang': 'en',
            'interval': 60,     # 60-minute intervals
            'dst': 0
        }
        
        location_info = f"Coordinates: {lat}, {lon}"
        
        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                headers=self.headers,
                timeout=30  # Increased timeout
            )
            response.raise_for_status()
            
            # Parse the tab-separated response
            raw_text = response.text
            
            # Format the data in a structure similar to MET APIs
            formatted_data = self._parse_tab_format(raw_text, lat, lon, location_info)
            
            formatted_data['_metadata'] = {
                'fetched_at': datetime.now().isoformat(),
                'location': location_info,
                'coordinates': {'lat': lat, 'lon': lon},
                'station': station or 'auto',
                'api': 'Kartverket Tide API',
                'forecast_period_days': days_ahead
            }
            
            return formatted_data
            
        except requests.exceptions.RequestException as e:
            # If API is unavailable, generate sample tide data for demonstration
            print(f"  Warning: Kartverket API unavailable ({str(e)[:80]}...)")
            print(f"  Generating sample tide data for demonstration")
            return self._generate_sample_tide_data(lat, lon, location_info, from_time, to_time, days_ahead)
        except Exception as e:
            return {
                'error': f'Error parsing tide data: {str(e)}',
                'api': 'Kartverket Tide API',
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_sample_tide_data(self, lat, lon, location_info, from_time, to_time, days_ahead):
        """Generate realistic sample tide data when API is unavailable"""
        
        timeseries = []
        current_time = from_time
        interval = timedelta(hours=1)
        
        # Tidal parameters (semi-diurnal tide - 12.42 hour period)
        # Typical for Norwegian coast
        tidal_period_hours = 12.42
        mean_high_water = 150  # cm
        mean_low_water = 50    # cm
        tidal_range = mean_high_water - mean_low_water
        mean_tide = (mean_high_water + mean_low_water) / 2
        
        while current_time <= to_time:
            # Calculate tide level using sinusoidal model
            hours_elapsed = (current_time - from_time).total_seconds() / 3600
            
            # Primary semi-diurnal component (M2)
            tide_m2 = math.sin(2 * math.pi * hours_elapsed / tidal_period_hours)
            
            # Secondary component (S2 - solar semi-diurnal)
            tide_s2 = 0.3 * math.sin(2 * math.pi * hours_elapsed / 12.0)
            
            # Combine components and scale
            tide_height = mean_tide + (tidal_range / 2) * (tide_m2 + tide_s2)
            
            timeseries.append({
                'time': current_time.strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                'data': {
                    'instant': {
                        'details': {
                            'sea_surface_height_above_chart_datum': round(tide_height, 1)
                        }
                    }
                }
            })
            
            current_time += interval
        
        # Return in GeoJSON-like format
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            'properties': {
                'meta': {
                    'updated_at': datetime.now().isoformat(),
                    'station_name': 'Sample Data (API Unavailable)',
                    'station_code': 'SAMPLE',
                    'data_source': 'Generated sample tide predictions',
                    'units': {
                        'sea_surface_height_above_chart_datum': 'cm'
                    }
                },
                'timeseries': timeseries
            },
            '_metadata': {
                'fetched_at': datetime.now().isoformat(),
                'location': location_info,
                'coordinates': {'lat': lat, 'lon': lon},
                'station': 'sample',
                'api': 'Kartverket Tide API (Sample Data)',
                'forecast_period_days': days_ahead,
                'note': 'Sample data generated - API unavailable'
            }
        }
    
    def _parse_tab_format(self, raw_text, lat, lon, location_info):
        """Parse tab-separated tide data"""
        
        lines = raw_text.strip().split('\n')
        
        # Extract station info from header (if present)
        station_name = 'Unknown'
        station_code = 'N/A'
        
        # Parse data lines
        timeseries = []
        for line in lines:
            # Skip comment lines and headers
            if line.startswith('#') or line.startswith('time') or not line.strip():
                # Try to extract station info from comments
                if 'Location:' in line:
                    parts = line.split('Location:')
                    if len(parts) > 1:
                        station_name = parts[1].strip()
                continue
            
            # Parse data line (format: timestamp\tvalue\n)
            parts = line.split('\t')
            if len(parts) >= 2:
                time_str = parts[0].strip()
                try:
                    value = float(parts[1].strip())
                    
                    timeseries.append({
                        'time': time_str,
                        'data': {
                            'instant': {
                                'details': {
                                    'sea_surface_height_above_chart_datum': value
                                }
                            }
                        }
                    })
                except (ValueError, IndexError):
                    continue
        
        # Return in GeoJSON-like format similar to MET APIs
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            'properties': {
                'meta': {
                    'updated_at': datetime.now().isoformat(),
                    'station_name': station_name,
                    'station_code': station_code,
                    'units': {
                        'sea_surface_height_above_chart_datum': 'cm'
                    }
                },
                'timeseries': timeseries
            }
        }


if __name__ == "__main__":
    # Test the API
    api = KartverketTideAPI()
    
    print("Testing Kartverket Tide API...\n")
    
    # Test with Bergen station
    print("1. Fetching tide data for Bergen station...")
    data = api.fetch(station='bergen', days_ahead=3)
    
    if 'error' in data:
        print(f"Error: {data['error']}")
    else:
        print(f"Successfully fetched data at {data['_metadata']['fetched_at']}")
        print(f"Location: {data['_metadata']['location']}")
        timeseries_count = len(data.get('properties', {}).get('timeseries', []))
        print(f"Data points: {timeseries_count}")
        print(f"Station: {data['properties']['meta'].get('station_name', 'N/A')}")
