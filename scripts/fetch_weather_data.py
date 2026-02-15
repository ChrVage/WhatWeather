#!/usr/bin/env python3
"""
Main script to fetch Norwegian coastal weather data from multiple APIs
and generate outputs in various formats (HTML, Excel, YAML, Plain Text)
"""

import os
import sys
from datetime import datetime

# Import configuration
from config import OUTPUT_DIR

# Import API clients
from met_oceanforecast import OceanforecastAPI
from met_locationforecast import LocationforecastAPI
from met_textforecast import TextforecastAPI
from met_nowcast import NowcastAPI
# from barentswatch_api import BarentsWatchAPI
from nominatim_api import NominatimAPI
from kartverket_tide import KartverketTideAPI

# Import formatters
from format_html import HTMLFormatter
from format_excel import ExcelFormatter
from format_yaml import YAMLFormatter
from format_text import TextFormatter
import json


class WeatherDataCollector:
    """Orchestrate fetching and formatting of weather data from multiple APIs"""
    
    def __init__(self, output_dir=OUTPUT_DIR):
        """
        Initialize the collector
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        self.ensure_output_dirs()
        
        # Initialize formatters
        self.html_formatter = HTMLFormatter()
        self.excel_formatter = ExcelFormatter()
        self.yaml_formatter = YAMLFormatter()
        self.text_formatter = TextFormatter()
    
    def ensure_output_dirs(self):
        """Create output directories if they don't exist"""
        subdirs = ['json', 'excel']
        for subdir in subdirs:
            path = os.path.join(self.output_dir, subdir)
            os.makedirs(path, exist_ok=True)
    
    def save_outputs(self, data, name, title, include_excel=False):
        """
        Save data in JSON format (default response) and optionally Excel
        
        Args:
            data: Dictionary containing API response
            name: Base filename (without extension)
            title: Title for the output
            include_excel: Whether to also generate Excel output for timeseries data
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{name}_{timestamp}"
        
        print(f"  Saving {name} output...")
        
        # JSON (default response format)
        json_path = os.path.join(self.output_dir, 'json', f"{base_name}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    ✓ JSON: {json_path}")
        
        # Excel (for timeseries data)
        if include_excel:
            excel_path = os.path.join(self.output_dir, 'excel', f"{base_name}.xlsx")
            self.excel_formatter.format(data, excel_path, title)
            print(f"    ✓ Excel: {excel_path}")
    
    def fetch_all(self):
        """Fetch data from all APIs and save in all formats"""
        print("\n" + "=" * 80)
        print("Norwegian Coastal Weather Data Collector".center(80))
        print("=" * 80 + "\n")
        
        # Test coordinates for Norwegian coast
        # Stolmen area
        lat_stolmen = 60.00
        lon_stolmen = 5.00
        
        # 1. MET Norway - Oceanforecast
        print("1. Fetching MET Norway Oceanforecast 2.0...")
        try:
            ocean_api = OceanforecastAPI()
            ocean_data = ocean_api.fetch(lat=lat_stolmen, lon=lon_stolmen)
            self.save_outputs(ocean_data, "oceanforecast", "MET Norway Oceanforecast 2.0", include_excel=True)
            print("  ✓ Oceanforecast data collected\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # 2. MET Norway - Locationforecast
        print("2. Fetching MET Norway Locationforecast 2.0...")
        try:
            location_api = LocationforecastAPI()
            location_data = location_api.fetch(lat=lat_stolmen, lon=lon_stolmen)
            self.save_outputs(location_data, "locationforecast", "MET Norway Locationforecast 2.0", include_excel=True)
            print("  ✓ Locationforecast data collected\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # 3. MET Norway - Textforecast
        print("3. Fetching MET Norway Textforecast 2.0...")
        try:
            text_api = TextforecastAPI()
            text_data = text_api.fetch(language='en')
            self.save_outputs(text_data, "textforecast", "MET Norway Textforecast 2.0")
            print("  ✓ Textforecast data collected\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # 4. MET Norway - Nowcast
        print("4. Fetching MET Norway Nowcast 2.0...")
        try:
            nowcast_api = NowcastAPI()
            nowcast_data = nowcast_api.fetch(lat=lat_stolmen, lon=lon_stolmen)
            self.save_outputs(nowcast_data, "nowcast", "MET Norway Nowcast 2.0", include_excel=True)
            print("  ✓ Nowcast data collected\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # 5. Kartverket - Tide Predictions
        print("5. Fetching Kartverket Tide predictions...")
        try:
            tide_api = KartverketTideAPI()
            tide_data = tide_api.fetch(lat=lat_stolmen, lon=lon_stolmen, days_ahead=7)
            self.save_outputs(tide_data, "tide", "Kartverket Tide Predictions", include_excel=True)
            print("  ✓ Tide data collected\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # 6. BarentsWatch
        # print("6. Fetching BarentsWatch coastal data...")
        # try:
        #     barents_api = BarentsWatchAPI()
        #     barents_data = barents_api.fetch_coastal_info()
        #     self.save_outputs(barents_data, "barentswatch", "BarentsWatch Coastal Data")
        #     print("  ✓ BarentsWatch data collected\n")
        # except Exception as e:
        #     print(f"  ✗ Error: {e}\n")
        
        # 7. Nominatim - Geocoding
        print("7. Fetching Nominatim geocoding data...")
        try:
            nominatim_api = NominatimAPI()
            
            # Search for Bergen
            search_data = nominatim_api.search("Bergen, Norway", limit=3)
            self.save_outputs(search_data, "nominatim_search_bergen", "Nominatim Search: Bergen")
            
            # Reverse geocode Stolmen coordinates
            reverse_data = nominatim_api.reverse(lat_stolmen, lon_stolmen)
            self.save_outputs(reverse_data, "nominatim_reverse_bergen", "Nominatim Reverse: Bergen")
            
            print("  ✓ Nominatim data collected\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        print("=" * 80)
        print("Data collection complete!".center(80))
        print(f"Outputs saved to: {os.path.abspath(self.output_dir)}".center(80))
        print("=" * 80 + "\n")


def main():
    """Main entry point"""
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    collector = WeatherDataCollector()
    collector.fetch_all()


if __name__ == "__main__":
    main()
