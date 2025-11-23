"""Base parser abstract class."""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

from src.core.config.models import ParserResult
from src.core.interfaces.parser_interface import ParserInterface


class BaseParser(ParserInterface, ABC):
    """Abstract base class for all parsers with full OOP support."""

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

        if not self.validate():
            raise FileNotFoundError(
                f"File not found or is not a valid file: {file_path}"
            )

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------

    @property
    def file_path(self) -> Path:
        """Get the file path being parsed."""
        return self.__file_path

    @property
    def file_name(self) -> str:
        """Get filename."""
        return self.__file_path.name

    @property
    def file_suffix(self) -> str:
        """Get file extension."""
        return self.__file_path.suffix.lower()

    @property
    def file_size(self) -> int:
        """Get file size in bytes."""
        return (
            self.__file_path.stat().st_size
            if self.__file_path.exists()
            else 0
        )

    # ---------------------------------------------------------
    # Polymorphism (subclass-specific behavior)
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def parser_type(self) -> str:
        """Polymorphic parser identifier."""
        raise NotImplementedError

    def supports(self, extension: str) -> bool:
        """Polymorphic extension support check."""
        return extension.lower() == self.file_suffix

    # ---------------------------------------------------------
    # Abstraction (common contract for all parsers)
    # ---------------------------------------------------------

    def validate(self) -> bool:
        """Validate that the file exists and is a file."""
        return self.__file_path.exists() and self.__file_path.is_file()

    @abstractmethod
    def parse(self) -> ParserResult:
        """Parse file and return result - implemented by subclasses."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Magic Methods (clean and consistent)
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(file={self.file_name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(file_path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path))

    def __bool__(self) -> bool:
        return self.__file_path.exists()
