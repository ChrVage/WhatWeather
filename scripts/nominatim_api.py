"""
Nominatim Geocoding API - Convert place names to coordinates and vice versa
API: https://nominatim.openstreetmap.org/
"""

import requests
from datetime import datetime
import time
from config import USER_AGENT, NOMINATIM_RATE_LIMIT


class NominatimAPI:
    """Fetch geocoding data from Nominatim/OpenStreetMap"""
    
    BASE_URL = "https://nominatim.openstreetmap.org"
    
    def __init__(self, user_agent=USER_AGENT):
        """Initialize with user agent as required by Nominatim"""
        self.headers = {
            'User-Agent': user_agent
        }
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Ensure we don't exceed Nominatim's rate limit (1 request per second)"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < NOMINATIM_RATE_LIMIT:
            time.sleep(NOMINATIM_RATE_LIMIT - time_since_last)
        self.last_request_time = time.time()
    
    def search(self, query, limit=5):
        """
        Search for a location by name
        
        Args:
            query: Place name to search for (e.g., "Bergen, Norway")
            limit: Maximum number of results (default: 5)
        
        Returns:
            dict: JSON response from API or error dict
        """
        self._rate_limit()
        
        params = {
            'q': query,
            'format': 'json',
            'limit': limit,
            'addressdetails': 1
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            data = {
                'query': query,
                'results': results,
                '_metadata': {
                    'fetched_at': datetime.now().isoformat(),
                    'api': 'Nominatim Geocoding',
                    'result_count': len(results)
                }
            }
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'api': 'Nominatim Geocoding',
                'timestamp': datetime.now().isoformat()
            }
    
    def reverse(self, lat, lon):
        """
        Reverse geocoding: get place name from coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            dict: JSON response from API or error dict
        """
        self._rate_limit()
        
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'addressdetails': 1
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/reverse",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            data = {
                'coordinates': {'lat': lat, 'lon': lon},
                'result': result,
                '_metadata': {
                    'fetched_at': datetime.now().isoformat(),
                    'api': 'Nominatim Reverse Geocoding'
                }
            }
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'api': 'Nominatim Reverse Geocoding',
                'timestamp': datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Test the API
    api = NominatimAPI()
    
    print("Testing geocoding search...")
    search_data = api.search("Bergen, Norway", limit=3)
    if 'error' in search_data:
        print(f"Search error: {search_data['error']}")
    else:
        print(f"Found {search_data['_metadata']['result_count']} results")
    
    print("\nTesting reverse geocoding...")
    reverse_data = api.reverse(60.39, 5.32)  # Bergen coordinates
    if 'error' in reverse_data:
        print(f"Reverse error: {reverse_data['error']}")
    else:
        print(f"Location: {reverse_data['result'].get('display_name', 'N/A')}")
