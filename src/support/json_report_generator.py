"""JSON report generator."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.config.models import ParserResult
from src.core.interfaces.report_interface import IReportGenerator


class JSONReportGenerator(IReportGenerator):
    """Generate JSON report file."""

    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate JSON report."""
        pages = [i.page for i in result.content_items]
        report: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "statistics": {
                "total_pages": max(pages) if pages else 0,
                "toc_entries": len(result.toc_entries),
                "content_items": len(result.content_items),
            },
            "validation": {
                "toc_extracted": bool(result.toc_entries),
                "content_extracted": bool(result.content_items),
            },
        }

        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        except OSError as e:
            raise OSError(f"Failed to save JSON report to {path}: {e}") from e

    def __str__(self) -> str:
        """String representation."""
        return "JSONReportGenerator(format=json)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return "JSONReportGenerator()"
