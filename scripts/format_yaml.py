"""
YAML Formatter - Convert API response data to YAML format
"""

import yaml
from datetime import datetime


class YAMLFormatter:
    """Format API responses as YAML"""
    
    @staticmethod
    def format(data):
        """
        Convert data to YAML format
        
        Args:
            data: Dictionary containing API response
        
        Returns:
            str: YAML formatted string
        """
        # Add generation timestamp
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'data': data
        }
        
        # Convert to YAML with nice formatting
        yaml_str = yaml.dump(
            output_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2
        )
        
        return yaml_str


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
    
    formatter = YAMLFormatter()
    yaml_output = formatter.format(test_data)
    print(yaml_output)
