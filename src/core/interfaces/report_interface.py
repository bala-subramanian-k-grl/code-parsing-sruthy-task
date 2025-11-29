"""
Enterprise-level Report Generator Interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import overload

from src.core.config.models import ParserResult


class IReportGenerator(ABC):
    """Interface for all report generator implementations."""

    # ==========================================================
    # CONSTRUCTOR (Encapsulation)
    # ==========================================================

    def __init__(self) -> None:
        self._last_path: Path | None = None
        self._errors: list[str] = []
        self._is_ready: bool = False

    # ==========================================================
    # ENCAPSULATED PROPERTIES
    # ==========================================================

    @property
    @abstractmethod
    def report_type(self) -> str:
        """Return human-friendly report type: PDF, HTML, JSON."""
        raise NotImplementedError

    @property
    @abstractmethod
    def output_extension(self) -> str:
        """Return generated file extension: .pdf, .html."""
        raise NotImplementedError

    @property
    def is_ready(self) -> bool:
        """Whether generator has been prepared."""
        return self._is_ready

    @property
    def last_error(self) -> str | None:
        return self._errors[-1] if self._errors else None

    # ==========================================================
    # PROTECTED HELPERS (ENCAPSULATION)
    # ==========================================================

    def _set_error(self, message: str) -> None:
        self._errors.append(message)

    def _ensure_path(self, path: Path) -> None:
        if not path.parent.exists():
            msg = f"Output directory not found: {path.parent}"
            raise FileNotFoundError(msg)

    def _ensure_ready(self) -> None:
        if not self._is_ready:
            msg = "Report generator is not prepared. Call prepare()."
            raise RuntimeError(msg)

    # ==========================================================
    # OPTIONAL LIFECYCLE HOOKS
    # ==========================================================

    def prepare(self) -> None:
        """Prepare generator resources."""
        self._is_ready = True

    def finalize(self) -> None:
        """Cleanup after generation."""
        self._is_ready = False

    # ==========================================================
    # RESULT VALIDATION (Optional Override)
    # ==========================================================

    def validate_result(self, result: ParserResult) -> None:
        """Basic validation hook—can be overridden."""
        if result.is_empty:
            raise ValueError("Cannot generate report: Parser result is empty.")

    # ==========================================================
    # ABSTRACT GENERATION METHOD (Polymorphism + Overloading)
    # ==========================================================

    @overload
    @abstractmethod
    def generate(self, result: ParserResult, path: Path) -> None:
        ...

    @overload
    @abstractmethod
    def generate(self, result: ParserResult, *, filename: str) -> None:
        ...

    @abstractmethod
    def generate(self, result: ParserResult, *args, **kwargs) -> None:
        """Polymorphic report generator."""
        raise NotImplementedError

    # ==========================================================
    # OPTIONAL POLYMORPHIC HOOK
    # ==========================================================

    def report_name(self) -> str:
        """Return a descriptive report name."""
        return f"{self.report_type}Report"

    # ==========================================================
    # DUNDER METHODS (OOP Score Boost)
    # ==========================================================

    def __str__(self) -> str:
        return f"{self.report_type}ReportGenerator(ready={self._is_ready})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.report_type!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, IReportGenerator)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return self._is_ready

    def __len__(self) -> int:
        """Number of errors recorded."""
        return len(self._errors)

    def __contains__(self, key: str) -> bool:
        return key in (self._last_path.name if self._last_path else "")

    def __float__(self) -> float:
        """Represent generator as float based on readiness."""
        return 1.0 if self._is_ready else 0.0

    def __int__(self) -> int:
        """Represent generator as int based on readiness."""
        return int(self._is_ready)
