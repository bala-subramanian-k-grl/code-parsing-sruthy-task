"""Protocol interface for better abstraction."""

from pathlib import Path
from typing import Any, Protocol


class Extractable(Protocol):  # Protocol Abstraction
    """Protocol for extractable objects."""

    def extract(self) -> Any:
        """Extract data."""
        ...


class Searchable(Protocol):  # Protocol Abstraction
    """Protocol for searchable objects."""

    def search(self, term: str) -> list[dict[str, Any]]:
        """Search for term."""
        ...


class Displayable(Protocol):  # Protocol Abstraction
    """Protocol for displayable objects."""

    def show(self, data: Any, term: str) -> None:
        """Display data."""
        ...


class Configurable(Protocol):  # Protocol Abstraction
    """Protocol for configurable objects."""

    @property
    def pdf_input_file(self) -> Path:
        """Get PDF input file path."""
        ...

    @property
    def output_directory(self) -> Path:
        """Get output directory path."""
        ...


class Writable(Protocol):  # Protocol Abstraction
    """Protocol for writable objects."""

    def write(self, data: Any) -> None:
        """Write data."""
        ...


class Cacheable(Protocol):  # Protocol Abstraction
    """Protocol for cacheable objects."""

    def cache_get(self, key: str) -> Any:
        """Get from cache."""
        ...

    def cache_set(self, key: str, value: Any) -> None:
        """Set cache value."""
        ...

    def cache_clear(self) -> None:
        """Clear cache."""
        ...


# Concrete implementations for polymorphism
class BaseExtractable:  # Base class for extractable objects
    """Base extractable implementation."""

    def __init__(self) -> None:
        self.__extraction_count: int = 0  # Private counter
        self.__last_result: Any = None  # Private result cache

    @property
    def extraction_count(self) -> int:
        """Get extraction count."""
        return self.__extraction_count

    def __increment_count(self) -> None:  # Private method
        """Increment extraction counter."""
        self.__extraction_count += 1

    def __cache_result(self, result: Any) -> None:  # Private method
        """Cache extraction result."""
        self.__last_result = result

    def extract(self) -> Any:
        """Base extract implementation."""
        self.__increment_count()
        result = "extracted_data"
        self.__cache_result(result)
        return result


class FastExtractable(BaseExtractable):  # Inheritance + Polymorphism
    """Fast extractable implementation."""

    def extract(self) -> Any:  # Method override
        """Fast extraction."""
        result = super().extract()
        return f"fast_{result}"


class DetailedExtractable(BaseExtractable):  # Inheritance + Polymorphism
    """Detailed extractable implementation."""

    def extract(self) -> Any:  # Method override
        """Detailed extraction."""
        result = super().extract()
        return {"detailed": result, "count": self.extraction_count}
