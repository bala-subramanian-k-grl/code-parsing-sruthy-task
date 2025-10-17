"""Validation report generator with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union

from src.config.constants import MIN_CONTENT_THRESHOLD

try:
    import openpyxl
    from openpyxl.styles import Font
except ImportError:
    openpyxl = None  # type: ignore
    Font = None  # type: ignore

HAS_OPENPYXL = openpyxl is not None


class BaseValidator(ABC):  # Abstraction
    """Abstract base class for validation report generators."""

    def __init__(self, output_dir: Path):
        """Initialize validator with output directory."""
        self._output_dir = output_dir  # Encapsulation

    @abstractmethod  # Abstraction
    def generate_validation(
        self, toc_data: list[Any], spec_data: list[Any]
    ) -> Path:
        """Generate validation report from TOC and spec data."""
        pass


class XLSValidator(BaseValidator):  # Inheritance
    """Excel-based validation report generator."""

    def generate_validation(
        self, toc_data: list[Any], spec_data: list[Any]
    ) -> Path:
        """Generate Excel validation report."""
        if not HAS_OPENPYXL or openpyxl is None:
            raise ImportError("openpyxl required for Excel reports")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Summary"  # type: ignore

        # Create summary
        ws["A1"] = "USB PD Validation Report"  # type: ignore
        ws["A1"].font = Font(bold=True, size=14)  # type: ignore

        status = "PASS" if len(spec_data) > MIN_CONTENT_THRESHOLD else "FAIL"
        metrics: list[tuple[str, Union[int, str]]] = [
            ("TOC Entries", len(toc_data)),
            ("Content Items", len(spec_data)),
            ("Status", status),
        ]

        for i, (metric, value) in enumerate(metrics, 3):
            ws[f"A{i}"] = metric  # type: ignore
            ws[f"B{i}"] = value  # type: ignore

        xlsx_file = self._output_dir / "validation_report.xlsx"
        wb.save(xlsx_file)
        return xlsx_file


def create_validation_report(
    output_dir: Path, toc_file: Path, spec_file: Path
) -> Path:
    """Factory function to create validation report."""
    toc_data: list[Any] = []
    spec_data: list[Any] = []

    # Load TOC data
    try:
        with open(toc_file, encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
            toc_data = [json.loads(line) for line in lines]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.debug("Failed to load TOC data: %s", e)
        toc_data = []

    # Load spec data
    try:
        with open(spec_file, encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
            spec_data = [json.loads(line) for line in lines]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.debug("Failed to load spec data: %s", e)
        spec_data = []

    validator = XLSValidator(output_dir)
    return validator.generate_validation(toc_data, spec_data)
