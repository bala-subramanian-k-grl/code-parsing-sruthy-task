"""PDF Reading Operations Module"""

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

from src.core.extractors.pdfextractor.base_extractor import BaseExtractor
from src.utils.decorators import log_execution


class PDFReader(BaseExtractor):  # Inheritance
    """Handles PDF reading operations with proper encapsulation."""

    def __init__(self, pdf_path: Path):
        """Initialize PDF reader with validation."""
        super().__init__(pdf_path)
        self.__document_cache: dict[str, Any] = {}  # Private cache
        self.__page_cache: dict[int, Any] = {}  # Private page cache

    def __enter__(self) -> "PDFReader":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit with cleanup."""
        self.clear_cache()

    @property
    def pdf_path(self) -> Path:  # Encapsulation
        """Get PDF file path (read-only)."""
        return self._pdf_path

    @property
    def pdf_name(self) -> str:  # Encapsulation
        """Get PDF file name (read-only)."""
        return self._pdf_path.name

    def clear_cache(self) -> None:
        """Clear all caches."""
        self.__document_cache.clear()
        self.__page_cache.clear()

    @log_execution
    def open_document(self) -> Any:
        """Open PDF document with caching."""
        cache_key = str(self._pdf_path)
        if cache_key not in self.__document_cache:
            fitz = self._get_fitz()
            self.__document_cache[cache_key] = fitz.open(str(self._pdf_path))
        return self.__document_cache[cache_key]

    def get_page_count(self) -> int:
        """Get total number of pages."""
        doc = self.open_document()
        return len(doc)

    def calculate_pages_to_process(self, max_pages: Optional[int]) -> int:
        """Calculate total pages to process."""
        total_pages = self.get_page_count()
        if max_pages is None:
            return total_pages
        return min(max_pages, total_pages)

    def get_page(self, page_num: int) -> Any:
        """Get page with caching."""
        if page_num not in self.__page_cache:
            doc = self.open_document()
            self.__page_cache[page_num] = doc[page_num]
        return self.__page_cache[page_num]

    def extract_page_blocks(self, page_num: int) -> Iterator[dict[str, Any]]:
        """Extract blocks from a page."""
        try:
            page = self.get_page(page_num)
            blocks = page.get_text("dict")["blocks"]
            for block_num, block in enumerate(blocks):
                if self.__should_process_block(block):
                    yield {
                        "block": block,
                        "block_num": block_num,
                        "page_num": page_num,
                    }
        except Exception as e:
            self._logger.warning("Error extracting page %s: %s", page_num, e)

    def __should_process_block(self, block: dict[str, Any]) -> bool:
        """Check if block should be processed."""
        return "lines" in block

    def extract(self) -> list[dict[str, Any]]:
        """Extract content - required by base class."""
        # This is a reader, actual extraction is done by engine
        return []

    def close_document(self) -> None:
        """Close document and clear cache."""
        for doc in self.__document_cache.values():
            if hasattr(doc, "close"):
                doc.close()
        self.clear_cache()
