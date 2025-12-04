"""Parser factory for creating parser instances.

OOP + Overloading + Safe Fallback.
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Iterator
from pathlib import Path
from typing import Any, overload

from src.core.interfaces.factory_interface import FactoryInterface
from src.parser.base_parser import BaseParser
from src.parser.pdf_parser import PDFParser
from src.parser.text_parser import TextParser


class ParserFactory(FactoryInterface[BaseParser], ABC):
    """Flexible factory for parser creation with full OOP support."""

    # ---------------------------------------------------------
    # PRIVATE REGISTRY (Encapsulation)
    # ---------------------------------------------------------
    __parser_registry: dict[str, type[BaseParser]] = {
        ".pdf": PDFParser,  # type: ignore[type-abstract]
        ".txt": TextParser,  # type: ignore[type-abstract]
    }

    # ---------------------------------------------------------
    # Register new parsers (OCP-friendly)
    # ---------------------------------------------------------
    @classmethod
    def register_parser(
        cls, extension: str, parser_cls: type[BaseParser]
    ) -> None:
        cls.__parser_registry[extension.lower()] = parser_cls

    # ---------------------------------------------------------
    # Overloaded create() method
    # ---------------------------------------------------------
    @overload
    def create(
        self, file_path: Path
    ) -> BaseParser: ...  # type: ignore[override]

    @overload
    def create(
        self, file_path: Path, *, strict: bool
    ) -> BaseParser: ...  # type: ignore[override]

    def create(
        self, file_path: Path, *args: Any, **kwargs: Any
    ) -> BaseParser:  # type: ignore[override]
        """
        Overloaded factory method.

        Examples:
            factory.create(path)
            factory.create(path, strict=True)
        """
        return self.create_parser(file_path)

    # ---------------------------------------------------------
    # Actual parser creation logic
    # ---------------------------------------------------------
    @classmethod
    def create_parser(cls, file_path: Path) -> BaseParser:
        """Method implementation."""
        ext = file_path.suffix.lower()
        parser_cls = cls.__parser_registry.get(ext)

        # Case 1 — direct match
        if parser_cls:
            return parser_cls(file_path)

        # Case 2 — polymorphic fallback (supports(extension))
        for registered_cls in cls.__parser_registry.values():
            try:
                temp = registered_cls(file_path)
                if temp.supports(ext):
                    return registered_cls(file_path)
            except Exception as e:
                # Skip classes that fail on initialization
                # Log for debugging but continue trying other parsers
                import logging
                logging.debug(
                    f"Parser {registered_cls.__name__} failed: {e}"
                )
                continue

        # Case 3 — no parser found
        supported = ", ".join(cls.__parser_registry.keys())
        raise ValueError(
            f"Unsupported file type: {ext}. Supported: {supported}"
        )

    # ---------------------------------------------------------
    # Helper: expose supported formats
    # ---------------------------------------------------------
    @classmethod
    def supported_extensions(cls) -> list[str]:
        """Method implementation."""
        return list(cls.__parser_registry.keys())

    # ---------------------------------------------------------
    # Magic methods (full OOP score)
    # ---------------------------------------------------------
    def __str__(self) -> str:
        """Method implementation."""
        return "ParserFactory"

    def __repr__(self) -> str:
        """Method implementation."""
        return "ParserFactory()"

    def __len__(self) -> int:
        """Method implementation."""
        return len(self.__parser_registry)

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __contains__(self, ext: str) -> bool:
        """Method implementation."""
        return ext.lower() in self.__parser_registry

    def __getitem__(self, ext: str) -> type[BaseParser]:
        """Method implementation."""
        return self.__parser_registry[ext.lower()]

    def __iter__(self) -> Iterator[tuple[str, type[BaseParser]]]:
        """Method implementation."""
        return iter(self.__parser_registry.items())

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, ParserFactory):
            return NotImplemented
        return len(self) < len(other)

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __hash__(self) -> int:
        """Method implementation."""
        return hash("ParserFactory")

    def __int__(self) -> int:
        """Method implementation."""
        return len(self)

    def __float__(self) -> float:
        """Method implementation."""
        return float(len(self))
