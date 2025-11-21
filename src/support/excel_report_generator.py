"""Excel validation report generator."""

from pathlib import Path
from typing import Any, Callable, Union

from openpyxl import Workbook  # type: ignore[import-untyped]

from src.core.config.models import ParserResult
from src.core.interfaces.report_interface import IReportGenerator


class ExcelReportGenerator(IReportGenerator):
    """Generate Excel validation report."""

    __METRICS: list[tuple[str, Union[str, Callable[[ParserResult], int]]]] = [
        ("Metric", "Value"),
        ("TOC Entries", lambda r: len(r.toc_entries)),
        ("Content Items", lambda r: len(r.content_items)),
    ]

    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate Excel validation report."""
        wb: Any = Workbook()
        ws: Any = wb.active
        ws.title = "Validation"

        for row_num, (metric, value_func) in enumerate(self.__METRICS, start=1):
            ws.cell(row=row_num, column=1, value=metric)
            if callable(value_func):
                ws.cell(row=row_num, column=2, value=value_func(result))
            else:
                ws.cell(row=row_num, column=2, value=value_func)

        try:
            wb.save(path)
        except OSError as e:
            raise OSError(f"Failed to save Excel report to {path}: {e}") from e

    def __str__(self) -> str:
        """String representation."""
        return "ExcelReportGenerator(format=xlsx)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return "ExcelReportGenerator()"
