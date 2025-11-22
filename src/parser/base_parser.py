"""Base parser abstract class."""

from abc import ABC, abstractmethod
from pathlib import Path

from src.core.config.models import ParserResult
from src.core.interfaces.parser_interface import ParserInterface


class BaseParser(ParserInterface, ABC):
    """Abstract base class for all parsers."""

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path
        if not self.validate():
            raise FileNotFoundError(
                f"File not found or is not a file: {file_path}"
            )

    @property
    def file_path(self) -> Path:
        """Get the file path being parsed."""
        return self.__file_path

    def validate(self) -> bool:
        """Validate that the file path exists and is a file."""
        return self.__file_path.exists() and self.__file_path.is_file()

    @abstractmethod
    def parse(self) -> ParserResult:
        """Parse file and return result - implemented by subclasses."""

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(file={self.__file_path.name})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"{self.__class__.__name__}(file_path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        """Hash for set/dict usage."""
        return hash((type(self).__name__, self.__file_path))

    def __bool__(self) -> bool:
        """Boolean conversion."""
        return self.__file_path.exists()
