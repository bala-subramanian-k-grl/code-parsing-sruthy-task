"""Base classe implementing OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractor(ABC):
    """Abstract base class for extractors (Abstraction)."""

    def __init__(self, config: dict[str, Any]):
        self.__config = config  # Private encapsulation
        self.__extraction_count: int = 0  # Private counter

    @abstractmethod
    def extract(self, file_path: Path) -> list[dict[str, Any]]:
        """Abstract method for extraction (Abstraction)."""

    @property
    def config(self) -> dict[str, Any]:
        """Get configuration (read-only)."""
        return self.__config.copy()

    def __increment_count(self) -> None:  # Private method
        """Increment extraction counter."""
        self.__extraction_count += 1

    def _validate_file(self, file_path: Path) -> None:
        """Protected method for file validation (Encapsulation)."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        self.__increment_count()


class BaseWriter(ABC):
    """Abstract base class for writers (Abstraction)."""

    def __init__(self, output_path: Path):
        self.__output_path = self._validate_path(output_path)  # Private
        self.__write_count: int = 0  # Private counter

    def _validate_path(self, path: Path) -> Path:  # Encapsulation
        """Validate and secure output path."""
        safe_path = path.resolve()  # Prevent path traversal
        try:
            safe_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RuntimeError(
                f"Cannot create directory {safe_path.parent}: {e}"
            ) from e
        return safe_path

    @abstractmethod
    def write(self, data: Any) -> None:
        """Abstract write method (Abstraction)."""
        self.__increment_write_count()  # Track write operations

    @property
    def output_path(self) -> Path:
        """Getter for output path (Encapsulation)."""
        return self.__output_path

    def __increment_write_count(self) -> None:  # Private method
        """Increment write counter."""
        self.__write_count += 1


class Processor:
    """Base processor with common functionality."""

    def __init__(self, name: str):
        self.__name = name  # Private encapsulation
        self.__processed_count = 0  # Private encapsulation

    def __increment_count(self) -> None:  # Private method
        """Increment processed count."""
        self.__processed_count += 1

    @property
    def processed_count(self) -> int:
        """Getter for count (Encapsulation)."""
        return self.__processed_count

    @property
    def name(self) -> str:
        """Getter for name (Encapsulation)."""
        return self.__name

    def process_item(self, item: Any) -> Any:
        """Process single item with tracking."""
        self.__increment_count()
        return item


class FastProcessor(Processor):  # Inheritance + Polymorphism
    """Fast processor variant."""

    def process_item(self, item: Any) -> Any:  # Method override
        """Fast processing implementation."""
        result = super().process_item(item)
        return f"fast_{result}"


class DetailedProcessor(Processor):  # Inheritance + Polymorphism
    """Detailed processor variant."""

    def process_item(self, item: Any) -> Any:  # Method override
        """Detailed processing implementation."""
        result = super().process_item(item)
        return {"detailed": result}
