"""Minimal report generator with OOP principles."""


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional


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
        self.__generation_count: int = 0  # Private counter
        self.__last_generated: Optional[Path] = None  # Private tracking
        self._setup_output_directory()

    def _setup_output_directory(self) -> None:
        """Protected method to setup output directory."""
        self.__output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def generate(self, data: dict[str, Any]) -> Path:
        """Generate report."""

    @abstractmethod
    def get_report_type(self) -> str:
        """Get report type name."""

    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension for this report type."""

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

    @property
    def generation_count(self) -> int:
        """Get number of reports generated."""
        return self.__generation_count

    @property
    def last_generated_file(self) -> Optional[Path]:
        """Get last generated file path."""
        return self.__last_generated

    def _increment_generation_count(self) -> None:
        """Increment generation counter."""
        self.__generation_count += 1

    def _set_last_generated(self, file_path: Path) -> None:
        """Set last generated file path."""
        self.__last_generated = file_path

    def _add_metadata(self, key: str, value: Any) -> None:
        """Add metadata entry."""
        self.__metadata[key] = value

    def _get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.__metadata.get(key, default)

    def _clear_metadata(self) -> None:
        """Clear all metadata."""
        self.__metadata.clear()

    def __str__(self) -> str:  # Magic method
        """String representation."""
        return f"{self.__class__.__name__}({self.__output_dir.name})"

    def __call__(self, data: dict[str, Any]) -> Path:  # Magic method
        """Make generator callable."""
        return self.generate(data)


class ReportFactory:  # Factory pattern
    __ALLOWED_TYPES = {"json", "excel", "html"}  # Private authorized types
    __INSTANCE_CACHE: dict[str, BaseReportGenerator] = {}  # Private cache

    @staticmethod
    def create_generator(
        report_type: str, output_dir: Path
    ) -> BaseReportGenerator:
        clean_type = ReportFactory._validate_and_clean_type(report_type)
        return ReportFactory._create_specific_generator(clean_type, output_dir)

    @staticmethod
    def _validate_and_clean_type(report_type: str) -> str:
        """Protected method to validate and clean report type."""
        if not report_type.strip():
            raise ValueError("Report type must be a non-empty string")

        clean_type = report_type.strip().lower()
        if clean_type not in ReportFactory.__ALLOWED_TYPES:
            raise ValueError(f"Unauthorized report type: {report_type}")
        return clean_type

    @staticmethod
    def _create_specific_generator(
        clean_type: str, output_dir: Path
    ) -> BaseReportGenerator:
        """Protected method to create generator instance."""
        if clean_type == "json":
            from .jsonreport_generator import JSONReportGenerator

            return JSONReportGenerator(output_dir)
        if clean_type == "excel":
            from .excel_report import ExcelReportGenerator

            return ExcelReportGenerator(output_dir)
        raise ValueError(f"Invalid report type: {clean_type}")

    @staticmethod
    def get_supported_types() -> set[str]:
        """Get supported report types."""
        return ReportFactory.__ALLOWED_TYPES.copy()

    @staticmethod
    def create_cached_generator(
        report_type: str, output_dir: Path
    ) -> BaseReportGenerator:
        """Create generator with caching."""
        cache_key = f"{report_type}_{output_dir}"
        if cache_key not in ReportFactory.__INSTANCE_CACHE:
            generator = ReportFactory.create_generator(report_type, output_dir)
            ReportFactory.__INSTANCE_CACHE[cache_key] = generator
        return ReportFactory.__INSTANCE_CACHE[cache_key]

    @staticmethod
    def clear_cache() -> None:
        """Clear generator cache."""
        ReportFactory.__INSTANCE_CACHE.clear()

    @staticmethod
    def _get_cache_size() -> int:
        """Get current cache size."""
        return len(ReportFactory.__INSTANCE_CACHE)
