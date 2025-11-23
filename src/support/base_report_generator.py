"""Base report generator with full OOP structure."""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.core.config.models import ParserResult
from src.core.interfaces.report_interface import IReportGenerator


class BaseReportGenerator(IReportGenerator, ABC):
    """
    Abstract base class for all report generators.

    Implements:
        - Template Method Pattern
        - Strict abstraction hooks
        - Polymorphism (file extension, formatter, writer)
        - Encapsulation for internal state tracking
    """

    def __init__(self) -> None:
        self.__generation_count = 0                 # private
        self.__last_output_path: Path | None = None  # private
        self.__last_success: bool = False           # private

    # ---------------------------------------------------------
    # Encapsulated Properties
    # ---------------------------------------------------------

    @property
    def generation_count(self) -> int:
        """Number of times this generator was used."""
        return self.__generation_count

    @property
    def last_output_path(self) -> Path | None:
        """Path of last generated report."""
        return self.__last_output_path

    @property
    def last_success(self) -> bool:
        """Whether last generation succeeded."""
        return self.__last_success

    # ---------------------------------------------------------
    # Template Method (Do NOT override in subclasses)
    # ---------------------------------------------------------

    def generate(self, result: ParserResult, path: Path) -> None:
        """
        Template method that defines the workflow:
            1. Validate input result
            2. Format data
            3. Write to target file
        """
        self.__generation_count += 1

        self._validate_result(result)
        formatted = self._format_data(result)
        self._write_to_file(formatted, path)

        self.__last_output_path = path
        self.__last_success = True

    # ---------------------------------------------------------
    # Abstract Methods (Polymorphism Points)
    # ---------------------------------------------------------

    @abstractmethod
    def _validate_result(self, result: ParserResult) -> None:
        """Validate ParserResult before processing."""

    @abstractmethod
    def _format_data(self, result: ParserResult) -> Any:
        """Format result data for output."""

    @abstractmethod
    def _write_to_file(self, data: Any, path: Path) -> None:
        """Write formatted data to requested file."""

    @abstractmethod
    def get_file_extension(self) -> str:
        """Return the file extension for this generator."""

    # ---------------------------------------------------------
    # Magic Methods (Clean, Highly Reusable)
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(format={self.get_file_extension()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True

    def __int__(self) -> int:
        return self.__generation_count

    def __float__(self) -> float:
        return float(self.__generation_count)
