"""Abstract Base Writer Module"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol


class WriterProtocol(Protocol):  # Protocol for polymorphism
    """Protocol for writer implementations."""

    def write(self, data: Any) -> None:
        """Write data to output."""
        ...

    def get_format(self) -> str:
        """Get format name."""
        ...


class BaseWriter(ABC):  # Abstraction
    """Abstract writer with encapsulation and polymorphism."""

    def __init__(self, output_path: Path):
        """Initialize writer with output path validation."""
        self.__output_path = self.__validate_path(output_path)  # Private

    def __validate_path(self, path: Path) -> Path:  # Private method
        """Validate and secure output path."""
        safe_path = path.resolve()  # Prevent path traversal
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        return safe_path

    @abstractmethod  # Abstraction
    def write(self, data: Any) -> None:
        """Abstract write method - must be implemented by subclasses."""

    @abstractmethod
    def get_format(self) -> str:
        """Get output format name - must be implemented by subclasses."""

    def __call__(self, data: Any) -> None:  # Magic method
        """Make writer callable."""
        self.write(data)

    def __str__(self) -> str:  # Magic method
        """String representation."""
        return f"{self.__class__.__name__}({self.output_path.name})"

    def __repr__(self) -> str:  # Magic method
        """Detailed representation."""
        return f"{self.__class__.__name__}(output_path={self.__output_path!r})"

    def __eq__(self, other: object) -> bool:  # Magic method
        """Compare writers by output path."""
        if not isinstance(other, BaseWriter):
            return False
        return self.__output_path == other.__output_path

    def __hash__(self) -> int:  # Magic method
        """Hash based on output path."""
        return hash(self.__output_path)

    @property  # Encapsulation
    def output_path(self) -> Path:
        """Get output path (read-only)."""
        return self.__output_path

    @property  # Encapsulation
    def output_directory(self) -> Path:
        """Get output directory (read-only)."""
        return self.__output_path.parent

    @property  # Encapsulation
    def file_name(self) -> str:
        """Get file name (read-only)."""
        return self.__output_path.name

    def validate_data(self, data: Any) -> bool:
        """Validate data before writing."""
        return data is not None

    def get_file_size(self) -> int:
        """Get output file size if exists."""
        if self.__output_path.exists():
            return self.__output_path.stat().st_size
        return 0
