"""
MET Norway Oceanforecast API 2.0 - Fetch coastal weather data
API: https://api.met.no/weatherapi/oceanforecast/2.0/
"""

import requests
from datetime import datetime


class OceanforecastAPI:
    """Fetch ocean forecast data from MET Norway API"""
    
    BASE_URL = "https://api.met.no/weatherapi/oceanforecast/2.0/complete"
    
    def __init__(self, user_agent="WhatWeather/1.0 github.com/ChrVage/WhatWeather"):
        """Initialize with user agent as required by MET Norway API"""
        self.headers = {
            'User-Agent': user_agent
        }
    
    def fetch(self, lat=60.10, lon=9.58):
        """
        Fetch ocean forecast for given coordinates
        Default: Norwegian coast (near Oslo fjord)
        
        Args:
            lat: Latitude (default: 60.10)
            lon: Longitude (default: 9.58)
        
        Returns:
            dict: JSON response from API or error dict
        """
        params = {
            'lat': lat,
            'lon': lon
        }
        
        try:
            response = requests.get(
                self.BASE_URL, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            data['_metadata'] = {
                'fetched_at': datetime.now().isoformat(),
                'coordinates': {'lat': lat, 'lon': lon},
                'api': 'Oceanforecast 2.0'
            }
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'api': 'Oceanforecast 2.0',
                'timestamp': datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Test the API
    api = OceanforecastAPI()
    print("Fetching ocean forecast data...")
    data = api.fetch()
    
    if 'error' in data:
        print(f"Error: {data['error']}")
    else:
        print(f"Successfully fetched data at {data['_metadata']['fetched_at']}")
        print(f"Properties available: {list(data.get('properties', {}).keys())}")
