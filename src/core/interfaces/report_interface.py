"""
Report generator interface with abstraction and encapsulation.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

from src.core.config.models import ParserResult


class IReportGenerator(ABC):
    """Interface for all report generators."""

    # ------------------------ PROPERTIES (ENCAPSULATION) ------------------------

    @property
    @abstractmethod
    def report_type(self) -> str:
        """
        Encapsulated property: return report type name.
        Example: "PDF", "HTML"
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def output_extension(self) -> str:
        """
        Encapsulated property: return output file extension.
        Example: ".pdf", ".html"
        """
        raise NotImplementedError

    # ------------------------ MAIN ABSTRACT METHOD ------------------------------

    @abstractmethod
    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate report from parser result."""
        raise NotImplementedError

    # ------------------------ MINIMAL OPTIONAL HOOK -----------------------------

    def validate_result(self, result: ParserResult) -> None:
        """
        Small validation hook (encapsulation).
        Not abstract—optional override.
        """
        if result.is_empty:
            raise ValueError("Cannot generate report: Result is empty.")
