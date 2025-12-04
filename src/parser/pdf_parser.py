"""PDF parser implementation with full OOP, Overloading, Polymorphism."""

from __future__ import annotations

from pathlib import Path
from typing import Any, overload

import fitz  # type: ignore[import-untyped]

from src.core.config.models import ParserResult
from src.extractors.content_extractor import ContentExtractor
from src.parser.base_parser import BaseParser
from src.parser.toc_extractor import TOCExtractor


class PDFParser(BaseParser):
    """Concrete PDF parser (TOC + Content Extraction)."""

    # ---------------------------------------------------------
    # INIT (Encapsulation)
    # ---------------------------------------------------------
    def __init__(self, file_path: Path, doc_title: str = "Document") -> None:
        """Method implementation."""
        super().__init__(file_path)
        self.__doc_title = doc_title

    # ---------------------------------------------------------
    # Polymorphism (Override from BaseParser)
    # ---------------------------------------------------------
    @property
    def parser_type(self) -> str:
        """Method implementation."""
        return "PDF"

    def supports(self, extension: str) -> bool:
        """Override: PDF supports only .pdf."""
        return extension.lower() in {".pdf", "pdf"}

    @property
    def is_binary(self) -> bool:
        """PDF files are always binary."""
        return True

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------
    @property
    def doc_title(self) -> str:
        """Method implementation."""
        return self.__doc_title

    @doc_title.setter
    def doc_title(self, value: str) -> None:
        """Method implementation."""
        if not value.strip():
            raise ValueError("Document title cannot be empty.")
        self.__doc_title = value

    @property
    def title_length(self) -> int:
        """Method implementation."""
        return len(self.__doc_title)

    @property
    def title_words(self) -> int:
        """Method implementation."""
        return len(self.__doc_title.split())

    @property
    def title_upper(self) -> str:
        """Method implementation."""
        return self.__doc_title.upper()

    @property
    def title_lower(self) -> str:
        """Method implementation."""
        return self.__doc_title.lower()

    @property
    def has_title(self) -> bool:
        """Method implementation."""
        return bool(self.__doc_title.strip())

    @property
    def title_is_empty(self) -> bool:
        """Method implementation."""
        return not self.__doc_title.strip()

    # ---------------------------------------------------------
    #  OVERLOADED parse() for polymorphic usage
    # ---------------------------------------------------------
    @overload
    def parse(self) -> ParserResult: ...

    @overload
    def parse(self, *, include_toc: bool) -> ParserResult: ...

    def parse(self, *, include_toc: bool = True) -> ParserResult:
        """
        Overloaded method:
            parse()                        → TOC + content
            parse(include_toc=False)       → content only
        """
        toc_entries = []
        if include_toc:
            toc_entries = self._extract_toc()

        content_items = self._extract_content()

        return ParserResult(
            toc_entries=toc_entries,
            content_items=content_items
        )

    # ---------------------------------------------------------
    # Protected Internal Methods
    # ---------------------------------------------------------
    def _extract_toc(self) -> list[Any]:
        """Protected: Extract TOC entries using TOCExtractor."""
        try:
            return TOCExtractor(self.file_path).extract()
        except Exception as e:
            raise ValueError(f"Failed to extract TOC: {e}") from e

    def _extract_content(self) -> list[Any]:
        """Protected: Extract content from PDF."""
        try:
            with fitz.open(str(self.file_path)) as doc:  # type: ignore
                extractor = ContentExtractor(self.__doc_title)
                return extractor.extract(doc)
        except Exception as e:
            raise ValueError(f"Failed to extract content: {e}") from e

    # ---------------------------------------------------------
    # Protected Helper Methods
    # ---------------------------------------------------------
    def _read(self) -> Any:
        """Protected: Read raw PDF document."""
        try:
            return fitz.open(str(self.file_path))  # type: ignore[attr-defined]
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}") from e

    def _extract_raw_text(self) -> str:
        """Protected: extract raw text only."""
        try:
            # type: ignore[attr-defined]
            with fitz.open(str(self.file_path)) as doc:
                text: str = ""
                for page in doc:  # type: ignore[attr-defined]
                    page_text = page.get_text()  # type: ignore[attr-defined]
                    if isinstance(page_text, str):
                        text += page_text
                return text
        except Exception as e:
            raise ValueError(f"Unable to extract raw text: {e}") from e

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        """Method implementation."""
        return (
            f"PDFParser(file={self.file_path.name}, "
            f"title={self.__doc_title})"
        )

    def __repr__(self) -> str:
        """Method implementation."""
        return (
            f"PDFParser(file_path={self.file_path!r}, "
            f"doc_title={self.__doc_title!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, PDFParser):
            return NotImplemented
        return (
            self.file_path == other.file_path
            and self.__doc_title == other.__doc_title
        )

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((type(self).__name__, self.file_path, self.__doc_title))

    def __contains__(self, text: str) -> bool:
        """Method implementation."""
        return text.lower() in self.__doc_title.lower()

    def __len__(self) -> int:
        """Method implementation."""
        return len(self.__doc_title)

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, PDFParser):
            return NotImplemented
        return self.file_size < other.file_size

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return self.__doc_title[index]

    def __enter__(self) -> "PDFParser":
        """Context manager: open parser."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager: close parser."""
        self.close()

    def __call__(self) -> ParserResult:
        """Make parser callable."""
        return self.parse()

    def __int__(self) -> int:
        """Method implementation."""
        return self.file_size

    def __float__(self) -> float:
        """Method implementation."""
        return float(self.file_size)

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __iter__(self):
        """Method implementation."""
        return iter([self.parser_type, self.doc_title])

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, PDFParser):
            return NotImplemented
        return self.file_size > other.file_size

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other
