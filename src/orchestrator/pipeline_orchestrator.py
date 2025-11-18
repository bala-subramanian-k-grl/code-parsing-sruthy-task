"""Pipeline orchestrator for coordinating extraction."""

import json
from pathlib import Path
from typing import Union

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ContentItem, ParserResult, TOCEntry
from src.core.interfaces.pipeline_interface import (PipelineInterface,
                                                    ValidationResult)
from src.parser.pdf_parser import PDFParser
from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.support.metadata_generator import MetadataGenerator
from src.utils.logger import logger


class PipelineOrchestrator(PipelineInterface):
    """Orchestrates the entire parsing pipeline."""

    def __init__(
        self,
        file_path: Path,
        mode: ParserMode,
        config: Union[ConfigLoader, None] = None,
        toc_filename: str = "usb_pd_toc.jsonl",
        content_filename: str = "usb_pd_spec.jsonl",
    ) -> None:

        self._file_path = file_path
        self._mode = mode
        self._config = config or ConfigLoader()
        self._output_dir = self._config.get_output_dir()
        self._doc_title = self._config.get_doc_title()
        self._toc_filename = toc_filename
        self._content_filename = content_filename

    def execute(self) -> ParserResult:
        """Execute pipeline."""
        validation = self.validate()
        if not validation.is_valid:
            raise ValueError(
                f"Pipeline validation failed: {', '.join(validation.errors)}"
            )

        try:
            logger.info("Starting PDF parsing")
            parser = PDFParser(self._file_path, self._doc_title)
            result: ParserResult = parser.parse()

            logger.info("Writing output files")
            self._output_dir.mkdir(exist_ok=True)
            self._write_toc(result.toc_entries)
            self._write_content(result.content_items)

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
        if not self._file_path.exists():
            errors.append(f"File not found: {self._file_path}")
        if self._file_path.suffix != ".pdf":
            errors.append(f"Invalid file type: {self._file_path.suffix}")
        return ValidationResult(is_valid=not errors, errors=errors)

    def _write_toc(self, entries: list[TOCEntry]) -> None:
        """Write table of contents entries to JSONL file."""
        path = self._output_dir / self._toc_filename
        with path.open("w", encoding="utf-8") as f:
            for entry in entries:
                json_data = json.dumps({
                    "doc_title": self._doc_title,
                    "section_id": entry.section_id,
                    "title": entry.title,
                    "full_path": entry.title,
                    "page": entry.page,
                    "level": entry.level,
                    "parent_id": entry.parent_id,
                    "tags": [],
                })
                f.write(f"{json_data}\n")

    def _write_content(self, items: list[ContentItem]) -> None:
        """Write content items to JSONL file."""
        path = self._output_dir / self._content_filename
        with path.open("w", encoding="utf-8") as f:
            for item in items:
                json_data = json.dumps({
                    "doc_title": item.doc_title,
                    "section_id": item.section_id,
                    "title": item.title,
                    "content": item.content,
                    "page": item.page,
                    "level": item.level,
                    "parent_id": item.parent_id,
                    "full_path": item.full_path,
                    "type": item.content_type,
                    "block_id": item.block_id,
                    "bbox": item.bbox,
                })
                f.write(f"{json_data}\n")

    def _generate_reports(self, result: ParserResult) -> None:
        """Generate metadata, JSON, and Excel reports from parser result."""
        MetadataGenerator().generate(
            result, self._output_dir / "usb_pd_metadata.jsonl"
        )
        JSONReportGenerator().generate(
            result, self._output_dir / "parsing_report.json"
        )
        ExcelReportGenerator().generate(
            result, self._output_dir / "validation_report.xlsx"
        )
