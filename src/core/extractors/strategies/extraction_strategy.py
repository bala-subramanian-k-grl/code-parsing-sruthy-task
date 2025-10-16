"""Extractions strategy pattern for improved page coverage."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional


class ExtractionStrategy(ABC):
    """Abstract extraction strategy."""

    @abstractmethod
    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Extract content using specific strategy."""


class ComprehensiveStrategy(ExtractionStrategy):
    """Strategy for maximum page coverage."""

    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Extract all pages with comprehensive coverage."""
        import fitz

        doc = fitz.open(str(pdf_path))
        try:
            doc_len = len(doc)
            # Force full document processing for complete coverage
            total_pages = doc_len  # Always process all pages
            for page_num in range(total_pages):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                for block_num, block in enumerate(blocks):
                    if "lines" in block:
                        text = self._get_block_text(block)
                        if text.strip():
                            yield {
                                "doc_title": "USB PD Specification",
                                "section_id": f"p{page_num + 1}_{block_num}",
                                "title": text[:50],
                                "content": text.strip(),
                                "page": page_num + 1,
                                "level": 1,
                                "parent_id": None,
                                "full_path": text[:50],
                                "type": "paragraph",
                                "block_id": f"p{page_num + 1}_{block_num}",
                                "bbox": list(block.get("bbox", [])),
                            }
        finally:
            doc.close()

    def _get_block_text(self, block: dict[str, Any]) -> str:
        """Extract text from block."""
        return "".join(
            str(span["text"]) for line in block["lines"] for span in line["spans"]
        )


class StandardStrategy(ExtractionStrategy):
    """Standard extraction strategy."""

    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Extract pages using standard PDF extractor."""
        from src.core.extractors.pdfextractor.pdf_extractor import (
            PDFExtractor,
        )

        extractor = PDFExtractor(pdf_path)
        yield from extractor.extract_structured_content(max_pages)
