#!/usr/bin/env python3
"""Run the table extraction pipeline with enhanced error handling."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.table_extraction_pipeline import TableExtractionPipeline, PipelineError
from utils.logger import logger


def main() -> int:
    """Run table extraction using enhanced pipeline."""
    try:
        # Configuration
        pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
        output_dir = Path("outputs")
        doc_title = "USB_PD_Spec"
        
        # Validate inputs
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            return 1
        
        # Initialize and run pipeline
        pipeline = TableExtractionPipeline(doc_title, output_dir, pdf_path)
        
        if not pipeline.validate_pipeline():
            logger.error("Pipeline validation failed")
            return 1
        
        result = pipeline.extract_and_save()
        
        # Display results
        print(f"✓ Extraction completed successfully!")
        print(f"  Document: {result['doc_title']}")
        print(f"  Tables extracted: {result['tables_extracted']}")
        if result['output_path']:
            print(f"  Output file: {result['output_path']}")
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"Error: {e}")
        return 1
    except PipelineError as e:
        logger.error(f"Pipeline error: {e}")
        print(f"Pipeline failed: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
