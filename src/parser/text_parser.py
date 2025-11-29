"""Text parser implementation with OOP, Overloading, and Polymorphism."""

from __future__ import annotations

from pathlib import Path
from typing import overload

from src.core.config.models import ContentItem, ParserResult
from src.parser.base_parser import BaseParser


class TextParser(BaseParser):
    """Concrete text parser."""

    # ---------------------------------------------------------
    # INIT (Encapsulation)
    # ---------------------------------------------------------
    def __init__(self, file_path: Path, doc_title: str = "Document") -> None:
        super().__init__(file_path)
        self.__doc_title = doc_title

    # ---------------------------------------------------------
    # Polymorphism (override)
    # ---------------------------------------------------------
    @property
    def parser_type(self) -> str:
        return "TEXT"

    def supports(self, extension: str) -> bool:
        """Override: supports only .txt"""
        return extension.lower() in {".txt", "txt"}

    @property
    def is_binary(self) -> bool:
        return False

    # ---------------------------------------------------------
    # Encapsulation (controlled title)
    # ---------------------------------------------------------
    @property
    def doc_title(self) -> str:
        return self.__doc_title

    @doc_title.setter
    def doc_title(self, title: str) -> None:
        if not title.strip():
            raise ValueError("Document title cannot be empty.")
        self.__doc_title = title

    # ---------------------------------------------------------
    # OVERLOADED parse()
    # ---------------------------------------------------------
    @overload
    def parse(self) -> ParserResult: ...

    @overload
    def parse(self, *, max_chars: int) -> ParserResult: ...

    @overload
    def parse(self, *, include_metadata: bool) -> ParserResult: ...

    def parse(
        self,
        *,
        max_chars: int | None = None,
        include_metadata: bool = False
    ) -> ParserResult:
        """
        Overloaded parse() method:
        ---------------------------------------
        parse()                          → normal full parse
        parse(max_chars=1000)            → truncate output
        parse(include_metadata=True)     → include metadata fields
        """
        content = self._read_file()

        if max_chars is not None:
            content = content[:max_chars]

        items = [
            ContentItem(
                doc_title=self.__doc_title,
                section_id="text_content",
                title=self.__doc_title,
                content=content,
                page=1,
            )
        ]

        result = ParserResult(content_items=items)

        if include_metadata:
            result.metadata.total_pages = 1
            result.metadata.total_content_items = 1

        return result

    # ---------------------------------------------------------
    # Protected internal helper
    # ---------------------------------------------------------
    def _read_file(self) -> str:
        """Protected: read text from file."""
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {e}") from e

    # ---------------------------------------------------------
    # Override validate() safely
    # ---------------------------------------------------------
    def validate(self, *, raise_on_error: bool = False) -> bool:
        """Override validation for .txt files."""
        is_valid = (
            super().validate()
            and self.file_path.suffix.lower() == ".txt"
        )

        if not is_valid and raise_on_error:
            raise FileNotFoundError(
                f"Invalid text file: {self.file_path}"
            )
        return is_valid

    # ---------------------------------------------------------
    # Polymorphic helper
    # ---------------------------------------------------------
    def get_first_line(self) -> str:
        """Return the first line of the text file."""
        content = self._read_file()
        return content.split("\n", 1)[0] if content else ""

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"TextParser(file={self.file_path.name}, "
            f"title={self.__doc_title})"
        )

    def __repr__(self) -> str:
        return (
            f"TextParser(file_path={self.file_path!r}, "
            f"doc_title={self.__doc_title!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextParser):
            return NotImplemented
        return self.file_path == other.file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.file_path))

    def __bool__(self) -> bool:
        return bool(self.__doc_title)

    def __len__(self) -> int:
        return len(self.__doc_title)

    def __contains__(self, text: str) -> bool:
        return text.lower() in self.__doc_title.lower()
