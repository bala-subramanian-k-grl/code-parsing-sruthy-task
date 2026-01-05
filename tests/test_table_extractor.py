#!/usr/bin/env python3
"""Test script for TableExtractor."""

import sys

sys.path.append('.')

from src.extractors.table_extractor import TableExtractor


def main():
    """Test table extraction."""
    try:
        extractor = TableExtractor()
        
        # Use the same PDF that main.py processed
        pdf_path = "assets/USB_PD_R3_2 V1.1 2024-10.pdf"
        
        print(f"Testing {extractor.extractor_type}")
        print(f"Priority: {extractor.priority()}")
        print(f"Is stateful: {extractor.is_stateful}")
        
        # Extract tables
        tables = extractor.extract(pdf_path)
        
        print(f"\nExtracted {len(tables)} tables")
        
        # Show first few tables
        for i, table in enumerate(tables[:3]):
            print(f"\nTable {i+1} (Page {table['page']}):")
            data = table['data']
            if data and len(data) > 0:
                # Show first few rows
                for row_idx, row in enumerate(data[:3]):
                    print(f"  Row {row_idx+1}: {row}")
                if len(data) > 3:
                    print(f"  ... ({len(data)} total rows)")
        
        if len(tables) > 3:
            print(f"\n... ({len(tables)} total tables)")
        
        # Show metadata
        metadata = extractor.get_metadata()
        print(f"\nMetadata: {metadata}")
    except FileNotFoundError as e:
        print(f"Error: PDF file not found - {e}")
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    main()
