"""Base report generator with polymorphic methods."""

from abc import abstractmethod
from pathlib import Path
from typing import Any

from src.core.config.models import ParserResult
from src.core.interfaces.report_interface import IReportGenerator


class BaseReportGenerator(IReportGenerator):
    """Abstract base class for all report generators."""

    def __init__(self) -> None:
        """Initialize base report generator."""
        self._generation_count = 0

    @property
    def generation_count(self) -> int:
        """Get generation count."""
        return self._generation_count

    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate report with validation and formatting."""
        self._generation_count += 1
        self._validate_result(result)
        formatted_data = self._format_data(result)
        self._write_to_file(formatted_data, path)

    @abstractmethod
    def _validate_result(self, result: ParserResult) -> None:
        """Validate result before generation (polymorphic)."""
        ...

    @abstractmethod
    def _format_data(self, result: ParserResult) -> Any:
        """Format data for output (polymorphic)."""
        ...

    @abstractmethod
    def _write_to_file(self, data: Any, path: Path) -> None:
        """Write formatted data to file (polymorphic)."""
        ...

    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension for this generator (polymorphic)."""
        ...

    def __str__(self) -> str:
        """String representation."""
        ext = self.get_file_extension()
        return f"{self.__class__.__name__}(format={ext})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        """Hash for set/dict usage."""
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        """Boolean conversion."""
        return True

    def __int__(self) -> int:
        """Integer conversion."""
        return self._generation_count

    def __float__(self) -> float:
        """Float conversion."""
        return float(self._generation_count)
