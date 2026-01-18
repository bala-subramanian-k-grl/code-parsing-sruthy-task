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
            raise TableExtractionError(
                f"Failed to extract tables: {str(e)}"
            ) from e

    def _validate_input(self, pdf_path: Path) -> None:
        """Validate input PDF file."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.is_file():
            raise ValueError(f"Path is not a file: {pdf_path}")

        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")

    def _extract_tables_from_pdf(
        self, pdf_path: Path
    ) -> list[dict[str, Any]]:
        """Extract tables from PDF file."""
        tables: list[dict[str, Any]] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = self._extract_page_tables(page, page_num)
                    tables.extend(page_tables)

            self._table_count = len(tables)
            logger.info(
                f"Successfully extracted {len(tables)} tables "
                f"from {pdf_path.name}"
            )
            return tables

        except PermissionError:
            raise TableExtractionError(
                f"Permission denied accessing PDF: {pdf_path}"
            )
        except Exception as e:
            raise TableExtractionError(
                f"PDF processing error: {str(e)}"
            ) from e

    def _extract_page_tables(
        self, page: Any, page_num: int
    ) -> list[dict[str, Any]]:
        """Extract tables from a single page."""
        page_tables: list[dict[str, Any]] = []

        try:
            tables = page.find_tables()

            for table_obj in tables:
                extracted = table_obj.extract()
                if (
                    extracted
                    and self._is_valid_table(extracted)
                    and not self._is_paragraph(extracted)
                ):
                    table_entry = self._create_table_entry(
                        page_num, len(page_tables), extracted
                    )
                    page_tables.append(table_entry)

        except Exception as e:
            logger.warning(
                f"Failed to extract tables from page {page_num}: {str(e)}"
            )

        return page_tables

    def _is_paragraph(self, table: list[list[Any]]) -> bool:
        """Detect if table is actually paragraph text."""
        if not table:
            return True

        # Count cells with long continuous text
        long_cells = 0
        total_cells = 0

        for row in table[:5]:
            for cell in row:
                if cell and str(cell).strip():
                    total_cells += 1
                    if len(str(cell).strip()) > 60:
                        long_cells += 1

        # If most cells are long text, it's a paragraph
        return total_cells > 0 and (long_cells / total_cells) > 0.5

    def _create_table_entry(
        self, page_num: int, table_idx: int, table: list[list[Any]]
    ) -> dict[str, Any]:
        """Create standardized table entry."""
        return {
            "page": page_num,
            "table_index": table_idx,
            "data": table,
            "row_count": len(table),
            "column_count": len(table[0]) if table else 0
        }



    def _is_valid_table(self, table: list[list[Any]]) -> bool:
        """Validate if extracted table is meaningful."""
        if not table or len(table) < 2:
            return False

        if not table[0] or len(table[0]) < 2:
            return False

        return True

    def validate(self) -> None:
        """Validate extractor state."""
        if (
            self._last_extraction_path
            and not self._last_extraction_path.exists()
        ):
            raise TableExtractionError(
                "Last processed file no longer exists"
            )

    def get_metadata(self) -> dict[str, Any]:
        """Return extraction metadata."""
        return {
            "type": self.extractor_type,
            "tables_extracted": self._table_count,
            "last_file": (
                str(self._last_extraction_path)
                if self._last_extraction_path else None
            ),
            "is_stateful": self.is_stateful
        }

    def priority(self) -> int:
        """Return extraction priority."""
        return 15

    def reset(self) -> None:
        """Reset extractor state."""
        self._table_count = 0
        self._last_extraction_path = None

    def __str__(self) -> str:
        """String representation."""
        return f"TableExtractor(tables={self._table_count})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"TableExtractor(table_count={self._table_count}, "
            f"last_file={self._last_extraction_path})"
        )

    def __len__(self) -> int:
        """Return number of extracted tables."""
        return self._table_count

    def __bool__(self) -> bool:
        """Return True if tables were extracted."""
        return self._table_count > 0

    def __eq__(self, other: object) -> bool:
        """Check equality based on type."""
        return isinstance(other, TableExtractor)

    def __hash__(self) -> int:
        """Hash based on class name."""
        return hash(self.__class__.__name__)

    def __call__(self, pdf_path: str | Path) -> list[dict[str, Any]]:
        """Make extractor callable."""
        return self.extract(pdf_path)
