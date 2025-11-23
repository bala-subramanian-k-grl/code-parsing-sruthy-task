"""Pipeline orchestrator for coordinating extraction."""

from __future__ import annotations
from pathlib import Path
from typing import Union

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.core.interfaces.pipeline_interface import (
    PipelineInterface,
    ValidationResult,
)
from src.parser.pdf_parser import PDFParser
from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.support.metadata_generator import MetadataGenerator
from src.utils.logger import logger
from src.writers.jsonl_writer import JSONLWriter


class PipelineOrchestrator(PipelineInterface):
    """Orchestrates the entire parsing pipeline."""

    # ---------------------------------------------------------
    # INITIALIZATION (ENCAPSULATION)
    # ---------------------------------------------------------
    def __init__(
        self,
        file_path: Path,
        mode: ParserMode,
        config: Union[ConfigLoader, None] = None,
    ) -> None:
        
        self.__file_path = file_path
        self.__mode = mode
        self.__config = config or ConfigLoader()

        self.__output_dir = self.__config.get_output_dir()
        self.__doc_title = self.__config.get_doc_title()

        self.__toc_filename = "usb_pd_toc.jsonl"
        self.__content_filename = "usb_pd_spec.jsonl"

    # ---------------------------------------------------------
    # REQUIRED INTERFACE PROPERTIES (POLYMORPHISM)
    # ---------------------------------------------------------
    @property
    def pipeline_type(self) -> str:
        return "USBPD-Pipeline"

    @property
    def is_async(self) -> bool:
        return False

    # ---------------------------------------------------------
    # ENCAPSULATED ATTRIBUTES
    # ---------------------------------------------------------
    @property
    def file_path(self) -> Path:
        return self.__file_path

    @property
    def mode(self) -> ParserMode:
        return self.__mode

    @property
    def output_dir(self) -> Path:
        return self.__output_dir

    @property
    def doc_title(self) -> str:
        return self.__doc_title

    @property
    def toc_filename(self) -> str:
        return self.__toc_filename

    @property
    def content_filename(self) -> str:
        return self.__content_filename

    @property
    def file_exists(self) -> bool:
        return self.__file_path.exists()

    @property
    def output_exists(self) -> bool:
        return self.__output_dir.exists()

    @property
    def file_name(self) -> str:
        return self.__file_path.name

    # ---------------------------------------------------------
    # PREPARE (REQUIRED BY INTERFACE)
    # ---------------------------------------------------------
    def prepare(self) -> None:
        """Prepare output directory."""
        if not self.__output_dir.exists():
            self.__output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created output directory → {self.__output_dir}")

    # ---------------------------------------------------------
    # VALIDATION (OVERRIDE)
    # ---------------------------------------------------------
    def validate(self) -> ValidationResult:
        """Validate pipeline configuration."""
        errors: list[str] = []

        if not self.__file_path.exists():
            errors.append(f"File not found: {self.__file_path}")

        if self.__file_path.suffix.lower() != ".pdf":
            errors.append(f"Invalid file type: {self.__file_path.suffix}")

        return ValidationResult(is_valid=(not errors), errors=errors)

    def _validate_pipeline(self) -> None:
        """Internal validator wrapper."""
        validation = self.validate()
        if not validation.is_valid:
            raise ValueError(
                f"Pipeline validation failed: {', '.join(validation.errors)}"
            )

    # ---------------------------------------------------------
    # EXECUTE (REQUIRED BY INTERFACE)
    # ---------------------------------------------------------
    def execute(self) -> ParserResult:
        """Execute entire pipeline."""
        self.prepare()
        self._validate_pipeline()

        try:
            result = self._parse_document()
            self._write_outputs(result)
            self._generate_reports(result)
            logger.info("Pipeline execution completed successfully")

            return result

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            raise

        finally:
            self.cleanup()

    # ---------------------------------------------------------
    # CLEANUP (REQUIRED BY INTERFACE)
    # ---------------------------------------------------------
    def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Pipeline cleanup complete")

    # ---------------------------------------------------------
    # INTERNAL PROCESSING METHODS (ENCAPSULATED)
    # ---------------------------------------------------------
    def _parse_document(self) -> ParserResult:
        """Parse PDF document."""
        logger.info("Starting PDF parsing")
        parser = PDFParser(self.__file_path, self.__doc_title)
        return parser.parse()

    def _write_outputs(self, result: ParserResult) -> None:
        """Write output files."""
        logger.info("Writing JSONL files")

        writer = JSONLWriter(self.__doc_title)

        writer.write_toc(
            result.toc_entries,
            self.__output_dir / self.__toc_filename,
        )
        writer.write_content(
            result.content_items,
            self.__output_dir / self.__content_filename,
        )

    def _generate_reports(self, result: ParserResult) -> None:
        """Generate metadata, JSON, and Excel reports."""
        MetadataGenerator().generate(
            result, self.__output_dir / "usb_pd_metadata.jsonl"
        )
        JSONReportGenerator().generate(
            result, self.__output_dir / "parsing_report.json",
        )
        ExcelReportGenerator().generate(
            result, self.__output_dir / "validation_report.xlsx",
        )

    # ---------------------------------------------------------
    # MAGIC METHODS (UNCHANGED)
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"PipelineOrchestrator(file={self.__file_path.name}, mode={self.__mode.value})"

    def __repr__(self) -> str:
        return f"PipelineOrchestrator(file_path={self.__file_path!r}, mode={self.__mode!r})"
