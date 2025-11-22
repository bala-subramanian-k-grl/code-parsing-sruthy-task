"""JSON report generator."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.config.models import ParserResult
from src.support.base_report_generator import BaseReportGenerator


class JSONReportGenerator(BaseReportGenerator):
    """Generate JSON report file."""

    def _validate_result(self, result: ParserResult) -> None:
        """Validate result has content items."""
        if not result.content_items:
            raise ValueError("Result has no content items")

    def _format_data(self, result: ParserResult) -> dict[str, Any]:
        """Format data as JSON dict."""
        pages = [i.page for i in result.content_items]
        return {
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

    def _write_to_file(self, data: dict[str, Any], path: Path) -> None:
        """Write JSON data to file."""
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            raise OSError(
                f"Failed to save JSON report to {path}: {e}"
            ) from e

    def get_file_extension(self) -> str:
        """Get file extension."""
        return "json"


