"""Extraction strategies with polymorphism."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional, Type, Dict

# Constants
DOC_TITLE = "USB PD Specification"


class ExtractionStrategy(ABC):
    """Abstract extraction strategy."""

    @abstractmethod
    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Extract content using specific strategy."""

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get strategy name."""

    def __call__(
        self, pdf_path: Path, max_pages: Optional[int] = None
    ) -> Iterator[dict[str, Any]]:
        """Make strategy callable."""
        return self.extract_pages(pdf_path, max_pages)

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}()"


class ComprehensiveStrategy(ExtractionStrategy):
    """Strategy for maximum page coverage."""

    def get_strategy_name(self) -> str:  # Polymorphism
        """Get strategy name."""
        return "comprehensive"

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
                                "doc_title": DOC_TITLE,
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
            str(span["text"])
            for line in block["lines"]
            for span in line["spans"]
        )


class StandardStrategy(ExtractionStrategy):
    """Standard extraction strategy."""

    def get_strategy_name(self) -> str:  # Polymorphism
        """Get strategy name."""
        return "standard"

    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Extract pages using standard PDF extractor."""
        from src.core.extractors.pdfextractor.pdf_extractor import (
            PDFExtractor,
        )

        extractor = PDFExtractor(pdf_path)
        yield from extractor.extract_structured_content(max_pages)


class FastStrategy(ExtractionStrategy):
    """Fast extraction strategy with minimal processing."""

    def get_strategy_name(self) -> str:  # Polymorphism
        """Get strategy name."""
        return "fast"

    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Fast extraction - text only, no detailed processing."""
        import fitz

        doc = fitz.open(str(pdf_path))
        try:
            doc_len = len(doc)
            total_pages = doc_len if max_pages is None else min(max_pages, doc_len)
            for page_num in range(total_pages):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    yield {
                        "doc_title": DOC_TITLE,
                        "section_id": f"fast_{page_num + 1}",
                        "title": text[:30],
                        "content": text.strip(),
                        "page": page_num + 1,
                        "level": 1,
                        "parent_id": None,
                        "full_path": text[:30],
                        "type": "text",
                        "block_id": f"fast_{page_num + 1}",
                        "bbox": [],
                    }
        finally:
            doc.close()


class DetailedStrategy(ExtractionStrategy):
    """Detailed extraction with enhanced metadata."""

    def get_strategy_name(self) -> str:  # Polymorphism
        """Get strategy name."""
        return "detailed"

    def extract_pages(
        self, pdf_path: Path, max_pages: Optional[int]
    ) -> Iterator[dict[str, Any]]:
        """Detailed extraction with font and formatting info."""
        import fitz

        doc = fitz.open(str(pdf_path))
        try:
            doc_len = len(doc)
            total_pages = doc_len if max_pages is None else min(max_pages, doc_len)
            for page_num in range(total_pages):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                for block_num, block in enumerate(blocks):
                    if "lines" in block and block["lines"]:
                        text = self._get_detailed_text(block)
                        if text.strip():
                            yield {
                                "doc_title": DOC_TITLE,
                                "section_id": f"det_{page_num + 1}_{block_num}",
                                "title": text[:40],
                                "content": text.strip(),
                                "page": page_num + 1,
                                "level": 1,
                                "parent_id": None,
                                "full_path": text[:40],
                                "type": "detailed",
                                "block_id": f"det_{page_num + 1}_{block_num}",
                                "bbox": list(block.get("bbox", [])),
                            }
        finally:
            doc.close()

    def _get_detailed_text(self, block: dict[str, Any]) -> str:
        """Extract text with detailed formatting."""
        return "".join(
            str(span["text"])
            for line in block["lines"]
            for span in line["spans"]
        )


class StrategyFactory:  # Factory for polymorphism
    """Factory to create extraction strategies."""
    
    @staticmethod
    def create(strategy_type: str) -> ExtractionStrategy:
        """Create strategy - runtime polymorphism."""
        strategies: Dict[str, Type[ExtractionStrategy]] = {
            "comprehensive": ComprehensiveStrategy,
            "standard": StandardStrategy,
            "fast": FastStrategy,
            "detailed": DetailedStrategy
        }
        if strategy_type not in strategies:
            raise ValueError(f"Unknown strategy: {strategy_type}")
        return strategies[strategy_type]()
