"""
Enterprise Pipeline Orchestrator (OOP-Optimized + Overloading Added)
"""

from __future__ import annotations

from pathlib import Path
from typing import overload

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.core.interfaces.pipeline_interface import (PipelineInterface,
                                                    ValidationResult)
from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.support.metadata_generator import MetadataGenerator
from src.utils.logger import logger
from src.writers.jsonl_writer import JSONLWriter


class PipelineOrchestrator(PipelineInterface):
    """Main enterprise pipeline orchestrator."""

    # ==========================================================
    # INIT (ENCAPSULATION)
    # ==========================================================
    def __init__(
        self,
        file_path: Path,
        mode: ParserMode,
        config: ConfigLoader | None = None,
    ) -> None:

        self.__file_path = file_path
        self.__mode = mode
        self.__config = config or ConfigLoader()

        # Encapsulated config values
        output_cfg = self.__config.get("output", {})
        self.__output_dir = Path(output_cfg.get("base_dir", "outputs"))
        meta_cfg = self.__config.get("metadata", {})
        self.__doc_title = str(meta_cfg.get("doc_title", "Document"))

        # Counters
        self.__exec_count = 0
        self.__success = 0
        self.__errors = 0

        # Filenames
        self._toc_name = "usb_pd_toc.jsonl"
        self._content_name = "usb_pd_spec.jsonl"

    # ==========================================================
    # PROPERTIES
    # ==========================================================
    @property
    def pipeline_type(self) -> str:
        """Method implementation."""
        return "USBPD-Pipeline"

    @property
    def file_path(self) -> Path:
        """Method implementation."""
        return self.__file_path

    @property
    def mode(self) -> ParserMode:
        """Method implementation."""
        return self.__mode

    @property
    def output_dir(self) -> Path:
        """Method implementation."""
        return self.__output_dir

    @property
    def doc_title(self) -> str:
        """Method implementation."""
        return self.__doc_title

    @property
    def execution_count(self) -> int:
        """Method implementation."""
        return self.__exec_count

    @property
    def success_count(self) -> int:
        """Method implementation."""
        return self.__success

    @property
    def error_count(self) -> int:
        """Method implementation."""
        return self.__errors

    @property
    def file_name(self) -> str:
        """Method implementation."""
        return self.__file_path.name

    @property
    def file_stem(self) -> str:
        """Method implementation."""
        return self.__file_path.stem

    @property
    def file_suffix(self) -> str:
        """Method implementation."""
        return self.__file_path.suffix

    @property
    def file_exists(self) -> bool:
        """Method implementation."""
        return self.__file_path.exists()

    @property
    def file_size(self) -> int:
        """Method implementation."""
        return self.__file_path.stat().st_size if self.file_exists else 0

    @property
    def file_size_kb(self) -> float:
        """Method implementation."""
        return self.file_size / 1024

    @property
    def file_size_mb(self) -> float:
        """Method implementation."""
        return self.file_size / (1024 * 1024)

    @property
    def output_exists(self) -> bool:
        """Method implementation."""
        return self.__output_dir.exists()

    @property
    def output_name(self) -> str:
        """Method implementation."""
        return self.__output_dir.name

    @property
    def mode_value(self) -> str:
        """Method implementation."""
        return str(self.__mode.value)

    @property
    def mode_name(self) -> str:
        """Method implementation."""
        return str(self.__mode.name)

    @property
    def is_full_mode(self) -> bool:
        """Method implementation."""
        return self.__mode == ParserMode.FULL

    @property
    def is_toc_mode(self) -> bool:
        """Method implementation."""
        return self.__mode == ParserMode.TOC

    @property
    def is_content_mode(self) -> bool:
        """Method implementation."""
        return self.__mode == ParserMode.CONTENT

    @property
    def has_executions(self) -> bool:
        """Method implementation."""
        return self.__exec_count > 0

    @property
    def has_successes(self) -> bool:
        """Method implementation."""
        return self.__success > 0

    @property
    def has_errors(self) -> bool:
        """Method implementation."""
        return self.__errors > 0

    @property
    def success_rate(self) -> float:
        """Method implementation."""
        if self.__exec_count > 0:
            return self.__success / self.__exec_count
        return 0.0

    @property
    def error_rate(self) -> float:
        """Method implementation."""
        if self.__exec_count > 0:
            return self.__errors / self.__exec_count
        return 0.0

    # ==========================================================
    # VALIDATION
    # ==========================================================
    def validate(self) -> ValidationResult:
        """Method implementation."""
        errors: list[str] = []

        if not self.__file_path.exists():
            errors.append(f"File not found: {self.__file_path}")

        if self.__file_path.suffix.lower() != ".pdf":
            errors.append("Input must be a PDF file.")

        return ValidationResult(is_valid=(not errors), errors=errors)

    def _ensure_valid(self) -> None:
        """Method implementation."""
        val = self.validate()
        if not val.is_valid:
            raise ValueError(f"Validation failed: {', '.join(val.errors)}")

    # ==========================================================
    # TEMPLATE METHOD PATTERN → execute()
    # ==========================================================
    def execute(self) -> ParserResult:
        """Method implementation."""
        self.__exec_count += 1
        self._on_start()

        try:
            self.prepare()
            self._ensure_valid()

            result = self._parse()
            self._write_outputs(result)      # overloaded version inside
            self._generate_reports(result)

            self.__success += 1
            self._on_complete()
            return result

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.__errors += 1
            raise

        finally:
            self.cleanup()

    # ==========================================================
    # METHOD OVERLOADING — run()
    # ==========================================================

    @overload
    def run(self) -> ParserResult: ...

    @overload
    def run(self, mode: ParserMode) -> ParserResult: ...

    def run(self, mode: ParserMode | None = None) -> ParserResult:
        """
        Overloaded method:
        - run()                 → use existing mode
        - run(ParserMode.FULL)  → override mode and run
        """
        if mode:
            self._PipelineOrchestrator__mode = mode
        return self.execute()

    # ==========================================================
    # INTERNAL LIFECYCLE HOOKS
    # ==========================================================
    def _on_start(self) -> None:
        """Method implementation."""
        logger.info("Pipeline started.")

    def _on_complete(self) -> None:
        """Method implementation."""
        logger.info("Pipeline completed successfully.")

    # ==========================================================
    # PREPARE
    # ==========================================================
    def prepare(self) -> None:
        """Method implementation."""
        if not self.__output_dir.exists():
            self.__output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created output directory: {self.__output_dir}")

    # ==========================================================
    # PARSE
    # ==========================================================
    def _parse(self) -> ParserResult:
        """Method implementation."""
        from src.parser.parser_factory import ParserFactory
        parser = ParserFactory.create_parser(self.__file_path)
        logger.info("Parsing PDF...")
        return parser.parse()

    # ==========================================================
    # METHOD OVERLOADING — write_outputs()
    # ==========================================================

    @overload
    def _write_outputs(self, result: ParserResult) -> None: ...

    @overload
    def _write_outputs(self, result: ParserResult, *, only: str) -> None: ...

    def _write_outputs(
        self, result: ParserResult, *, only: str = "all"
    ) -> None:
        """
        Overloaded output writer.
        - only="all" (default)
        - only="toc"
        - only="content"
        """
        writer = JSONLWriter(self.__doc_title)
        out = self.__output_dir

        if only == "all":
            writer.write_toc(
                result.toc_entries, out / self._toc_name
            )
            writer.write_content(
                result.content_items, out / self._content_name
            )
        elif only == "toc":
            writer.write_toc(
                result.toc_entries, out / self._toc_name
            )
        elif only == "content":
            writer.write_content(
                result.content_items, out / self._content_name
            )
        else:
            raise ValueError("Invalid `only` value for _write_outputs")

    # ==========================================================
    # REPORT GENERATION
    # ==========================================================
    def _generate_reports(self, result: ParserResult) -> None:
        """Method implementation."""
        out = self.__output_dir
        MetadataGenerator().generate(result, out / "usb_pd_metadata.jsonl")
        JSONReportGenerator().generate(result, out / "parsing_report.json")
        ExcelReportGenerator().generate(result, out / "validation_report.xlsx")

    # ==========================================================
    # CLEANUP
    # ==========================================================
    def cleanup(self) -> None:
        """Method implementation."""
        logger.info("Cleanup complete.")

    # ==========================================================
    # REQUIRED INTERFACE METHODS
    # ==========================================================
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def cancel(self) -> None: ...

    def get_status(self) -> str:
        """Method implementation."""
        return "running" if self.__exec_count else "idle"

    def get_progress(self) -> float:
        """Method implementation."""
        return 1.0 if self.__success else 0.0

    # ==========================================================
    # MAGIC METHODS
    # ==========================================================
    def __str__(self) -> str:
        """Method implementation."""
        return (
            f"PipelineOrchestrator(file={self.file_path.name}, "
            f"mode={self.mode.value})"
        )

    def __repr__(self) -> str:
        """Method implementation."""
        return (
            f"PipelineOrchestrator(path={self.file_path!r}, "
            f"mode={self.mode!r})"
        )

    def __len__(self) -> int:
        """Method implementation."""
        return self.__exec_count

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.file_path.exists()

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return (
            isinstance(other, PipelineOrchestrator)
            and self.__file_path == other.__file_path
        )

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((type(self).__name__, self.__file_path))

    def __call__(self) -> ParserResult:
        """Make orchestrator callable."""
        return self.execute()

    def __enter__(self) -> "PipelineOrchestrator":
        """Context manager support."""
        self.prepare()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object
    ) -> None:
        """Context manager cleanup."""
        self.cleanup()

    def __int__(self) -> int:
        """Method implementation."""
        return self.__exec_count

    def __float__(self) -> float:
        """Method implementation."""
        return float(self.__success)

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, PipelineOrchestrator):
            return NotImplemented
        return self.__exec_count < other.__exec_count

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, PipelineOrchestrator):
            return NotImplemented
        return self.__exec_count > other.__exec_count

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in str(self.__file_path)

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return str(self.__file_path)[index]
