"""Core Extraction Algorithms Module"""

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

from src.core.extractors.pdfextractor.content_processor import ContentProcessor
from src.core.extractors.pdfextractor.pdf_reader import PDFReader
from src.utils.decorators import log_execution, timing


class ExtractionEngine:  # Composition and Encapsulation
    """Core extraction engine coordinating reader and processor."""

    def __init__(self, pdf_path: Path):
        """Initialize extraction engine with components."""
        self.__pdf_reader = PDFReader(pdf_path)  # Private composition
        self.__content_processor = ContentProcessor()  # Private composition
        self.__extraction_modes = {  # Private mode mapping
            "fast": self.__extract_fast_mode,
            "standard": self.__extract_standard_mode,
            "comprehensive": self.__extract_comprehensive_mode,
        }

    def __str__(self) -> str:  # Magic method
        """String representation."""
        return f"ExtractionEngine({self.__pdf_reader.pdf_name})"

    def __repr__(self) -> str:  # Magic method
        """Detailed representation."""
        return f"ExtractionEngine(pdf_path={self.__pdf_reader.pdf_path!r})"

    def __call__(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Make engine callable."""
        return self.extract_content(max_pages)

    def __len__(self) -> int:  # Magic method
        """Return number of extracted items."""
        return len(self.extract_content())

    def __eq__(self, other: object) -> bool:  # Magic method
        """Compare engines by PDF path."""
        if not isinstance(other, ExtractionEngine):
            return False
        return self.__pdf_reader.pdf_path == other.__pdf_reader.pdf_path

    def __hash__(self) -> int:  # Magic method
        """Hash based on PDF path."""
        return hash(self.__pdf_reader.pdf_path)

    @property
    def pdf_path(self) -> Path:  # Encapsulation
        """Get PDF path (read-only)."""
        return self.__pdf_reader.pdf_path

    @property
    def extraction_stats(self) -> dict[str, int]:  # Encapsulation
        """Get extraction statistics (read-only)."""
        return self.__content_processor.stats

    @property
    def processing_mode(self) -> str:  # Encapsulation
        """Get processing mode."""
        return self.__content_processor.processing_mode

    @processing_mode.setter
    def processing_mode(self, mode: str) -> None:
        """Set processing mode."""
        self.__content_processor.processing_mode = mode

    @timing
    @log_execution
    def extract_content(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Extract content using current mode."""
        return list(self.extract_structured_content(max_pages))

    def extract_structured_content(
        self, max_pages: Optional[int] = None
    ) -> Iterator[dict[str, Any]]:
        """Extract structured content from PDF."""
        try:
            with self.__pdf_reader:
                total_pages = self.__pdf_reader.calculate_pages_to_process(
                    max_pages
                )
                extraction_method = self.__get_extraction_method()
                yield from extraction_method(total_pages)
        finally:
            self.__pdf_reader.close_document()

    def __get_extraction_method(self) -> Any:
        """Get extraction method based on mode."""
        mode = self.__content_processor.processing_mode
        return self.__extraction_modes.get(mode, self.__extract_standard_mode)

    def __extract_fast_mode(
        self, total_pages: int
    ) -> Iterator[dict[str, Any]]:
        """Fast extraction mode - basic processing."""
        for page_num in range(0, total_pages, 2):  # Skip every other page
            yield from self.__extract_page_content(page_num)

    def __extract_standard_mode(
        self, total_pages: int
    ) -> Iterator[dict[str, Any]]:
        """Standard extraction mode - normal processing."""
        for page_num in range(total_pages):
            yield from self.__extract_page_content(page_num)

    def __extract_comprehensive_mode(
        self, total_pages: int
    ) -> Iterator[dict[str, Any]]:
        """Comprehensive extraction mode - includes tables."""
        for page_num in range(total_pages):
            yield from self.__extract_page_content(page_num)
            yield from self.__extract_page_tables(page_num)

    def __extract_page_content(
        self, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Extract content from a single page."""
        for block_data in self.__pdf_reader.extract_page_blocks(page_num):
            content_item = self.__content_processor.process_block_data(
                block_data
            )
            if content_item:
                yield content_item

    def __extract_page_tables(self, page_num: int) -> Iterator[dict[str, Any]]:
        """Extract tables from a page."""
        try:
            # Table extraction would be implemented here
            # For now, return empty iterator
            return iter([])
        except Exception:
            return iter([])

    def extract_fast(self) -> list[dict[str, Any]]:  # Polymorphism
        """Fast extraction mode."""
        old_mode = self.processing_mode
        self.processing_mode = "fast"
        result = self.extract_content()
        self.processing_mode = old_mode
        return result

    def extract_comprehensive(self) -> list[dict[str, Any]]:  # Polymorphism
        """Comprehensive extraction mode."""
        old_mode = self.processing_mode
        self.processing_mode = "comprehensive"
        result = self.extract_content()
        self.processing_mode = old_mode
        return result

    def reset_stats(self) -> None:
        """Reset extraction statistics."""
        self.__content_processor.reset_stats()

    def clear_cache(self) -> None:
        """Clear all caches."""
        self.__pdf_reader.clear_cache()
