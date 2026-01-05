"""PDF parser implementation with full OOP, Overloading, Polymorphism."""

from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Any, overload

import fitz

from src.core.config.models import ParserResult
from src.extractors.content_extractor import ContentExtractor
from src.parser.base_parser import BaseParser
from src.parser.toc_extractor import TOCExtractor
from src.utils.logger import logger


class PDFParser(BaseParser, ABC):
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
        msg = (f"PDF parsing started: {self.file_path.name} "
               f"(size: {self.file_size_mb:.2f} MB)")
        logger.info(msg)
        toc_entries = []
        if include_toc:
            toc_entries = self._extract_toc()

        content_items = self._extract_content()
        logger.info(f"Content items extracted: {len(content_items)}")

        result = ParserResult(
            toc_entries=toc_entries,
            content_items=content_items
        )
        msg = (f"PDF parsing completed: {len(toc_entries)} TOC + "
               f"{len(content_items)} content items")
        logger.info(msg)
        return result

    # ---------------------------------------------------------
    # Protected Internal Methods
    # ---------------------------------------------------------
    def _extract_toc(self) -> list[Any]:
        """Protected: Extract TOC entries using TOCExtractor."""
        try:
            return TOCExtractor(self.file_path).extract()
        except Exception as e:
            logger.error(f"TOC extraction failed: {e}")
            raise ValueError(f"Failed to extract TOC: {e}") from e

    def _extract_content(self) -> list[Any]:
        """Protected: Extract content from PDF."""
        try:
            with fitz.open(str(self.file_path)) as doc:
                extractor = ContentExtractor(self.__doc_title, str(self.file_path))
                return extractor.extract(doc)
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            raise ValueError(f"Failed to extract content: {e}") from e

    # ---------------------------------------------------------
    # Protected Helper Methods
    # ---------------------------------------------------------




    # ---------------------------------------------------------
    # Required abstract methods from ParserInterface
    # ---------------------------------------------------------

    def open(self, mode: str = "r") -> None:
        """Open parser resources."""
        pass

    def close(self) -> None:
        """Close parser resources."""
        pass

    def read(self) -> Any:
        """Read and return parsed data."""
        return self.parse()

    def reset(self) -> None:
        """Reset parser state."""
        pass

    def supports_format(self, format_type: str = "", *formats: str) -> bool:
        """Check if format is supported."""
        all_formats = (format_type,) + formats if format_type else formats
        if not all_formats:
            return False
        return any(self.supports(fmt) for fmt in all_formats)

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
