"""Protocol interfaces for better abstraction."""

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
