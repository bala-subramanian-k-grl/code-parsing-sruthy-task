"""PDF parser implementation."""

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

    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self.__doc_title

    def parse(self) -> ParserResult:
        """Parse PDF and extract TOC + content."""
        toc_entries = TOCExtractor(self.file_path).extract()

        try:
            with fitz.open(str(self.file_path)) as doc:  # type: ignore
                content_items = ContentExtractor(
                    self.__doc_title
                ).extract(doc)
        except Exception as e:
            raise ValueError(
                f"Failed to extract content from PDF: {e}"
            ) from e

        return ParserResult(
            toc_entries=toc_entries, content_items=content_items
        )

    def __str__(self) -> str:
        """String representation."""
        return f"PDFParser(file={self.file_path.name}, title={self.__doc_title})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"PDFParser(file_path={self.file_path!r}, doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, PDFParser):
            return NotImplemented
        return (
            self.file_path == other.file_path
            and self.__doc_title == other.__doc_title
        )

    def __hash__(self) -> int:
        """Hash for set/dict usage."""
        return hash((type(self).__name__, self.file_path, self.__doc_title))
