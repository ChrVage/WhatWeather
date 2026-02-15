"""
MET Norway Nowcast API 2.0 - Fetch short-term precipitation forecast
API: https://api.met.no/weatherapi/nowcast/2.0/
"""

import requests
from datetime import datetime


class NowcastAPI:
    """Fetch nowcast data from MET Norway API"""
    
    BASE_URL = "https://api.met.no/weatherapi/nowcast/2.0/complete"
    
    def __init__(self, user_agent="WhatWeather/1.0 github.com/ChrVage/WhatWeather"):
        """Initialize with user agent as required by MET Norway API"""
        self.headers = {
            'User-Agent': user_agent
        }
    
    def fetch(self, lat=59.91, lon=10.75):
        """
        Fetch nowcast (short-term precipitation forecast) for given coordinates
        Default: Oslo, Norway
        
        Args:
            lat: Latitude (default: 59.91 - Oslo)
            lon: Longitude (default: 10.75 - Oslo)
        
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
                'api': 'Nowcast 2.0'
            }
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'api': 'Nowcast 2.0',
                'timestamp': datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Test the API
    api = NowcastAPI()
    print("Fetching nowcast data...")
    data = api.fetch()
    
    if 'error' in data:
        print(f"Error: {data['error']}")
    else:
        print(f"Successfully fetched data at {data['_metadata']['fetched_at']}")
        print(f"Properties available: {list(data.get('properties', {}).keys())}")
