"""JSON Report Generator Module"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config.constants import MIN_CONTENT_THRESHOLD
from src.support.report.report_generator import BaseReportGenerator


class JSONReportGenerator(BaseReportGenerator):  # Inheritance
    def get_report_type(self) -> str:
        """Get report type name."""
        return "json"

    def get_file_extension(self) -> str:
        """Get file extension for this report type."""
        return ".json"

    def generate(self, data: dict[str, Any]) -> Path:  # Polymorphism
        report_file = self.output_dir / "parsing_report.json"
        try:
            report: dict[str, Any] = {
                "metadata": {
                    "title": "USB PD Report",
                    "generated": datetime.now().isoformat(),
                },
                "summary": data,
                "validation": {
                    "status": (
                        "PASS"
                        if data.get("content_items", 0) > MIN_CONTENT_THRESHOLD
                        else "FAIL"
                    )
                },
            }
        except (TypeError, ValueError) as e:
            raise RuntimeError(f"Cannot create report data: {e}") from e
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        except OSError as e:
            raise RuntimeError(f"Cannot write JSON report: {e}") from e
        return report_file
