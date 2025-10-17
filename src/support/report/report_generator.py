"""Minimal report generator with OOP principles."""


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class ProcessableMixin:
    """Mixin for processable objects."""

    def process(self) -> Any:
        """Process the object."""
        return None

    def validate(self) -> bool:
        """Validate the object."""
        return True


class TransformableMixin:
    """Mixin for transformable objects."""

    def transform(self, data: Any) -> Any:
        """Transform data."""
        return data

    def serialize(self) -> str:
        """Serialize object."""
        return ""


class BaseReportGenerator(ABC, ProcessableMixin, TransformableMixin):
    def __init__(self, output_dir: Path):
        self.__output_dir = output_dir  # Private encapsulation
        self.__metadata: dict[str, Any] = {}  # Private metadata
        self.__output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def generate(self, data: dict[str, Any]) -> Path:
        """Generate report."""
        pass

    def process(self) -> Any:
        """Process report generation."""
        return self.generate({})

    def validate(self) -> bool:
        """Validate report configuration."""
        return self.__output_dir.exists()

    def transform(self, data: Any) -> Any:
        """Transform data for report."""
        return data

    def serialize(self) -> str:
        """Serialize report metadata."""
        return str(self.__metadata)

    @property
    def output_dir(self) -> Path:
        """Get output directory."""
        return self.__output_dir


class ReportFactory:  # Factory pattern
    __ALLOWED_TYPES = {"json", "excel"}  # Private authorized types

    @staticmethod
    def create_generator(
        report_type: str, output_dir: Path
    ) -> BaseReportGenerator:
        # Validate and sanitize input
        if not report_type.strip():
            raise ValueError("Report type must be a non-empty string")

        clean_type = report_type.strip().lower()
        if clean_type not in ReportFactory.__ALLOWED_TYPES:
            raise ValueError(f"Unauthorized report type: {report_type}")

        if clean_type == "json":
            from .jsonreport_generator import JSONReportGenerator

            return JSONReportGenerator(output_dir)  # Polymorphism
        elif clean_type == "excel":
            from .excel_report import ExcelReportGenerator

            return ExcelReportGenerator(output_dir)
        raise ValueError(f"Invalid report type: {report_type}")

    @staticmethod
    def get_supported_types() -> set[str]:
        """Get supported report types."""
        return ReportFactory.__ALLOWED_TYPES.copy()
