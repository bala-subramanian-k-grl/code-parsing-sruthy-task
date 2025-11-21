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

    @property
    def toc_filename(self) -> str:
        """Get TOC filename."""
        return self.__toc_filename

    @property
    def content_filename(self) -> str:
        """Get content filename."""
        return self.__content_filename

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self.__file_path.exists()

    @property
    def output_exists(self) -> bool:
        """Check if output dir exists."""
        return self.__output_dir.exists()

    @property
    def file_name(self) -> str:
        """Get file name."""
        return self.__file_path.name

    def execute(self) -> ParserResult:
        """Execute pipeline."""
        self._validate_pipeline()

        try:
            result = self._parse_document()
            self._write_outputs(result)
            self._generate_reports(result)
            logger.info("Pipeline execution completed")
            return result
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            raise

    def _validate_pipeline(self) -> None:
        """Validate pipeline configuration."""
        validation = self.validate()
        if not validation.is_valid:
            raise ValueError(
                f"Pipeline validation failed: {', '.join(validation.errors)}"
            )

    def _parse_document(self) -> ParserResult:
        """Parse PDF document."""
        logger.info("Starting PDF parsing")
        parser = PDFParser(self.__file_path, self.__doc_title)
        return parser.parse()

    def _write_outputs(self, result: ParserResult) -> None:
        """Write output files."""
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PipelineOrchestrator):
            return NotImplemented
        return self.__file_path == other.__file_path and self.__mode == other.__mode

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path, self.__mode))

    def __len__(self) -> int:
        return 2

    def __bool__(self) -> bool:
        return self.__file_path.exists()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PipelineOrchestrator):
            return NotImplemented
        return str(self.__file_path) < str(other.__file_path)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, text: str) -> bool:
        """Check if text in file path."""
        return text in str(self.__file_path)

    def __int__(self) -> int:
        """Get number of output files."""
        return 2

    def __float__(self) -> float:
        """Get number of output files as float."""
        return 2.0
