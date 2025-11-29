"""
Base report generator with full OOP structure + Overloading.

Enhancements Added:
-------------------
✔ Template Method Pattern (final generate())
✔ Overloading of generate() for flexibility
✔ Protected lifecycle hooks (before_write, after_write)
✔ Better abstraction enforcement
✔ Polymorphic extension support (supports_format)
✔ More encapsulation for internal state
✔ Error tracking, success tracking
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, overload

from src.core.config.models import ParserResult
from src.core.interfaces.report_interface import IReportGenerator


class BaseReportGenerator(IReportGenerator, ABC):
    """Abstract base class for all report generators."""

    # ---------------------------------------------------------
    # INIT (State Encapsulation)
    # ---------------------------------------------------------
    def __init__(self) -> None:
        self.__generation_count = 0
        self.__last_output_path: Path | None = None
        self.__last_success = False
        self.__error_count = 0
        self.__total_bytes_written = 0
        self.__initialized = True

    # ---------------------------------------------------------
    # Encapsulated Read-Only Properties
    # ---------------------------------------------------------
    @property
    def generation_count(self) -> int:
        return self.__generation_count

    @property
    def last_output_path(self) -> Path | None:
        return self.__last_output_path

    @property
    def last_success(self) -> bool:
        return self.__last_success

    @property
    def error_count(self) -> int:
        return self.__error_count

    @property
    def total_bytes_written(self) -> int:
        return self.__total_bytes_written

    @property
    def is_initialized(self) -> bool:
        return self.__initialized

    # ---------------------------------------------------------
    # Polymorphic Capability
    # ---------------------------------------------------------
    @property
    @abstractmethod
    def report_type(self) -> str:
        """Return human-friendly report type (PDF, JSON, Excel)."""

    @abstractmethod
    def get_file_extension(self) -> str:
        """Return extension like .json / .xlsx"""

    def supports_format(self, ext: str) -> bool:
        """Polymorphic: Check if generator supports a file format."""
        return ext.lower() == self.get_file_extension()

    # ---------------------------------------------------------
    # Overloaded generate() for flexibility
    # ---------------------------------------------------------
    @overload
    def generate(self, result: ParserResult, path: Path) -> None:
        ...

    @overload
    def generate(self, result: ParserResult, path: str) -> None:
        ...

    # ---------------------------------------------------------
    # FINAL Template Method Pattern
    # ---------------------------------------------------------
    def generate(self, result: ParserResult, path: Path | str) -> None:
        """Do NOT override in subclasses."""
        self.__generation_count += 1

        # Allow string path input
        if isinstance(path, str):
            path = Path(path)

        try:
            self._validate_result(result)

            self.before_write(result, path)

            formatted = self._format_data(result)
            bytes_written = self._write_to_file(formatted, path)

            self.__total_bytes_written += bytes_written or 0
            self.__last_success = True
            self.__last_output_path = path

            self.after_write(result, path)

        except Exception:
            self.__error_count += 1
            self.__last_success = False
            raise

    # ---------------------------------------------------------
    # Protected Lifecycle Hooks (Optional override)
    # ---------------------------------------------------------
    def before_write(self, result: ParserResult, path: Path) -> None:
        """Hook called before writing (optional)."""

    def after_write(self, result: ParserResult, path: Path) -> None:
        """Hook called after writing (optional)."""

    # ---------------------------------------------------------
    # Abstract Methods (Subclasses MUST implement)
    # ---------------------------------------------------------
    @abstractmethod
    def _validate_result(self, result: ParserResult) -> None:
        pass

    @abstractmethod
    def _format_data(self, result: ParserResult) -> Any:
        pass

    @abstractmethod
    def _write_to_file(self, data: Any, path: Path) -> int:
        """Return number of bytes written."""

    # ---------------------------------------------------------
    # Magic Methods (clean + helpful)
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(ext={self.get_file_extension()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> bool:
        return self.__initialized

    def __int__(self) -> int:
        return self.__generation_count

    def __float__(self) -> float:
        return float(self.__generation_count)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)
