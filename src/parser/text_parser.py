"""Text parser implementation."""

from __future__ import annotations
from pathlib import Path

from src.core.config.models import ContentItem, ParserResult
from src.parser.base_parser import BaseParser


class TextParser(BaseParser):
    """Concrete text parser."""

    def __init__(self, file_path: Path, doc_title: str = "Document") -> None:
        super().__init__(file_path)
        self.__doc_title = doc_title

    # ---------------------------------------------------------
    # Polymorphism
    # ---------------------------------------------------------
    @property
    def parser_type(self) -> str:
        """Return parser type."""
        return "TEXT"

    def supports(self, extension: str) -> bool:
        """Polymorphic override—supports .txt files only."""
        return extension.lower() == ".txt"

    @property
    def is_binary(self) -> bool:
        """Text files are not binary."""
        return False

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------
    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self.__doc_title

    # ---------------------------------------------------------
    # Parsing Implementation
    # ---------------------------------------------------------
    def parse(self) -> ParserResult:
        """Parse text file and extract content."""
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                content = f.read()

            items = [
                ContentItem(
                    doc_title=self.__doc_title,
                    section_id="text_content",
                    title=self.__doc_title,
                    content=content,
                    page=1,
                )
            ]

            return ParserResult(content_items=items)

        except (OSError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to parse text file: {e}") from e

    # ---------------------------------------------------------
    # Validation Override (LSP-safe)
    # ---------------------------------------------------------
    def validate(self) -> bool:
        """Validate text file has .txt extension."""
        return super().validate() and self.file_path.suffix.lower() == ".txt"

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"TextParser(file={self.file_path.name}, title={self.__doc_title})"

    def __repr__(self) -> str:
        return f"TextParser(file_path={self.file_path!r}, doc_title={self.__doc_title!r})"
