"""
Excel Formatter - Convert API response data to Excel format
"""

from datetime import datetime
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


class ExcelFormatter:
    """Format API responses as Excel spreadsheets"""
    
    @staticmethod
    def format(data, filename, title="API Response"):
        """
        Convert data to Excel format and save to file
        
        Args:
            data: Dictionary containing API response
            filename: Path to save Excel file
            title: Title for the spreadsheet
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Response Data"
        
        # Title
        ws['A1'] = title
        ws['A1'].font = Font(size=16, bold=True, color="FFFFFF")
        ws['A1'].fill = PatternFill(start_color="3498DB", end_color="3498DB", fill_type="solid")
        ws.merge_cells('A1:B1')
        
        row = 3
        
        # Metadata section
        if '_metadata' in data:
            ws[f'A{row}'] = "Metadata"
            ws[f'A{row}'].font = Font(size=14, bold=True)
            ws[f'A{row}'].fill = PatternFill(start_color="ECF0F1", end_color="ECF0F1", fill_type="solid")
            ws.merge_cells(f'A{row}:B{row}')
            row += 1
            
            metadata = data['_metadata']
            for key, value in metadata.items():
                ws[f'A{row}'] = key
                ws[f'B{row}'] = str(value)
                ws[f'A{row}'].font = Font(bold=True)
                row += 1
            
            row += 1
        
        # Error section
        if 'error' in data:
            ws[f'A{row}'] = "Error"
            ws[f'A{row}'].font = Font(size=14, bold=True, color="FFFFFF")
            ws[f'A{row}'].fill = PatternFill(start_color="E74C3C", end_color="E74C3C", fill_type="solid")
            ws.merge_cells(f'A{row}:B{row}')
            row += 1
            
            ws[f'A{row}'] = "Error Message"
            ws[f'B{row}'] = data['error']
            ws[f'A{row}'].font = Font(bold=True)
            row += 1
            
            row += 1
        
        # Full data as JSON
        ws[f'A{row}'] = "Full Response (JSON)"
        ws[f'A{row}'].font = Font(size=14, bold=True)
        ws[f'A{row}'].fill = PatternFill(start_color="ECF0F1", end_color="ECF0F1", fill_type="solid")
        ws.merge_cells(f'A{row}:B{row}')
        row += 1
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        ws[f'A{row}'] = json_str
        ws[f'A{row}'].alignment = Alignment(wrap_text=True, vertical='top')
        ws.merge_cells(f'A{row}:B{row + 20}')
        
        # Adjust column widths
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 60
        
        # Save file
        wb.save(filename)
        return filename


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
    
    formatter = ExcelFormatter()
    filename = '/tmp/test_output.xlsx'
    formatter.format(test_data, filename, "Test API Response")
    print(f"Created test Excel file: {filename}")
