"""USB PD Specification Parser - Report Management Module"""

from typing import Any

from src.config.config import Config
from src.config.constants import USB_PD_SPEC_FILE, USB_PD_TOC_FILE
from src.core.analyzer.content_analyzer import ContentAnalyzer
from src.support.metadata_generator import create_metadata_file
from src.support.report.report_generator import ReportFactory
from src.support.validation_generator import create_validation_report


class ReportManager:  # Encapsulation + Interface Implementation
    """Manages all report generation operations."""

    def __init__(self, config: Config, logger: Any):
        """Initialize report manager with dependencies."""
        if not config:
            raise ValueError("Config cannot be None")
        if not logger:
            raise ValueError("Logger cannot be None")

        self.__config = config  # Private
        self.__logger = logger  # Private

    def __calculate_counts(
        self, toc: list[Any], content: list[Any]
    ) -> dict[str, Any]:
        """Calculate enhanced content statistics."""
        if not toc or not content:
            raise ValueError("TOC and content cannot be empty")

        analyzer = ContentAnalyzer()

        major_sections = sum(
            1
            for item in content
            if analyzer.is_major_section(item.get("content", ""))
        )

        return {
            "pages": len({item.get("page", 0) for item in content}),
            "content_items": len(content),
            "toc_entries": len(toc),
            "major_sections": major_sections,
            "key_terms": 0,
            "paragraphs": sum(
                1 for item in content if item.get("type") == "paragraph"
            ),
        }

    def __create_analysis_reports(self, counts: dict[str, Any]) -> None:
        """Create JSON and Excel analysis reports."""
        output_dir = self.__config.output_directory
        json_gen = ReportFactory.create_generator("json", output_dir)
        json_gen.generate(counts)
        excel_gen = ReportFactory.create_generator("excel", output_dir)
        excel_gen.generate(counts)

    def __create_validation_report(self) -> None:
        """Create validation report."""
        output_dir = self.__config.output_directory
        create_validation_report(
            output_dir,
            output_dir / USB_PD_TOC_FILE,
            output_dir / USB_PD_SPEC_FILE,
        )

    def __create_metadata_file(self) -> None:
        """Create metadata file."""
        output_dir = self.__config.output_directory
        spec_file = output_dir / USB_PD_SPEC_FILE
        create_metadata_file(output_dir, spec_file)

    def generate_reports(
        self, toc: list[Any], content: list[Any]
    ) -> dict[str, Any]:
        """Generate all analysis and validation reports."""
        self.__logger.info("Generating analysis reports...")
        counts = self.__calculate_counts(toc, content)
        self.__create_analysis_reports(counts)
        self.__logger.info("Analysis reports generated successfully")

        self.__logger.info("Generating validation report...")
        self.__create_validation_report()
        self.__logger.info("Validation report generated successfully")

        self.__logger.info("Generating metadata file...")
        self.__create_metadata_file()
        self.__logger.info("Metadata file generated successfully")
        return counts
