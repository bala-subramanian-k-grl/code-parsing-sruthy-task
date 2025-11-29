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
        super().__init__(file_path)
        self.__doc_title = doc_title

    # ---------------------------------------------------------
    # Polymorphism (Override from BaseParser)
    # ---------------------------------------------------------
    @property
    def parser_type(self) -> str:
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
        return self.__doc_title

    @doc_title.setter
    def doc_title(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Document title cannot be empty.")
        self.__doc_title = value

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
    # Additional Polymorphic Helper
    # ---------------------------------------------------------
    def read(self) -> Any:
        """Override: Read raw PDF document."""
        try:
            return fitz.open(str(self.file_path))  # type: ignore[attr-defined]
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}") from e

    def extract_raw_text(self) -> str:
        """Polymorphic helper: extract raw text only."""
        try:
            with fitz.open(str(self.file_path)) as doc:  # type: ignore[attr-defined]
                text: str = ""
                for page in doc:  # type: ignore[attr-defined]
                    page_text = page.get_text()  # type: ignore[attr-defined]
                    if isinstance(page_text, str):
                        text += page_text
                return text
        except Exception as e:
            raise ValueError(f"Unable to extract raw text: {e}")

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"PDFParser(file={self.file_path.name}, title={self.__doc_title})"

    def __repr__(self) -> str:
        return (
            f"PDFParser(file_path={self.file_path!r}, "
            f"doc_title={self.__doc_title!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PDFParser):
            return NotImplemented
        return (
            self.file_path == other.file_path
            and self.__doc_title == other.__doc_title
        )

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.file_path, self.__doc_title))

    def __contains__(self, text: str) -> bool:
        return text.lower() in self.__doc_title.lower()

    def __len__(self) -> int:
        return len(self.__doc_title)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PDFParser):
            return NotImplemented
        return self.file_size < other.file_size

    def __getitem__(self, index: int) -> str:
        return self.__doc_title[index]
