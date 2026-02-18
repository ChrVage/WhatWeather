"""
Quick test script for Kartverket Tide API
Usage: python quick_test_tide.py
"""

from kartverket_tide import KartverketTideAPI
from datetime import datetime


def main():
    """Run a quick tide API test"""
    
    print("\n🌊 QUICK KARTVERKET TIDE API TEST\n")
    
    # Initialize API
    api = KartverketTideAPI()
    
    # Display available stations
    print("📍 Available stations:")
    for name, code in api.STATIONS.items():
        print(f"   • {name.capitalize()}")
    print()
    
    # Test with Bergen
    print("🧪 Testing with Bergen station (3-day forecast)...")
    print("-" * 60)
    
    data = api.fetch(station='bergen', days_ahead=3)
    
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    # Display results
    metadata = data.get('_metadata', {})
    print(f"\n✅ Success!")
    print(f"📍 Location: {metadata.get('location', 'N/A')}")
    print(f"🕒 Fetched: {metadata.get('fetched_at', 'N/A')[:19]}")
    print(f"📊 Forecast period: {metadata.get('forecast_period_days', 'N/A')} days")
    
    # Get station info
    meta = data.get('properties', {}).get('meta', {})
    print(f"🏷️  Station: {meta.get('station_name', 'N/A')}")
    
    # Get timeseries
    timeseries = data.get('properties', {}).get('timeseries', [])
    print(f"\n📈 Total data points: {len(timeseries)}")
    
    if timeseries:
        print(f"\n🌊 SAMPLE TIDE HEIGHTS (Next 12 hours):")
        print(f"\n{'Time':^25} {'Height (cm)':>15}")
        print("-" * 45)
        
        # Show first 12 hours
        for i, entry in enumerate(timeseries[:12]):
            time_str = entry.get('time', 'N/A')
            height = entry.get('data', {}).get('instant', {}).get('details', {}).get(
                'sea_surface_height_above_chart_datum', 'N/A')
            
            # Format time
            try:
                dt = datetime.fromisoformat(time_str.replace('+00:00', ''))
                time_display = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_display = time_str
            
            print(f"{time_display:^25} {height:>15}")
    
    print("\n" + "=" * 60)
    print("✨ Test complete!")
    print("\nTo test other locations, modify the script or use test_tide.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
