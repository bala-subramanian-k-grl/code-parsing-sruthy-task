"""Pipeline orchestrator for coordinating extraction."""

from pathlib import Path
from typing import Union

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.core.interfaces.pipeline_interface import (PipelineInterface,
                                                    ValidationResult)
from src.parser.pdf_parser import PDFParser
from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.support.metadata_generator import MetadataGenerator
from src.utils.logger import logger
from src.writers.jsonl_writer import JSONLWriter


class PipelineOrchestrator(PipelineInterface):
    """Orchestrates the entire parsing pipeline."""

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

    @property
    def file_path(self) -> Path:
        """Get file path."""
        return self.__file_path

    @property
    def mode(self) -> ParserMode:
        """Get parser mode."""
        return self.__mode

    @property
    def output_dir(self) -> Path:
        """Get output directory."""
        return self.__output_dir

    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self.__doc_title

    def execute(self) -> ParserResult:
        """Execute pipeline."""
        validation = self.validate()
        if not validation.is_valid:
            raise ValueError(
                f"Pipeline validation failed: {', '.join(validation.errors)}"
            )

        try:
            logger.info("Starting PDF parsing")
            parser = PDFParser(self.__file_path, self.__doc_title)
            result: ParserResult = parser.parse()

            logger.info("Writing output files")
            writer = JSONLWriter(self.__doc_title)
            writer.write_toc(
                result.toc_entries,
                self.__output_dir / self.__toc_filename
            )
            writer.write_content(
                result.content_items,
                self.__output_dir / self.__content_filename
            )

            logger.info("Generating reports")
            self._generate_reports(result)
            logger.info("Pipeline execution completed")

            return result
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            raise

    def validate(self) -> ValidationResult:
        """Validate pipeline configuration."""
        errors: list[str] = []
        if not self.__file_path.exists():
            errors.append(f"File not found: {self.__file_path}")
        if self.__file_path.suffix != ".pdf":
            errors.append(f"Invalid file type: {self.__file_path.suffix}")
        return ValidationResult(is_valid=not errors, errors=errors)

    def _generate_reports(self, result: ParserResult) -> None:
        """Generate metadata, JSON, and Excel reports from parser result."""
        MetadataGenerator().generate(
            result, self.__output_dir / "usb_pd_metadata.jsonl"
        )
        JSONReportGenerator().generate(
            result, self.__output_dir / "parsing_report.json"
        )
        ExcelReportGenerator().generate(
            result, self.__output_dir / "validation_report.xlsx"
        )

    def __str__(self) -> str:
        """String representation."""
        return f"PipelineOrchestrator(file={self.__file_path.name}, mode={self.__mode.value})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"PipelineOrchestrator(file_path={self.__file_path!r}, mode={self.__mode!r})"
