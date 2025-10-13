
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

from src.core.analyzer.content_analyzer import ContentAnalyzer
from src.core.extractors.pdfextractor.base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):  # Inheritance
    """Fast PDF content extractor (Inheritance, Polymorphism)."""

    def __init__(self, pdf_path: Path):
        super().__init__(pdf_path)
        self._analyzer = ContentAnalyzer()  # Composition

    def extract(self) -> list[dict[str, Any]]:  # Polymorphism
        return list(self.extract_structured_content())

    def extract_content(self, max_pages: Optional[int] = None) -> list[dict[str, Any]]:
        return list(self.extract_structured_content(max_pages))

    def _validate_path(self, path: Path) -> Path:  # Encapsulation
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        return path.resolve()  # Prevent path traversal

    def extract_structured_content(
        self, max_pages: Optional[int] = None
    ) -> Iterator[dict[str, Any]]:
        fitz = self._get_fitz()
        doc = fitz.open(str(self._pdf_path))  # type: ignore
        try:
            doc_length: int = len(doc)  # type: ignore
            total_pages = (
                doc_length if max_pages is None else min(max_pages, doc_length)
            )
            for page_num in range(total_pages):
                yield from self._extract_page_content(doc[page_num], page_num)
        finally:
            doc.close()  # type: ignore

    def _extract_page_content(
        self, page: Any, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Fast page content extraction (Encapsulation)."""
        try:
            blocks = page.get_text("dict")["blocks"]  # type: ignore
            for block_num, block in enumerate(blocks):
                yield from self._process_block(block, block_num, page_num)
        except Exception as e:
            self._logger.warning(f"Error extracting page {page_num}: {e}")

    def _process_block(self, block: dict[str, Any], block_num: int, page_num: int) -> Iterator[dict[str, Any]]:
        """Process individual block (Encapsulation)."""
        if "lines" not in block:
            return
        
        text = self._get_block_text(block)
        if not self._is_valid_text(text):
            return
        
        content_type = self._analyzer.classify(text)
        yield self._create_content_item(text, content_type, block_num, page_num, block)

    def _is_valid_text(self, text: str) -> bool:
        """Check if text is valid for processing (Encapsulation)."""
        return bool(text.strip()) and len(text) > 5

    def _create_content_item(self, text: str, content_type: str, block_num: int, page_num: int, block: dict[str, Any]) -> dict[str, Any]:
        """Create content item dictionary (Encapsulation)."""
        title = self._get_title(text)
        return {
            "doc_title": "USB PD Specification",
            "section_id": f"{content_type[0]}{page_num + 1}_{block_num}",
            "title": title,
            "content": text.strip(),
            "page": page_num + 1,
            "level": 1,
            "parent_id": None,
            "full_path": title,
            "type": content_type,
            "block_id": f"{content_type[0]}{page_num + 1}_{block_num}",
            "bbox": list(block.get("bbox", [])),
        }

    def _get_title(self, text: str) -> str:
        """Get title from text (Encapsulation)."""
        stripped = text.strip()
        return stripped[:50] + "..." if len(stripped) > 50 else stripped

    def _get_block_text(self, block: dict[str, Any]) -> str:  # Encapsulation
        return "".join(
            str(span["text"]) for line in block["lines"] for span in line["spans"]
        )

    def _extract_tables(
        self, plumber_doc: Any, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Extract tables using cached pdfplumber doc (Encapsulation)."""
        try:
            if page_num < len(plumber_doc.pages):
                plumber_page = plumber_doc.pages[page_num]
                tables = plumber_page.extract_tables()
                for table_num, table in enumerate(tables or []):
                    if table and len(table) > 1:
                        table_text = "\n".join(
                            " | ".join(str(cell or "") for cell in row) for row in table
                        )
                        yield {
                            "type": "table",
                            "content": table_text,
                            "page": page_num + 1,
                            "block_id": f"tbl{page_num + 1}_{table_num}",
                            "bbox": [],
                        }
        except Exception as e:
            self._logger.warning(f"Table extraction failed: {e}")
