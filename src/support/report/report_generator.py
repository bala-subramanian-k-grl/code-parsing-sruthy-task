"""Minimal report generator with OOP principles."""


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseReportGenerator(ABC):  # Abstraction
    def __init__(self, output_dir: Path):
        self._output_dir = output_dir  # Encapsulation
        self._output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod  # Abstraction
    def generate(self, data: dict[str, Any]) -> Path:
        pass


class ReportFactory:  # Factory pattern
    _ALLOWED_TYPES = {"json", "excel"}  # Authorized report types

    @staticmethod
    def create_generator(
        report_type: str, output_dir: Path
    ) -> BaseReportGenerator:
        # Validate and sanitize input
        if not report_type.strip():
            raise ValueError("Report type must be a non-empty string")

        clean_type = report_type.strip().lower()
        if clean_type not in ReportFactory._ALLOWED_TYPES:
            raise ValueError(f"Unauthorized report type: {report_type}")

        if clean_type == "json":
            from .jsonreport_generator import JSONReportGenerator

            return JSONReportGenerator(output_dir)  # Polymorphism
        elif clean_type == "excel":
            from .excel_report import ExcelReportGenerator

            return ExcelReportGenerator(output_dir)
        raise ValueError(f"Invalid report type: {report_type}")
