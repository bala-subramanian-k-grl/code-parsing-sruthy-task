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

    def validate(self) -> bool:
        """Validate that the file path exists and is a file."""
        return self._file_path.exists() and self._file_path.is_file()

    @abstractmethod
    def parse(self) -> ParserResult:
        """Parse file and return result - implemented by subclasses."""
