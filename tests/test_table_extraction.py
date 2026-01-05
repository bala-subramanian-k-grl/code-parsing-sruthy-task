"""Test script for table extraction."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.extractors.table_extractor import TableExtractor
from src.writers.table_writer import TableWriter
from src.support.table_extraction_pipeline import TableExtractionPipeline

def test_table_extraction():
    """Test table extraction from PDF."""
    # Find a PDF file in the workspace
    pdf_files = list(Path(__file__).parent.rglob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in workspace")
        return
    
    pdf_path = pdf_files[0]
    print(f"Testing with PDF: {pdf_path}")
    
    try:
        # Test direct extraction
        extractor = TableExtractor()
        tables = extractor.extract(pdf_path)
        print(f"Extracted {len(tables)} tables")
        
        if tables:
            print(f"First table page: {tables[0]['page']}")
            print(f"First table data sample: {tables[0]['data'][:2] if len(tables[0]['data']) > 0 else 'Empty'}")
        
        # Test pipeline
        output_dir = Path(__file__).parent / "output"
        pipeline = TableExtractionPipeline("test_doc", output_dir, pdf_path)
        pipeline.extract_and_save()
        
        # Check output
        output_file = output_dir / "test_doc_table.jsonl"
        if output_file.exists():
            print(f"Output file created: {output_file}")
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Output file has {len(lines)} lines")
        else:
            print("Output file not created")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_table_extraction()
