"""USB PD Specification Parser - Pipeline Orchestrator Module"""

from typing import Any, Optional

from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor
from src.core.extractors.tocextractor.toc_extractor import TOCExtractor
from src.core.extractors.strategies.extraction_strategy import (
    ComprehensiveStrategy,
)
from src.core.orchestrator.base_pipeline import BasePipeline
from src.support.output_writer import JSONLWriter
from src.support.report.report_generator import ReportFactory
from src.support.factories.file_factory import FileGeneratorFactory
from src.utils.decorators import log_execution, timing


class PipelineOrchestrator(BasePipeline):  # Inheritance
    def _get_max_pages(self, mode: int) -> Optional[int]:
        """Get max pages based on mode."""
        if mode == 1:
            return None
        elif mode == 2:
            return 600
        else:
            return 200

    def _extract_data(
        self, max_pages: Optional[int]
    ) -> tuple[list[Any], list[Any]]:
        """Extract TOC and content data using Strategy Pattern."""
        self._logger.info("Extracting Table of Contents...")
        pdf_file = self._config.pdf_input_file
        toc = TOCExtractor().extract_toc(pdf_file)
        self._logger.info(
            f"TOC extraction completed: {len(toc)} entries found"
        )

        max_pages_str = max_pages or 'all'
        msg = f"Extracting content from PDF (max pages: {max_pages_str})..."
        self._logger.info(msg)
        
        # Use Strategy Pattern for comprehensive extraction
        strategy = ComprehensiveStrategy()
        content = list(strategy.extract_pages(pdf_file, max_pages))
        count = len(content)
        self._logger.info(f"Content extraction completed: {count} items")
        return toc, content

    def _write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write JSONL output files including metadata."""
        self._logger.info("Writing JSONL output files...")
        output_dir = self._config.output_directory
        
        # Write TOC and spec files
        toc_path = output_dir / "usb_pd_toc.jsonl"
        toc_writer = JSONLWriter(toc_path)
        toc_writer.write(toc)
        spec_path = output_dir / "usb_pd_spec.jsonl"
        spec_writer = JSONLWriter(spec_path)
        spec_writer.write(content)
        
        # Generate missing metadata file using Factory Pattern
        metadata_path = output_dir / "usb_pd_metadata.jsonl"
        factory = FileGeneratorFactory
        metadata_gen = factory.create_generator("metadata")
        metadata_gen.generate(content, metadata_path)
        
        self._logger.info("JSONL files written successfully")

    def _calculate_counts(
        self, toc: list[Any], content: list[Any]
    ) -> dict[str, Any]:
        """Calculate content statistics."""
        return {
            "pages": len(content),
            "content_items": len(content),
            "toc_entries": len(toc),
            "paragraphs": sum(
                1 for item in content if item.get("type") == "paragraph"
            ),
        }

    def _create_analysis_reports(self, counts: dict[str, Any]) -> None:
        """Create JSON and Excel analysis reports."""
        output_dir = self._config.output_directory
        json_gen = ReportFactory.create_generator("json", output_dir)
        json_gen.generate(counts)
        excel_gen = ReportFactory.create_generator("excel", output_dir)
        excel_gen.generate(counts)

    def _create_validation_report(self) -> None:
        """Create validation report."""
        from src.support.validation_generator import create_validation_report

        output_dir = self._config.output_directory
        create_validation_report(
            output_dir,
            output_dir / "usb_pd_toc.jsonl",
            output_dir / "usb_pd_spec.jsonl",
        )

    def _generate_reports(self, toc: list[Any], content: list[Any]) -> dict[str, Any]:
        """Generate analysis and validation reports."""
        self._logger.info("Generating analysis reports...")
        counts = self._calculate_counts(toc, content)
        self._create_analysis_reports(counts)
        self._logger.info("Analysis reports generated successfully")

        self._logger.info("Generating validation report...")
        self._create_validation_report()
        self._logger.info("Validation report generated successfully")
        return counts

    def _get_mode_name(self, mode: int) -> str:
        """Get mode name for logging."""
        mode_names = {
            1: "Full Document",
            2: "Extended (600 pages)",
            3: "Standard (200 pages)",
        }
        return mode_names.get(mode, "Unknown")

    @timing
    @log_execution
    def run(self, mode: int = 1) -> dict[str, Any]:  # Polymorphism
        mode_name = self._get_mode_name(mode)
        msg = f"Starting pipeline execution - Mode: {mode_name}"
        self._logger.info(msg)
        
        max_pages = self._get_max_pages(mode)
        toc, content = self._extract_data(max_pages)
        self._write_files(toc, content)
        counts = self._generate_reports(toc, content)
        
        self._logger.info("Pipeline execution completed successfully")
        return {"toc_entries": len(toc), "spec_counts": counts}

    def run_toc_only(self) -> Any:  # Polymorphism
        return TOCExtractor().extract_toc(self._config.pdf_input_file)

    def run_content_only(self) -> int:  # Polymorphism
        return len(PDFExtractor(self._config.pdf_input_file).extract_content())

    def run_full_pipeline(self, mode: int = 1) -> dict[str, Any]:  # Polymorphism
        return self.run(mode)
