"""
Table extraction using pdfplumber with enhanced OOP design.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pdfplumber

from src.extractors.extractor_interface import ExtractorInterface
from src.utils.logger import logger


class TableExtractionError(Exception):
    """Custom exception for table extraction errors."""
    pass


class TableExtractor(ExtractorInterface):
    """Extract tables from PDFs using pdfplumber with enhanced error handling."""

    def __init__(self) -> None:
        """Initialize table extractor."""
        self._table_count: int = 0
        self._last_extraction_path: Path | None = None

    @property
    def extractor_type(self) -> str:
        """Return extractor type."""
        return "table"

    @property
    def is_stateful(self) -> bool:
        """Return statefulness."""
        return True

    @property
    def table_count(self) -> int:
        """Get number of extracted tables."""
        return self._table_count

    def extract(self, data: str | Path) -> list[dict[str, Any]]:
        """Extract tables from PDF with comprehensive error handling."""
        pdf_path = Path(data)
        self._last_extraction_path = pdf_path

        self._validate_input(pdf_path)

        try:
            return self._extract_tables_from_pdf(pdf_path)
        except Exception as e:
            logger.error(f"Table extraction failed for {pdf_path}: {str(e)}")
            raise TableExtractionError(f"Failed to extract tables: {str(e)}") from e

    def _validate_input(self, pdf_path: Path) -> None:
        """Validate input PDF file."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.is_file():
            raise ValueError(f"Path is not a file: {pdf_path}")

        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")

    def _extract_tables_from_pdf(self, pdf_path: Path) -> list[dict[str, Any]]:
        """Extract tables from PDF file."""
        tables: list[dict[str, Any]] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = self._extract_page_tables(page, page_num)
                    tables.extend(page_tables)

            self._table_count = len(tables)
            logger.info(f"Successfully extracted {len(tables)} tables from {pdf_path.name}")
            return tables

        except PermissionError:
            raise TableExtractionError(f"Permission denied accessing PDF: {pdf_path}")
        except Exception as e:
            raise TableExtractionError(f"PDF processing error: {str(e)}") from e

    def _extract_page_tables(self, page: Any, page_num: int) -> list[dict[str, Any]]:
        """Extract tables from a single page."""
        page_tables = []

        try:
            extracted_tables = page.extract_tables()
            if extracted_tables:
                for table_idx, table in enumerate(extracted_tables):
                    if table and self._is_valid_table(table):
                        page_tables.append({
                            "page": page_num,
                            "table_index": table_idx,
                            "data": table,
                            "row_count": len(table),
                            "column_count": len(table[0]) if table else 0
                        })
        except Exception as e:
            logger.warning(f"Failed to extract tables from page {page_num}: {str(e)}")

        return page_tables

    def _is_valid_table(self, table: list[list[Any]]) -> bool:
        """Validate if extracted table is meaningful."""
        if not table or len(table) < 2:  # At least header + 1 row
            return False

        # Check if table has consistent column count
        first_row_cols = len(table[0]) if table[0] else 0
        if first_row_cols < 2:  # At least 2 columns
            return False

        return True

    def validate(self) -> None:
        """Validate extractor state."""
        if self._last_extraction_path and not self._last_extraction_path.exists():
            raise TableExtractionError("Last processed file no longer exists")

    def get_metadata(self) -> dict[str, Any]:
        """Return extraction metadata."""
        return {
            "type": self.extractor_type,
            "tables_extracted": self._table_count,
            "last_file": str(self._last_extraction_path) if self._last_extraction_path else None,
            "is_stateful": self.is_stateful
        }

    def priority(self) -> int:
        """Return extraction priority."""
        return 15

    def reset(self) -> None:
        """Reset extractor state."""
        self._table_count = 0
        self._last_extraction_path = None
