"""Validation report generator with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union

try:
    import openpyxl
    from openpyxl.styles import Font

    _has_openpyxl = True
except ImportError:
    openpyxl = None  # type: ignore
    Font = None  # type: ignore
    _has_openpyxl = False


class BaseValidator(ABC):  # Abstraction
    def __init__(self, output_dir: Path):
        self._output_dir = output_dir  # Encapsulation

    @abstractmethod  # Abstraction
    def generate_validation(self, toc_data: list[Any], spec_data: list[Any]) -> Path:
        pass


class XLSValidator(BaseValidator):  # Inheritance
    def generate_validation(
        self, toc_data: list[Any], spec_data: list[Any]
    ) -> Path:  # Polymorphism
        if not _has_openpyxl or openpyxl is None or Font is None:
            raise ImportError("openpyxl required for Excel reports")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Summary"  # type: ignore

        # Create summary
        ws["A1"] = "USB PD Validation Report"  # type: ignore
        ws["A1"].font = Font(bold=True, size=14)  # type: ignore

        metrics: list[tuple[str, Union[int, str]]] = [
            ("TOC Entries", len(toc_data)),
            ("Content Items", len(spec_data)),
            ("Status", "PASS" if len(spec_data) > 1000 else "FAIL"),
        ]

        for i, (metric, value) in enumerate(metrics, 3):
            ws[f"A{i}"] = metric  # type: ignore
            ws[f"B{i}"] = value  # type: ignore

        xlsx_file = self._output_dir / "validation_report.xlsx"
        wb.save(xlsx_file)
        return xlsx_file


def create_validation_report(output_dir: Path, toc_file: Path, spec_file: Path) -> Path:
    """Factory function to create validation report."""
    toc_data: list[Any] = []
    spec_data: list[Any] = []

    # Load TOC data
    try:
        with open(toc_file, encoding="utf-8") as f:
            toc_data = [json.loads(line) for line in f if line.strip()]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Load spec data
    try:
        with open(spec_file, encoding="utf-8") as f:
            spec_data = [json.loads(line) for line in f if line.strip()]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return XLSValidator(output_dir).generate_validation(toc_data, spec_data)
