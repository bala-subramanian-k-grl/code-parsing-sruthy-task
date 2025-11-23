"""PDF parser implementation."""

from __future__ import annotations
from pathlib import Path
import fitz  # type: ignore[import-untyped]

from src.core.config.models import ParserResult
from src.extractors.content_extractor import ContentExtractor
from src.parser.base_parser import BaseParser
from src.parser.toc_extractor import TOCExtractor


class PDFParser(BaseParser):
    """Concrete PDF parser with full extraction."""

    def __init__(self, file_path: Path, doc_title: str = "Document") -> None:
        super().__init__(file_path)
        self.__doc_title = doc_title

    # ---------------------------------------------------------
    # Polymorphism
    # ---------------------------------------------------------
    @property
    def parser_type(self) -> str:
        """Polymorphic parser identifier."""
        return "PDF"

    def supports(self, extension: str) -> bool:
        """Polymorphic override for parser compatibility."""
        return extension.lower() == ".pdf"

    @property
    def is_binary(self) -> bool:
        """PDF is always a binary document."""
        return True

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------
    @property
    def doc_title(self) -> str:
        """Get the document title."""
        return self.__doc_title

    # ---------------------------------------------------------
    # Parsing Implementation
    # ---------------------------------------------------------
    def parse(self) -> ParserResult:
        """Parse PDF and extract TOC + content."""
        toc_entries = TOCExtractor(self.file_path).extract()

        try:
            with fitz.open(str(self.file_path)) as doc:  # type: ignore
                extractor = ContentExtractor(self.__doc_title)
                content_items = extractor.extract(doc)
        except Exception as e:
            raise ValueError(f"Failed to extract content from PDF: {e}") from e

        return ParserResult(
            toc_entries=toc_entries,
            content_items=content_items
        )

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"PDFParser(file={self.file_path.name}, "
            f"title={self.__doc_title})"
        )

    def __repr__(self) -> str:
        return (
            f"PDFParser(file_path={self.file_path!r}, "
            f"doc_title={self.__doc_title!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PDFParser):
            return NotImplemented
        return self.file_path == other.file_path and self.__doc_title == other.__doc_title

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.file_path, self.__doc_title))
