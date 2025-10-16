"""PDF content extractor module."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

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

    def __str__(self) -> str:  # Public magic method
        return f"PDFExtractor({self.get_pdf_name()})"

    def __repr__(self) -> str:  # Public magic method
        return f"PDFExtractor(pdf_path={self.get_pdf_path()!r})"

    def get_pdf_name(self) -> str:  # Public method
        """Get PDF file name."""
        return self._pdf_path.name

    def get_pdf_path(self) -> Path:  # Public method
        """Get PDF file path."""
        return self._pdf_path

    def __call__(
        self, max_pages: Optional[int] = None
    ) -> list[dict[str, Any]]:
        return self.extract_content(max_pages)

    def __len__(self) -> int:  # Magic Method
        return len(self.extract())

    def extract(self) -> list[dict[str, Any]]:  # Polymorphism
        """Extract content from PDF."""
        return list(self.extract_structured_content())

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
            self._logger.warning("Error extracting page %s: %s", page_num, e)

    def _process_block(
        self, block: dict[str, Any], block_num: int, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Process individual block (Encapsulation)."""
        if "lines" not in block:
            return

        text = self._get_block_text(block)
        if not self._is_valid_text(text):
            return

        content_type = self.__analyzer.classify(text)  # Private access
        item_data = ContentItemData(
            text, content_type, block_num, page_num, block
        )
        yield self._create_content_item(item_data)

    def _is_valid_text(self, text: str) -> bool:
        """Check if text is valid for processing (Encapsulation)."""
        return bool(text.strip()) and len(text) > 5

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
        stripped = text.strip()
        return stripped[:50] + "..." if len(stripped) > 50 else stripped

    def _get_block_text(self, block: dict[str, Any]) -> str:
        """Extract text from block."""
        return "".join(
            str(span["text"])
            for line in block["lines"]
            for span in line["spans"]
        )

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
        table_text = "\n".join(
            " | ".join(str(cell or "") for cell in row) for row in table
        )
        return {
            "type": "table",
            "content": table_text,
            "page": page_num + 1,
            "block_id": f"tbl{page_num + 1}_{table_num}",
            "bbox": [],
        }
