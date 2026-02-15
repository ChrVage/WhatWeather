"""
Plain Text Formatter - Convert API response data to readable plain text format
"""

from datetime import datetime
import json


class TextFormatter:
    """Format API responses as plain text"""
    
    @staticmethod
    def format(data, title="API Response"):
        """
        Convert data to plain text format
        
        Args:
            data: Dictionary containing API response
            title: Title for the output
        
        Returns:
            str: Plain text formatted string
        """
        lines = []
        lines.append("=" * 80)
        lines.append(title.center(80))
        lines.append("=" * 80)
        lines.append("")
        
        # Add metadata if available
        if '_metadata' in data:
            lines.append("METADATA")
            lines.append("-" * 80)
            metadata = data['_metadata']
            for key, value in metadata.items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        
        # Check for errors
        if 'error' in data:
            lines.append("ERROR")
            lines.append("-" * 80)
            lines.append(f"  {data['error']}")
            lines.append("")
        
        # Add full data as formatted JSON
        lines.append("FULL RESPONSE DATA")
        lines.append("-" * 80)
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        lines.append(json_str)
        lines.append("")
        
        # Add timestamp
        lines.append("-" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        
        return "\n".join(lines)


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
    
    formatter = TextFormatter()
    text_output = formatter.format(test_data, "Test API Response")
    print(text_output)
