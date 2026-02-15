"""
MET Norway Textforecast API 3.0 - Fetch text-based weather forecasts
API: https://api.met.no/weatherapi/textforecast/2.0/
Note: Using version 2.0 as 3.0 may not be available yet
"""

import requests
from datetime import datetime


class TextforecastAPI:
    """Fetch text forecast data from MET Norway API"""
    
    BASE_URL = "https://api.met.no/weatherapi/textforecast/2.0/landoverview"
    
    def __init__(self, user_agent="WhatWeather/1.0 github.com/ChrVage/WhatWeather"):
        """Initialize with user agent as required by MET Norway API"""
        self.headers = {
            'User-Agent': user_agent
        }
    
    def fetch(self, language='nb'):
        """
        Fetch text forecast for Norway
        
        Args:
            language: Language code (default: 'nb' for Norwegian Bokmål)
                     Options: 'nb', 'nn', 'en'
        
        Returns:
            dict: JSON response from API or error dict
        """
        params = {
            'language': language
        }
        
        try:
            response = requests.get(
                self.BASE_URL, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            # Try to parse as JSON, fallback to text
            try:
                data = response.json()
            except ValueError:
                data = {'text': response.text}
            
            data['_metadata'] = {
                'fetched_at': datetime.now().isoformat(),
                'language': language,
                'api': 'Textforecast 2.0'
            }
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'api': 'Textforecast 2.0',
                'timestamp': datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Test the API
    api = TextforecastAPI()
    print("Fetching text forecast data...")
    data = api.fetch()
    
    if 'error' in data:
        print(f"Error: {data['error']}")
    else:
        print(f"Successfully fetched data at {data['_metadata']['fetched_at']}")
        if 'text' in data:
            print(f"Forecast text length: {len(data['text'])} characters")
