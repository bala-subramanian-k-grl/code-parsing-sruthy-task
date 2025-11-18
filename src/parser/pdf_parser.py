"""PDF parser implementation."""

from pathlib import Path
from typing import Any

import fitz  # type: ignore[import-untyped]

from src.core.config.models import ContentItem, ParserResult, TOCEntry
from src.parser.base_parser import BaseParser
from src.parser.toc_extractor import TOCExtractor


class PDFParser(BaseParser):
    """Concrete PDF parser with full extraction."""

    def __init__(self, file_path: Path, doc_title: str = "Document") -> None:
        super().__init__(file_path)
        self._doc_title = doc_title

    def parse(self) -> ParserResult:
        """Parse PDF and extract TOC + content."""
        toc_entries = self._extract_toc()
        content_items = self._extract_content()
        return ParserResult(
            toc_entries=toc_entries, content_items=content_items
        )

    def _extract_toc(self) -> list[TOCEntry]:
        """Extract table of contents."""
        extractor = TOCExtractor(self._file_path)
        return extractor.extract()

    def _extract_content(self) -> list[ContentItem]:
        """Extract all content from PDF."""
        items: list[ContentItem] = []
        try:
            with fitz.open(str(self._file_path)) as doc:  # type: ignore
                for page_num, page in enumerate(doc, start=1):  # type: ignore
                    text_dict = page.get_text("dict")  # type: ignore
                    blocks = text_dict["blocks"]  # type: ignore
                    for block_num, block in enumerate(blocks):  # type: ignore
                        if "lines" not in block:
                            continue
                        text = self._extract_block_text(block)  # type: ignore
                        if len(text.strip()) < 1:
                            continue
                        items.append(
                            ContentItem(
                                doc_title=self._doc_title,
                                section_id=f"p{page_num}_{block_num}",
                                title=text[:100],
                                content=text,
                                page=page_num,
                                block_id=f"p{page_num}_{block_num}",
                                bbox=list(block.get("bbox", []))
                            )
                        )
        except Exception as e:
            raise ValueError(
                f"Failed to extract content from PDF: {e}"
            ) from e
        return items

    def _extract_block_text(self, block: dict[str, Any]) -> str:
        """Extract text from block."""
        lines: list[Any] = block.get("lines", [])  # type: ignore
        texts: list[str] = []
        for line in lines:  # type: ignore
            spans: list[Any] = line.get("spans", [])  # type: ignore
            for span in spans:  # type: ignore
                text = str(span.get("text", ""))  # type: ignore
                texts.append(text)
        return "".join(texts)
