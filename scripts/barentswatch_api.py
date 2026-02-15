"""
BarentsWatch API - Fetch Norwegian coastal and marine data
API: https://www.barentswatch.no/
Note: BarentsWatch requires authentication. This is a demo implementation.
"""

import requests
from datetime import datetime
from config import USER_AGENT


class BarentsWatchAPI:
    """Fetch data from BarentsWatch API"""
    
    # Using public endpoint for demo - real usage requires API key
    BASE_URL = "https://www.barentswatch.no/bwapi"
    
    def __init__(self, api_key=None, user_agent=USER_AGENT):
        """
        Initialize BarentsWatch API client
        
        Args:
            api_key: BarentsWatch API key (optional for demo)
            user_agent: User agent string
        """
        self.api_key = api_key
        self.headers = {
            'User-Agent': user_agent
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def fetch_coastal_info(self):
        """
        Fetch coastal information (demo endpoint)
        
        Returns:
            dict: Response data or error dict
        """
        # Note: This is a placeholder implementation
        # BarentsWatch API requires authentication and specific endpoints
        
        if not self.api_key:
            return {
                '_metadata': {
                    'fetched_at': datetime.now().isoformat(),
                    'api': 'BarentsWatch',
                    'note': 'API key required for real data access'
                },
                'info': 'BarentsWatch API provides coastal and marine data for Norway',
                'features': [
                    'Ship traffic data (AIS)',
                    'Fishing vessel positions',
                    'Weather observations',
                    'Sea temperature',
                    'Wave height and direction',
                    'Coastal zone information'
                ],
                'documentation': 'https://www.barentswatch.no/en/articles/api-documentation/',
                'note': 'This is a demo response. Real implementation requires API authentication.'
            }
        
        try:
            # Example endpoint (would need proper authentication)
            response = requests.get(
                f"{self.BASE_URL}/v1/geodata/download/fishingfacility",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            data['_metadata'] = {
                'fetched_at': datetime.now().isoformat(),
                'api': 'BarentsWatch'
            }
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'api': 'BarentsWatch',
                'timestamp': datetime.now().isoformat(),
                'note': 'API key authentication required'
            }


if __name__ == "__main__":
    # Test the API
    api = BarentsWatchAPI()
    print("Fetching BarentsWatch coastal data...")
    data = api.fetch_coastal_info()
    
    if 'error' in data:
        print(f"Error: {data['error']}")
    elif 'note' in data:
        print(f"Demo mode: {data['note']}")
        print(f"Available features: {data.get('features', [])}")
    else:
        print(f"Successfully fetched data at {data['_metadata']['fetched_at']}")
