"""
Simple test script for Kartverket Tide API
Usage: python test_tide.py
"""

from kartverket_tide import KartverketTideAPI
from datetime import datetime
import json


def print_separator():
    print("=" * 70)


def display_tide_data(data, station_name):
    """Display tide data in a readable format"""
    print_separator()
    print(f"TIDE DATA FOR: {station_name}")
    print_separator()
    
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    # Display metadata
    metadata = data.get('_metadata', {})
    print(f"\n📍 Location: {metadata.get('location', 'N/A')}")
    print(f"🕒 Fetched at: {metadata.get('fetched_at', 'N/A')}")
    print(f"📊 Forecast period: {metadata.get('forecast_period_days', 'N/A')} days")
    
    # Display station info
    meta = data.get('properties', {}).get('meta', {})
    print(f"🏷️  Station: {meta.get('station_name', 'N/A')}")
    
    # Display sample of timeseries data
    timeseries = data.get('properties', {}).get('timeseries', [])
    print(f"\n📈 Total data points: {len(timeseries)}")
    
    if timeseries:
        print(f"\n🌊 TIDE HEIGHTS (First 24 hours):\n")
        print(f"{'Time':^25} {'Height (cm)':>15}")
        print("-" * 45)
        
        # Show first 24 entries (hourly data)
        for entry in timeseries[:24]:
            time_str = entry.get('time', 'N/A')
            height = entry.get('data', {}).get('instant', {}).get('details', {}).get(
                'sea_surface_height_above_chart_datum', 'N/A')
            
            # Format time for display
            try:
                dt = datetime.fromisoformat(time_str.replace('+00:00', ''))
                time_display = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_display = time_str
            
            print(f"{time_display:^25} {height:>15}")
    
    print("\n")


def main():
    """Run tide API tests"""
    
    print("\n🌊 KARTVERKET TIDE API TEST SCRIPT 🌊\n")
    
    # Initialize API
    api = KartverketTideAPI()
    
    # Display available stations
    print("📍 Available stations:")
    for name, code in api.STATIONS.items():
        print(f"   • {name.capitalize():15} (code: {code})")
    
    print("\n")
    print_separator()
    
    # Test 1: Bergen station
    print("\n🧪 TEST 1: Fetching tide data for Bergen...")
    bergen_data = api.fetch(station='bergen', days_ahead=3)
    display_tide_data(bergen_data, "Bergen")
    
    # Test 2: Oslo station
    print("\n🧪 TEST 2: Fetching tide data for Oslo...")
    oslo_data = api.fetch(station='oslo', days_ahead=3)
    display_tide_data(oslo_data, "Oslo")
    
    # Test 3: Custom coordinates (Stavanger area)
    print("\n🧪 TEST 3: Fetching tide data for custom coordinates (Stavanger)...")
    custom_data = api.fetch(lat=58.97, lon=5.73, days_ahead=2)
    display_tide_data(custom_data, "Stavanger (Custom Coordinates)")
    
    # Optional: Save full data to JSON file
    print_separator()
    save = input("\n💾 Do you want to save the full Bergen data to a JSON file? (y/n): ")
    
    if save.lower() == 'y':
        filename = f"tide_data_bergen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bergen_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Data saved to: {filename}")
    
    print("\n✨ Testing complete!\n")


if __name__ == "__main__":
    main()
