"""
Table extraction pipeline with enhanced OOP design and error handling.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from src.extractors.table_extractor import TableExtractionError, TableExtractor
from src.utils.logger import logger
from src.writers.table_writer import TableWriter, WriterError


class PipelineError(Exception):
    """Custom exception for pipeline errors."""
    pass


class TableExtractionPipeline:
    """Extract tables from PDF with comprehensive error handling and validation."""

    def __init__(self, doc_title: str, output_dir: Path, pdf_path: Path) -> None:
        """Initialize pipeline with validation."""
        self._doc_title = self._validate_doc_title(doc_title)
        self._output_dir = self._validate_output_dir(output_dir)
        self._pdf_path = self._validate_pdf_path(pdf_path)
        
        self._extractor: Optional[TableExtractor] = None
        self._writer: Optional[TableWriter] = None
        self._extraction_metadata: Optional[dict[str, Any]] = None

    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self._doc_title

    @property
    def output_dir(self) -> Path:
        """Get output directory."""
        return self._output_dir

    @property
    def pdf_path(self) -> Path:
        """Get PDF path."""
        return self._pdf_path

    @property
    def extraction_metadata(self) -> Optional[dict[str, Any]]:
        """Get extraction metadata."""
        return self._extraction_metadata

    def extract_and_save(self) -> dict[str, Any]:
        """Extract tables and save with comprehensive error handling."""
        try:
            logger.info(f"Starting table extraction pipeline for {self._pdf_path.name}")
            
            # Extract tables
            tables = self._extract_tables()
            
            if not tables:
                logger.warning(f"No tables found in {self._pdf_path.name}")
                return self._create_result_metadata(0, None)
            
            # Save tables
            output_path = self._save_tables(tables)
            
            # Collect metadata
            result = self._create_result_metadata(len(tables), output_path)
            logger.info(f"Pipeline completed successfully: {len(tables)} tables saved to {output_path.name}")
            
            return result
            
        except (TableExtractionError, WriterError) as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise PipelineError(f"Table extraction pipeline failed: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected pipeline error: {str(e)}")
            raise PipelineError(f"Unexpected error in pipeline: {str(e)}") from e

    def _extract_tables(self) -> list[dict[str, Any]]:
        """Extract tables using the table extractor."""
        self._extractor = TableExtractor()
        
        try:
            tables = self._extractor.extract(self._pdf_path)
            self._extraction_metadata = self._extractor.get_metadata()
            return tables
        except Exception as e:
            raise TableExtractionError(f"Failed to extract tables: {str(e)}") from e

    def _save_tables(self, tables: list[dict[str, Any]]) -> Path:
        """Save tables using the table writer."""
        self._writer = TableWriter(self._doc_title)
        output_path = self._output_dir / f"{self._doc_title}_table.jsonl"
        
        try:
            self._writer.write_tables(tables, output_path)
            return output_path
        except Exception as e:
            raise WriterError(f"Failed to save tables: {str(e)}") from e

    def _create_result_metadata(self, table_count: int, output_path: Optional[Path]) -> dict[str, Any]:
        """Create result metadata."""
        return {
            "success": True,
            "doc_title": self._doc_title,
            "pdf_path": str(self._pdf_path),
            "output_path": str(output_path) if output_path else None,
            "tables_extracted": table_count,
            "extraction_metadata": self._extraction_metadata,
            "writer_metadata": self._writer.get_metadata() if self._writer else None
        }

    def _validate_doc_title(self, doc_title: str) -> str:
        """Validate document title."""
        if not doc_title or not doc_title.strip():
            raise ValueError("Document title cannot be empty")
        return doc_title.strip()

    def _validate_output_dir(self, output_dir: Path) -> Path:
        """Validate and prepare output directory."""
        if not isinstance(output_dir, Path):
            raise TypeError("Output directory must be a Path object")
        
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise PipelineError(f"Cannot create output directory {output_dir}: {str(e)}") from e
        
        return output_dir

    def _validate_pdf_path(self, pdf_path: Path) -> Path:
        """Validate PDF path."""
        if not isinstance(pdf_path, Path):
            raise TypeError("PDF path must be a Path object")
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.is_file():
            raise ValueError(f"PDF path is not a file: {pdf_path}")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        return pdf_path

    def validate_pipeline(self) -> bool:
        """Validate pipeline configuration."""
        try:
            self._validate_doc_title(self._doc_title)
            self._validate_output_dir(self._output_dir)
            self._validate_pdf_path(self._pdf_path)
            return True
        except Exception as e:
            logger.error(f"Pipeline validation failed: {str(e)}")
            return False
