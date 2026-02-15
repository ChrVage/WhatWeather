"""
HTML Formatter - Convert API response data to HTML format
"""

from datetime import datetime
import json


class HTMLFormatter:
    """Format API responses as HTML"""
    
    @staticmethod
    def format(data, title="API Response"):
        """
        Convert data to HTML format
        
        Args:
            data: Dictionary containing API response
            title: Title for the HTML page
        
        Returns:
            str: HTML formatted string
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .metadata p {{
            margin: 5px 0;
            color: #555;
        }}
        .json-display {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
        }}
        .error {{
            background-color: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
"""
        
        # Add metadata if available
        if '_metadata' in data:
            metadata = data['_metadata']
            html += """
        <div class="metadata">
            <h2>Metadata</h2>
"""
            for key, value in metadata.items():
                html += f"            <p><strong>{key}:</strong> {value}</p>\n"
            html += "        </div>\n"
        
        # Check for errors
        if 'error' in data:
            html += f"""
        <div class="error">
            <h2>Error</h2>
            <p>{data['error']}</p>
        </div>
"""
        
        # Add JSON display
        html += """
        <h2>Full Response Data</h2>
        <div class="json-display">
"""
        # Pretty print JSON
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        # Escape HTML
        json_str = json_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html += f"<pre>{json_str}</pre>"
        
        html += """
        </div>
        <p class="timestamp">Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
</body>
</html>
"""
        
        return html


if __name__ == "__main__":
    # Test the formatter
    test_data = {
        '_metadata': {
            'api': 'Test API',
            'fetched_at': datetime.now().isoformat()
        },
        'test': 'value',
        'nested': {'key': 'value'}
    }
    
    formatter = HTMLFormatter()
    html = formatter.format(test_data, "Test API Response")
    print(html[:200] + "...")
