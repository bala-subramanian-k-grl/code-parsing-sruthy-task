"""Orchestrator Interface Definitions"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Protocol


class DataExtractorInterface(Protocol):
    """Protocol for data extraction operations."""

    def extract_toc(self) -> list[Any]:
        """Extract Table of Contents."""
        ...

    def extract_content(self, max_pages: Optional[int] = None) -> list[Any]:
        """Extract content data."""
        ...

    def extract_data(
        self, max_pages: Optional[int]
    ) -> tuple[list[Any], list[Any]]:
        """Extract both TOC and content."""
        ...


class FileManagerInterface(Protocol):
    """Protocol for file management operations."""

    def write_toc_file(self, toc: list[Any]) -> None:
        """Write TOC file."""
        ...

    def write_spec_file(self, content: list[Any]) -> None:
        """Write specification file."""
        ...

    def write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write all files."""
        ...


class ReportManagerInterface(Protocol):
    """Protocol for report generation operations."""

    def generate_reports(
        self, toc: list[Any], content: list[Any]
    ) -> dict[str, Any]:
        """Generate all reports."""
        ...


class PipelineInterface(ABC):
    """Abstract interface for pipeline operations."""

    @abstractmethod
    def run(self) -> dict[str, Any]:
        """Execute pipeline."""

    @abstractmethod
    def run_toc_only(self) -> Any:
        """Extract TOC only."""

    @abstractmethod
    def run_content_only(self) -> int:
        """Extract content only."""
