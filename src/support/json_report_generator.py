"""JSON report generator."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.config.models import ParserResult
from src.core.interfaces.report_interface import IReportGenerator


class JSONReportGenerator(IReportGenerator):
    """Generate JSON report file."""

    def __init__(self) -> None:
        self.__generation_count = 0

    @property
    def generation_count(self) -> int:
        """Get generation count."""
        return self.__generation_count

    @property
    def has_generated(self) -> bool:
        """Check if has generated reports."""
        return self.__generation_count > 0

    @property
    def generation_rate(self) -> float:
        """Get generation rate."""
        return float(self.__generation_count)

    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate JSON report."""
        self.__generation_count += 1
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

    def __eq__(self, other: object) -> bool:
        return isinstance(other, JSONReportGenerator)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __len__(self) -> int:
        return 1

    def __bool__(self) -> bool:
        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, JSONReportGenerator):
            return NotImplemented
        return self.__generation_count < other.__generation_count

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __int__(self) -> int:
        return self.__generation_count

    def __float__(self) -> float:
        return float(self.__generation_count)
