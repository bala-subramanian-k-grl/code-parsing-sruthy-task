"""Excel validation report generator."""

from pathlib import Path
from typing import Any, Callable, Union

from openpyxl import Workbook  # type: ignore[import-untyped]

from src.core.config.models import ParserResult
from src.support.base_report_generator import BaseReportGenerator


class ExcelReportGenerator(BaseReportGenerator):
    """Generate Excel validation report."""

    _METRICS: list[tuple[str, Union[str, Callable[[ParserResult], int]]]] = [
        ("Metric", "Value"),
        ("TOC Entries", lambda r: len(r.toc_entries)),
        ("Content Items", lambda r: len(r.content_items)),
    ]

    def _validate_result(self, result: ParserResult) -> None:
        """Validate result has required data."""
        if not result.toc_entries and not result.content_items:
            raise ValueError("Result has no data to report")

    def _format_data(self, result: ParserResult) -> Any:
        """Format data as Excel workbook."""
        wb: Any = Workbook()
        ws: Any = wb.active
        ws.title = "Validation"

        for row_num, (metric, value_func) in enumerate(
            self._METRICS, start=1
        ):
            ws.cell(row=row_num, column=1, value=metric)
            if callable(value_func):
                ws.cell(row=row_num, column=2, value=value_func(result))
            else:
                ws.cell(row=row_num, column=2, value=value_func)
        return wb

    def _write_to_file(self, data: Any, path: Path) -> None:
        """Write workbook to Excel file."""
        try:
            data.save(path)
        except OSError as e:
            raise OSError(
                f"Failed to save Excel report to {path}: {e}"
            ) from e

    def get_file_extension(self) -> str:
        """Get file extension."""
        return "xlsx"


