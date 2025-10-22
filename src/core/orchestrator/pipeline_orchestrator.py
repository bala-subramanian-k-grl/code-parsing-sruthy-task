"""USB PD Specification Parser - Pipeline Orchestrator Module"""

from typing import Any, Optional

from src.config.config import Config
from src.config.constants import USB_PD_SPEC_FILE, USB_PD_TOC_FILE
from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor
from src.core.extractors.strategies.extraction_strategy import (
    ComprehensiveStrategy,
)
from src.core.extractors.tocextractor.toc_extractor import TOCExtractor
from src.core.orchestrator.base_pipeline import BasePipeline
from src.support.output_writer import JSONLWriter
from src.support.report.report_generator import ReportFactory
from src.utils.decorators import log_execution, timing


class PipelineOrchestrator(BasePipeline):  # Inheritance
    def __init__(self, config_path: str):
        """Initialize pipeline orchestrator with configuration."""
        import logging

        class_name = self.__class__.__name__
        self.__logger = logging.getLogger(class_name)  # Private
        try:
            self.__config = Config(config_path)  # Private
            self.__logger.info("Configuration loaded from %s", config_path)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        try:
            output_dir = self.__config.output_directory
            output_dir.mkdir(parents=True, exist_ok=True)
            msg = f"Output directory prepared: {output_dir}"
            self.__logger.info(msg)
        except OSError as e:
            msg = f"Cannot create output directory: {e}"
            raise RuntimeError(msg) from e

    @property
    def config(self) -> Config:
        """Get configuration (read-only access)."""
        return self.__config

    @property
    def logger(self):
        """Get logger (read-only access)."""
        return self.__logger

    def _get_max_pages(self) -> Optional[int]:
        """Get max pages for processing."""
        return None  # Process all pages

    def _calculate_counts(
        self, toc: list[Any], content: list[Any]
    ) -> dict[str, Any]:
        """Calculate enhanced content statistics."""
        from src.core.analyzer.content_analyzer import ContentAnalyzer

        analyzer = ContentAnalyzer()

        major_sections = sum(
            1
            for item in content
            if analyzer.is_major_section(item.get("content", ""))
        )

        # Remove key terms counting - not needed

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

    def _create_analysis_reports(self, counts: dict[str, Any]) -> None:
        """Create JSON and Excel analysis reports."""
        output_dir = self.__config.output_directory
        json_gen = ReportFactory.create_generator("json", output_dir)
        json_gen.generate(counts)
        excel_gen = ReportFactory.create_generator("excel", output_dir)
        excel_gen.generate(counts)

    def _create_validation_report(self) -> None:
        """Create validation report."""
        from src.support.validation_generator import create_validation_report

        output_dir = self.__config.output_directory
        create_validation_report(
            output_dir,
            output_dir / USB_PD_TOC_FILE,
            output_dir / USB_PD_SPEC_FILE,
        )

    def _create_metadata_file(self) -> None:
        """Create metadata file."""
        from src.support.metadata_generator import create_metadata_file

        output_dir = self.__config.output_directory
        spec_file = output_dir / USB_PD_SPEC_FILE
        create_metadata_file(output_dir, spec_file)

    def _extract_data(
        self, max_pages: Optional[int]
    ) -> tuple[list[Any], list[Any]]:
        """Extract TOC and content data using Strategy Pattern."""
        self.__logger.info("Extracting Table of Contents...")
        pdf_file = self.__config.pdf_input_file
        toc = TOCExtractor().extract_toc(pdf_file)
        toc_count = len(toc)
        msg = f"TOC extraction completed: {toc_count} entries"
        self.__logger.info(msg)

        pages_info = max_pages or "all"
        msg = "Extracting content (max pages: %s)..."
        self.__logger.info(msg, pages_info)

        # Use Strategy Pattern for comprehensive extraction
        strategy = ComprehensiveStrategy()
        content = list(strategy.extract_pages(pdf_file, max_pages))
        count = len(content)
        self.__logger.info("Content extraction completed: %s items", count)
        return toc, content

    def _write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write JSONL output files."""
        self.__logger.info("Writing JSONL output files...")
        output_dir = self.__config.output_directory

        # Write TOC and spec files
        toc_path = output_dir / USB_PD_TOC_FILE
        toc_writer = JSONLWriter(toc_path)
        toc_writer.write(toc)
        spec_path = output_dir / USB_PD_SPEC_FILE
        spec_writer = JSONLWriter(spec_path)
        spec_writer.write(content)

        self.__logger.info("JSONL files written successfully")

    def _generate_reports(
        self, toc: list[Any], content: list[Any]
    ) -> dict[str, Any]:
        """Generate analysis and validation reports."""
        self.__logger.info("Generating analysis reports...")
        counts = self._calculate_counts(toc, content)
        self._create_analysis_reports(counts)
        self.__logger.info("Analysis reports generated successfully")

        self.__logger.info("Generating validation report...")
        self._create_validation_report()
        self.__logger.info("Validation report generated successfully")

        self.__logger.info("Generating metadata file...")
        self._create_metadata_file()
        self.__logger.info("Metadata file generated successfully")
        return counts

    def _get_mode_name(self) -> str:
        """Get mode name for logging."""
        return "Full Document Processing"

    @timing
    @log_execution
    def run(self) -> dict[str, Any]:  # Polymorphism
        mode_name = self._get_mode_name()
        msg = "Starting pipeline execution - %s"
        self.__logger.info(msg, mode_name)

        max_pages = self._get_max_pages()
        toc, content = self._extract_data(max_pages)
        self._write_files(toc, content)
        counts = self._generate_reports(toc, content)

        msg = "Pipeline execution completed successfully"
        self.__logger.info(msg)
        return {"toc_entries": len(toc), "spec_counts": counts}

    def run_toc_only(self) -> Any:  # Polymorphism
        return TOCExtractor().extract_toc(self.__config.pdf_input_file)

    def run_content_only(self) -> int:  # Polymorphism
        extractor = PDFExtractor(self.__config.pdf_input_file)
        return len(extractor.extract_content())

    def run_full_pipeline(self) -> dict[str, Any]:
        """Run full pipeline - Polymorphism."""
        return self.run()
