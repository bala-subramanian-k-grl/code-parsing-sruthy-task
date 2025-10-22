"""PDF content extractor module."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from src.config.constants import MAX_TITLE_LENGTH, MIN_TEXT_LENGTH
from src.core.analyzer.content_analyzer import ContentAnalyzer
from src.core.extractors.pdfextractor.base_extractor import BaseExtractor
from src.utils.decorators import log_execution, timing


@dataclass
class ContentItemData:
    """Data class for content item creation."""

    text: str
    content_type: str
    block_num: int
    page_num: int
    block: dict[str, Any]


class PDFExtractor(BaseExtractor):  # Inheritance
    """Fast PDF content extractor (Inheritance, Polymorphism)."""

    def __init__(self, pdf_path: Path):
        super().__init__(pdf_path)
        self.__analyzer = ContentAnalyzer()  # Private composition
        self.__page_cache: dict[int, Any] = {}  # Private cache
        self.__extraction_stats: dict[str, int] = {}  # Private stats
        self.__processing_mode: str = "standard"  # Private mode
    def __str__(self) -> str:  # Public magic method
        return f"PDFExtractor({self.pdf_name})"

    def __repr__(self) -> str:  # Public magic method
        return f"PDFExtractor(pdf_path={self.pdf_path!r})"

    @property
    def pdf_path(self) -> Path:
        """Get PDF file path (read-only)."""
        return self._pdf_path

    @property
    def pdf_name(self) -> str:
        """Get PDF file name (read-only)."""
        return self._pdf_path.name

    @property
    def extraction_stats(self) -> dict[str, int]:
        """Get extraction statistics (read-only)."""
        return self.__extraction_stats.copy()

    @property
    def processing_mode(self) -> str:
        """Get processing mode."""
        return self.__processing_mode

    @processing_mode.setter
    def processing_mode(self, mode: str) -> None:
        """Set processing mode with validation."""
        valid_modes = ["standard", "fast", "comprehensive"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}")
        self.__processing_mode = mode

    def __call__(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        return self.extract_content(max_pages)

    def __len__(self) -> int:  # Magic Method
        return len(self.extract())

    def __eq__(self, other: object) -> bool:  # Magic Method
        """Compare extractors by PDF path."""
        if not isinstance(other, PDFExtractor):
            return False
        return self.pdf_path == other.pdf_path

    def __hash__(self) -> int:  # Magic Method
        """Hash based on PDF path."""
        return hash(self.pdf_path)

    def extract(self) -> list[dict[str, Any]]:  # Polymorphism
        """Extract content from PDF."""
        return list(self.extract_structured_content())

    def extract_fast(self) -> list[dict[str, Any]]:  # Polymorphism
        """Fast extraction mode."""
        old_mode = self.__processing_mode
        self.__processing_mode = "fast"
        result = self.extract()
        self.__processing_mode = old_mode
        return result

    def extract_comprehensive(self) -> list[dict[str, Any]]:
        """Comprehensive extraction mode."""
        old_mode = self.__processing_mode
        self.__processing_mode = "comprehensive"
        result = self.extract()
        self.__processing_mode = old_mode
        return result

    @timing
    @log_execution
    def extract_content(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        return list(self.extract_structured_content(max_pages))

    def _validate_path(self, path: Path) -> Path:  # Encapsulation
        """Validate PDF path."""
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        return path.resolve()  # Prevent path traversal

    def extract_structured_content(
        self, max_pages: Optional[int] = None
    ) -> Iterator[dict[str, Any]]:
        fitz = self._get_fitz()
        doc = fitz.open(str(self._pdf_path))
        try:
            total_pages = self._calculate_total_pages(doc, max_pages)
            for page_num in range(total_pages):
                page = doc[page_num]
                yield from self._extract_page_content(page, page_num)
        finally:
            doc.close()

    def _calculate_total_pages(
        self, doc: Any, max_pages: Optional[int]
    ) -> int:
        """Calculate total pages to process."""
        doc_length = len(doc)
        return doc_length if max_pages is None else min(max_pages, doc_length)

    def _extract_page_content(
        self, page: Any, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Fast page content extraction (Encapsulation)."""
        try:
            blocks = page.get_text("dict")["blocks"]
            for block_num, block in enumerate(blocks):
                yield from self._process_block(block, block_num, page_num)
        except Exception as e:
            msg = "Error extracting page %s: %s"
            self._logger.warning(msg, page_num, e)

    def _process_block(
        self, block: dict[str, Any], block_num: int, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Process individual block (Encapsulation)."""
        if not self._should_process_block(block):
            return

        text = self._get_block_text(block)
        if not self._is_valid_text(text):
            return

        content_type = self.__analyzer.classify(text)  # Private access
        self._update_stats(content_type)  # Private method
        item_data = self._create_item_data(
            text, content_type, block_num, page_num, block
        )
        yield self._create_content_item(item_data)

    def _should_process_block(self, block: dict[str, Any]) -> bool:
        """Check if block should be processed."""
        return "lines" in block

    def _update_stats(self, content_type: str) -> None:
        """Update extraction statistics."""
        self.__extraction_stats[content_type] = (
            self.__extraction_stats.get(content_type, 0) + 1
        )

    def _create_item_data(
        self, text: str, content_type: str, block_num: int,
        page_num: int, block: dict[str, Any]
    ) -> ContentItemData:
        """Create content item data object."""
        return ContentItemData(text, content_type, block_num, page_num, block)

    def _is_valid_text(self, text: str) -> bool:
        """Check if text is valid for processing (Encapsulation)."""
        return bool(text.strip()) and len(text) > MIN_TEXT_LENGTH

    def _create_content_item(self, data: ContentItemData) -> dict[str, Any]:
        """Create content item dictionary (Encapsulation)."""
        title = self._get_title(data.text)
        prefix = data.content_type[0]
        page = data.page_num + 1
        section_id = f"{prefix}{page}_{data.block_num}"

        return {
            "doc_title": "USB PD Specification",
            "section_id": section_id,
            "title": title,
            "content": data.text.strip(),
            "page": data.page_num + 1,
            "level": 1,
            "parent_id": None,
            "full_path": title,
            "type": data.content_type,
            "block_id": section_id,
            "bbox": list(data.block.get("bbox", [])),
        }

    def _get_title(self, text: str) -> str:
        """Get title from text (Encapsulation)."""
        return self._truncate_text(text.strip(), MAX_TITLE_LENGTH)

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to maximum length."""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    def _reset_stats(self) -> None:
        """Reset extraction statistics."""
        self.__extraction_stats.clear()

    def _get_cache_key(self, page_num: int) -> str:
        """Generate cache key for page."""
        return f"page_{page_num}_{self.__processing_mode}"

    def _get_block_text(self, block: dict[str, Any]) -> str:
        """Extract text from block."""
        text_parts = [
            str(span["text"])
            for line in block["lines"]
            for span in line["spans"]
        ]
        return "".join(text_parts)

    def _extract_tables(
        self, plumber_doc: Any, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Extract tables from page."""
        try:
            if page_num >= len(plumber_doc.pages):
                return

            page = plumber_doc.pages[page_num]
            tables = page.extract_tables()

            for table_num, table in enumerate(tables or []):
                if self._is_valid_table(table):
                    data = self._create_table_data(table, page_num, table_num)
                    yield data
        except Exception as e:
            self._logger.warning("Table extraction failed: %s", e)

    def _is_valid_table(self, table: Any) -> bool:
        """Check if table is valid for processing."""
        return table and len(table) > 1

    def _create_table_data(
        self, table: Any, page_num: int, table_num: int
    ) -> dict[str, Any]:
        """Create table data dictionary."""
        table_text = self._format_table_text(table)
        return self._build_table_dict(table_text, page_num, table_num)

    def _format_table_text(self, table: Any) -> str:
        """Format table as text."""
        rows = [
            " | ".join(str(cell or "") for cell in row) for row in table
        ]
        return "\n".join(rows)

    def _build_table_dict(
        self, table_text: str, page_num: int, table_num: int
    ) -> dict[str, Any]:
        """Build table dictionary."""
        return {
            "type": "table",
            "content": table_text,
            "page": page_num + 1,
            "block_id": f"tbl{page_num + 1}_{table_num}",
            "bbox": [],
        }
