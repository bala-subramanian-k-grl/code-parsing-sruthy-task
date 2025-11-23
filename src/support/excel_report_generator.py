"""Excel validation report generator."""

from __future__ import annotations
from pathlib import Path
from typing import Any, Callable, Union

from openpyxl import Workbook  # type: ignore[import-untyped]
from openpyxl.worksheet.worksheet import Worksheet  # type: ignore[import-untyped]

from src.core.config.models import ParserResult
from src.support.base_report_generator import BaseReportGenerator


class ExcelReportGenerator(BaseReportGenerator):
    """Generate Excel validation report."""

    # ---------------------------------------------------------
    # Polymorphic Identification
    # ---------------------------------------------------------

    @property
    def report_type(self) -> str:
        """Return report type."""
        return "Excel"

    @property
    def output_extension(self) -> str:
        """Return output file extension."""
        return ".xlsx"

    def get_file_extension(self) -> str:
        """Return output extension (polymorphic)."""
        return "xlsx"

    # ---------------------------------------------------------
    # Report Metrics — Encapsulated, Reusable
    # ---------------------------------------------------------

    _METRICS: list[
        tuple[str, Union[str, Callable[[ParserResult], int]]]
    ] = [
        ("Metric", "Value"),
        ("TOC Entries", lambda r: len(r.toc_entries)),
        ("Content Items", lambda r: len(r.content_items)),
    ]

    # ---------------------------------------------------------
    # Template Method Hooks (abstract in BaseReportGenerator)
    # ---------------------------------------------------------

    def _validate_result(self, result: ParserResult) -> None:
        """Ensure the result has data."""
        if not result.toc_entries and not result.content_items:
            raise ValueError("ParserResult contains no TOC or content items.")

    def _format_data(self, result: ParserResult) -> Any:
        """Convert parser result into an Excel workbook."""
        workbook: Workbook = Workbook()
        sheet: Worksheet = workbook.active  # type: ignore
        sheet.title = "Validation"

        for idx, (metric, value_fn) in enumerate(self._METRICS, start=1):
            sheet.cell(row=idx, column=1, value=metric)

            value = value_fn(result) if callable(value_fn) else value_fn
            sheet.cell(row=idx, column=2, value=value)

        return workbook

    def _write_to_file(self, data: Any, path: Path) -> None:
        """Save workbook to Excel file."""
        try:
            data.save(path)
        except OSError as e:
            raise OSError(
                f"Failed to save Excel report to '{path}': {e}"
            ) from e

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return f"ExcelReportGenerator(format={self.get_file_extension()})"

    def __repr__(self) -> str:
        return "ExcelReportGenerator()"
