"""Base parser abstract class."""

from abc import ABC, abstractmethod
from pathlib import Path

from src.core.config.models import ParserResult
from src.core.interfaces.parser_interface import ParserInterface


class BaseParser(ParserInterface, ABC):
    """Abstract base class for all parsers."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        if not self.validate():
            raise FileNotFoundError(
                f"File not found or is not a file: {file_path}"
            )

    @property
    def file_path(self) -> Path:
        """Get the file path being parsed."""
        return self._file_path

    @property
    def file_name(self) -> str:
        """Get file name."""
        return self._file_path.name

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self._file_path.exists()

    @property
    def file_size(self) -> int:
        """Get file size."""
        return self._file_path.stat().st_size if self._file_path.exists() else 0

    @property
    def file_suffix(self) -> str:
        """Get file suffix."""
        return self._file_path.suffix

    def validate(self) -> bool:
        """Validate that the file path exists and is a file."""
        return self._file_path.exists() and self._file_path.is_file()

    @abstractmethod
    def parse(self) -> ParserResult:
        """Parse file and return result - implemented by subclasses."""

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(file={self._file_path.name})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"{self.__class__.__name__}(file_path={self._file_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self._file_path == other._file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._file_path))

    def __len__(self) -> int:
        return len(str(self._file_path))

    def __bool__(self) -> bool:
        return self._file_path.exists()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseParser):
            return NotImplemented
        return str(self._file_path) < str(other._file_path)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, text: str) -> bool:
        """Check if text in file path."""
        return text in str(self._file_path)
