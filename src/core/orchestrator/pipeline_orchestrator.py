# USB PD Specification Parser - Pipeline Orchestrator Module
"""Simple pipeline orchestrator with OOP principles."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from src.config.config import Config
from src.support.output_writer import JSONLWriter
from src.core.extractors.pdf_extractor import PDFExtractor
from src.support.report_generator import ReportFactory
from src.core.extractors.toc_extractor import TOCExtractor


class BasePipeline(ABC):  # Abstraction
    def __init__(self, config_path: str):
        import logging

        self._logger = logging.getLogger(self.__class__.__name__)
        try:
            self._config = Config(config_path)  # Encapsulation
            self._logger.info(f"Configuration loaded successfully from {config_path}")
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        try:
            self._config.output_directory.mkdir(parents=True, exist_ok=True)
            self._logger.info(
                f"Output directory prepared: {self._config.output_directory}"
            )
        except (OSError, PermissionError) as e:
            raise RuntimeError(f"Cannot create output directory: {e}") from e

    @abstractmethod  # Abstraction
    def run(self, mode: int = 1) -> dict[str, Any]:
        pass


class PipelineOrchestrator(BasePipeline):  # Inheritance
    def run(self, mode: int = 1) -> dict[str, Any]:  # Polymorphism
        mode_names = {
            1: "Full Document",
            2: "Extended (600 pages)",
            3: "Standard (200 pages)",
        }
        self._logger.info(
            f"Starting pipeline execution - Mode: {mode_names.get(mode, 'Unknown')}"
        )

        if mode == 1:
            max_pages: Optional[int] = None
        elif mode == 2:
            max_pages = 600
        else:
            max_pages = 200

        # Extract
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

        # Write
        self._logger.info("Writing JSONL output files...")
        JSONLWriter(self._config.output_directory / "usb_pd_toc.jsonl").write(toc)
        JSONLWriter(self._config.output_directory / "usb_pd_spec.jsonl").write(content)
        self._logger.info("JSONL files written successfully")

        # Reports
        self._logger.info("Generating analysis reports...")
        counts = {
            "pages": len(content),
            "content_items": len(content),
            "toc_entries": len(toc),
            "paragraphs": sum(1 for item in content if item.get("type") == "paragraph"),
        }
        ReportFactory.create_generator("json", self._config.output_directory).generate(
            counts
        )
        ReportFactory.create_generator("excel", self._config.output_directory).generate(
            counts
        )
        self._logger.info("Analysis reports generated successfully")

        # Validation report
        self._logger.info("Generating validation report...")
        from src.support.validation_generator import create_validation_report

        create_validation_report(
            self._config.output_directory,
            self._config.output_directory / "usb_pd_toc.jsonl",
            self._config.output_directory / "usb_pd_spec.jsonl",
        )
        self._logger.info("Validation report generated successfully")
        self._logger.info("Pipeline execution completed successfully")

        return {"toc_entries": len(toc), "spec_counts": counts}

    def run_toc_only(self) -> Any:  # Polymorphism
        return TOCExtractor().extract_toc(self._config.pdf_input_file)

    def run_content_only(self) -> int:  # Polymorphism
        return len(PDFExtractor(self._config.pdf_input_file).extract_content())

    def run_full_pipeline(self, mode: int = 1) -> dict[str, Any]:  # Polymorphism
        return self.run(mode)
