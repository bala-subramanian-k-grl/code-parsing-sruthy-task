import json
from src.support.report.report_generator import BaseReportGenerator
from datetime import datetime
from pathlib import Path
from typing import Any


class JSONReportGenerator(BaseReportGenerator):  # Inheritance
    def generate(self, data: dict[str, Any]) -> Path:  # Polymorphism
        report_file = self._output_dir / "parsing_report.json"
        try:
            report: dict[str, Any] = {
                "metadata": {
                    "title": "USB PD Report",
                    "generated": datetime.now().isoformat(),
                },
                "summary": data,
                "validation": {
                    "status": "PASS" if data.get("content_items", 0) > 1000 else "FAIL"
                },
            }
        except (TypeError, ValueError) as e:
            raise RuntimeError(f"Cannot create report data: {e}") from e
        try:
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)
        except OSError as e:
            raise RuntimeError(f"Cannot write JSON report: {e}") from e
        return report_file