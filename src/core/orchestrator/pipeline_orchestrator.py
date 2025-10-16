"""USB PD Specification Parser - Pipeline Orchestrator Module"""

from typing import Any, Optional

from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor
from src.core.extractors.tocextractor.toc_extractor import TOCExtractor
from src.core.orchestrator.base_pipeline import BasePipeline  # Inheritance
from src.support.output_writer import JSONLWriter
from src.support.report.report_generator import ReportFactory
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

    def _extract_data(self, max_pages: Optional[int]) -> tuple[list[Any], list[Any]]:
        """Extract TOC and content data."""
        self._logger.info("Extracting Table of Contents...")
        toc = TOCExtractor().extract_toc(self._config.pdf_input_file)
        self._logger.info(f"TOC extraction completed: {len(toc)} entries found")

        self._logger.info(
            f"Extracting content from PDF (max pages: {max_pages or 'all'})..."
        )
        content = PDFExtractor(self._config.pdf_input_file).extract_content(max_pages)
        self._logger.info(
            f"Content extraction completed: {len(content)} items processed"
        )
        return toc, content

    def _write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write JSONL output files."""
        self._logger.info("Writing JSONL output files...")
        JSONLWriter(self._config.output_directory / "usb_pd_toc.jsonl").write(toc)
        JSONLWriter(self._config.output_directory / "usb_pd_spec.jsonl").write(content)
        self._logger.info("JSONL files written successfully")

    def _generate_reports(self, toc: list[Any], content: list[Any]) -> dict[str, Any]:
        """Generate analysis and validation reports."""
        self._logger.info("Generating analysis reports...")
        counts = {
            "pages": len(content),
            "content_items": len(content),
            "toc_entries": len(toc),
            "paragraphs": sum(1 for item in content if item.get("type") == "paragraph"),
        }
        json_gen = ReportFactory.create_generator("json", self._config.output_directory)
        json_gen.generate(counts)
        excel_gen = ReportFactory.create_generator("excel", self._config.output_directory)
        excel_gen.generate(counts)
        self._logger.info("Analysis reports generated successfully")

        self._logger.info("Generating validation report...")
        from src.support.validation_generator import create_validation_report

        create_validation_report(
            self._config.output_directory,
            self._config.output_directory / "usb_pd_toc.jsonl",
            self._config.output_directory / "usb_pd_spec.jsonl",
        )
        self._logger.info("Validation report generated successfully")
        return counts

    @timing
    @log_execution
    def run(self, mode: int = 1) -> dict[str, Any]:  # Polymorphism
        mode_names = {
            1: "Full Document",
            2: "Extended (600 pages)",
            3: "Standard (200 pages)",
        }
        self._logger.info(
            f"Starting pipeline execution - Mode: {mode_names.get(mode, 'Unknown')}"
        )

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
