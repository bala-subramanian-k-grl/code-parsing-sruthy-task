"""Parser factory for creating parser instances."""

from __future__ import annotations
from pathlib import Path

from src.parser.base_parser import BaseParser
from src.parser.pdf_parser import PDFParser
from src.parser.text_parser import TextParser


class ParserFactory:
    """Factory for creating the appropriate parser based on file extension."""

    # ---------------------------------------------------------
    # Encapsulation — registry is private
    # ---------------------------------------------------------
    __parser_registry: dict[str, type[BaseParser]] = {
        ".pdf": PDFParser,
        ".txt": TextParser,
    }

    # ---------------------------------------------------------
    # Register new parsers (Open/Closed Principle)
    # ---------------------------------------------------------
    @classmethod
    def register_parser(cls, extension: str, parser_cls: type[BaseParser]) -> None:
        """Register a new parser type for given extension."""
        cls.__parser_registry[extension.lower()] = parser_cls

    # ---------------------------------------------------------
    # Parser Creation (Polymorphism + Inheritance)
    # ---------------------------------------------------------
    @classmethod
    def create_parser(cls, file_path: Path) -> BaseParser:
        """Create parser instance based on file extension."""

        ext = file_path.suffix.lower()
        parser_cls = cls.__parser_registry.get(ext)

        # If parser class found directly — use it
        if parser_cls:
            return parser_cls(file_path)

        # Polymorphic fallback: check supports()
        for registered_cls in cls.__parser_registry.values():
            if registered_cls(file_path).supports(ext):
                return registered_cls(file_path)

        # No parser found
        supported = ", ".join(cls.__parser_registry.keys())
        raise ValueError(
            f"Unsupported file type: {ext}. Supported extensions: {supported}"
        )

    # ---------------------------------------------------------
    # Optional: expose list of supported formats
    # ---------------------------------------------------------
    @classmethod
    def supported_extensions(cls) -> list[str]:
        """Return list of supported file extensions."""
        return list(cls.__parser_registry.keys())
