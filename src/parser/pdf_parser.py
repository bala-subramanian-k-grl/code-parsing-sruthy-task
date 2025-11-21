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

    @property
    def title_length(self) -> int:
        """Get title length."""
        return len(self.__doc_title)

    @property
    def has_title(self) -> bool:
        """Check if has title."""
        return bool(self.__doc_title)

    @property
    def title_words(self) -> int:
        """Get title word count."""
        return len(self.__doc_title.split())

    @property
    def title_chars(self) -> int:
        """Get title character count."""
        return len(self.__doc_title)

    @property
    def title_upper(self) -> str:
        """Get title in uppercase."""
        return self.__doc_title.upper()

    def parse(self) -> ParserResult:
        """Parse PDF and extract TOC + content."""
        toc_entries = TOCExtractor(self._file_path).extract()

        try:
            with fitz.open(str(self._file_path)) as doc:  # type: ignore
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
        return f"PDFParser(file={self._file_path.name}, title={self.__doc_title})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"PDFParser(file_path={self._file_path!r}, doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PDFParser):
            return NotImplemented
        return self._file_path == other._file_path and self.__doc_title == other.__doc_title

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._file_path, self.__doc_title))

    def __len__(self) -> int:
        return len(self.__doc_title)

    def __bool__(self) -> bool:
        return self._file_path.exists()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PDFParser):
            return NotImplemented
        return (str(self._file_path), self.__doc_title) < (str(other._file_path), other.__doc_title)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __getitem__(self, index: int) -> str:
        """Get character from doc title."""
        return self.__doc_title[index]

    def __contains__(self, text: str) -> bool:
        """Check if text in file path or doc title."""
        return text in str(self._file_path) or text in self.__doc_title
