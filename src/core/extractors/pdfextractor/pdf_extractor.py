"""PDF content extractor module - Modular Architecture."""

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

from src.core.extractors.pdfextractor.base_extractor import BaseExtractor
from src.core.extractors.pdfextractor.extraction_engine import ExtractionEngine
from src.utils.decorators import log_execution, timing


class PDFExtractor(BaseExtractor):  # Inheritance
    """Modular PDF content extractor using composition."""

    def __init__(self, pdf_path: Path):
        """Initialize with extraction engine composition."""
        super().__init__(pdf_path)
        self.__engine = ExtractionEngine(pdf_path)  # Private composition

    def __str__(self) -> str:  # Magic method
        """String representation."""
        return f"PDFExtractor({self.pdf_name})"

    def __repr__(self) -> str:  # Magic method
        """Detailed representation."""
        return f"PDFExtractor(pdf_path={self.pdf_path!r})"

    def __call__(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Make extractor callable."""
        return self.extract_content(max_pages)

    def __len__(self) -> int:  # Magic method
        """Return number of extracted items."""
        return len(self.extract())

    def __eq__(self, other: object) -> bool:  # Magic method
        """Compare extractors by PDF path."""
        if not isinstance(other, PDFExtractor):
            return False
        return self.pdf_path == other.pdf_path

    def __hash__(self) -> int:  # Magic method
        """Hash based on PDF path."""
        return hash(self.pdf_path)

    @property
    def pdf_path(self) -> Path:  # Encapsulation
        """Get PDF file path (read-only)."""
        return self._pdf_path

    @property
    def pdf_name(self) -> str:  # Encapsulation
        """Get PDF file name (read-only)."""
        return self._pdf_path.name

    @property
    def extraction_stats(self) -> dict[str, int]:  # Encapsulation
        """Get extraction statistics (read-only)."""
        return self.__engine.extraction_stats

    @property
    def processing_mode(self) -> str:  # Encapsulation
        """Get processing mode."""
        return self.__engine.processing_mode

    @processing_mode.setter
    def processing_mode(self, mode: str) -> None:
        """Set processing mode."""
        self.__engine.processing_mode = mode

    def extract(self) -> list[dict[str, Any]]:  # Polymorphism
        """Extract content from PDF."""
        return list(self.__extract_structured_content())

    def extract_fast(self) -> list[dict[str, Any]]:  # Polymorphism
        """Fast extraction mode."""
        return self.__engine.extract_fast()

    def extract_comprehensive(self) -> list[dict[str, Any]]:  # Polymorphism
        """Comprehensive extraction mode."""
        return self.__engine.extract_comprehensive()

    @timing
    @log_execution
    def extract_content(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Extract content using engine."""
        return self.__engine.extract_content(max_pages)

    def __extract_structured_content(
        self, max_pages: Optional[int] = None
    ) -> Iterator[dict[str, Any]]:  # Private - only used internally
        """Extract structured content using engine."""
        return self.__engine.extract_structured_content(max_pages)

    def reset_stats(self) -> None:
        """Reset extraction statistics."""
        self.__engine.reset_stats()

    def clear_cache(self) -> None:
        """Clear extraction cache."""
        self.__engine.clear_cache()
