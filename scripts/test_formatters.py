#!/usr/bin/env python3
"""
Test script to verify all functionality works with mock data
"""

import os
import sys
from datetime import datetime

# Import configuration
from config import OUTPUT_DIR

# Import formatters
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from format_html import HTMLFormatter
from format_excel import ExcelFormatter
from format_yaml import YAMLFormatter
from format_text import TextFormatter


def create_mock_data(api_name):
    """Create mock API response data"""
    return {
        '_metadata': {
            'fetched_at': datetime.now().isoformat(),
            'coordinates': {'lat': 60.39, 'lon': 5.32},
            'api': api_name
        },
        'properties': {
            'meta': {
                'updated_at': datetime.now().isoformat(),
                'units': {
                    'air_temperature': 'celsius',
                    'precipitation_amount': 'mm'
                }
            },
            'timeseries': [
                {
                    'time': datetime.now().isoformat(),
                    'data': {
                        'instant': {
                            'details': {
                                'air_temperature': 12.5,
                                'wind_speed': 5.2,
                                'precipitation_amount': 0.0
                            }
                        }
                    }
                }
            ]
        }
    }


def test_formatters():
    """Test all formatters with mock data"""
    print("\n" + "=" * 80)
    print("Testing Weather Data Formatters".center(80))
    print("=" * 80 + "\n")
    
    # Create output directories
    output_dir = OUTPUT_DIR
    for subdir in ['html', 'excel', 'yaml', 'txt']:
        path = os.path.join(output_dir, subdir)
        os.makedirs(path, exist_ok=True)
    
    # Initialize formatters
    html_formatter = HTMLFormatter()
    excel_formatter = ExcelFormatter()
    yaml_formatter = YAMLFormatter()
    text_formatter = TextFormatter()
    
    # Test data
    test_apis = [
        ('oceanforecast', 'MET Norway Oceanforecast 2.0'),
        ('locationforecast', 'MET Norway Locationforecast 2.0'),
        ('textforecast', 'MET Norway Textforecast 2.0'),
        ('nowcast', 'MET Norway Nowcast 2.0')
    ]
    
    for api_name, title in test_apis:
        print(f"Testing {title}...")
        data = create_mock_data(title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{api_name}_test_{timestamp}"
        
        # HTML
        html_content = html_formatter.format(data, title)
        html_path = os.path.join(output_dir, 'html', f"{base_name}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  ✓ HTML: {html_path}")
        
        # Excel
        excel_path = os.path.join(output_dir, 'excel', f"{base_name}.xlsx")
        excel_formatter.format(data, excel_path, title)
        print(f"  ✓ Excel: {excel_path}")
        
        # YAML
        yaml_content = yaml_formatter.format(data)
        yaml_path = os.path.join(output_dir, 'yaml', f"{base_name}.yaml")
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"  ✓ YAML: {yaml_path}")
        
        # Plain Text
        text_content = text_formatter.format(data, title)
        text_path = os.path.join(output_dir, 'txt', f"{base_name}.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"  ✓ Text: {text_path}\n")
    
    print("=" * 80)
    print("All formatters tested successfully!".center(80))
    print(f"Outputs saved to: {os.path.abspath(output_dir)}".center(80))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    test_formatters()
