"""
JSON report generator with full OOP, overloading, polymorphism.
"""

from __future__ import annotations

from abc import ABC
import json
from datetime import datetime
from pathlib import Path
from typing import Any, overload

from src.core.config.models import ParserResult
from src.support.base_report_generator import BaseReportGenerator


class JSONReportGenerator(BaseReportGenerator, ABC):
    """Generate structured JSON summary report."""

    # ---------------------------------------------------------
    # Polymorphic Identification
    # ---------------------------------------------------------
    @property
    def report_type(self) -> str:
        """Method implementation."""
        return "JSON"

    @property
    def output_extension(self) -> str:
        """Method implementation."""
        return ".json"

    def get_file_extension(self) -> str:
        """Return correct extension."""
        return ".json"

    # ---------------------------------------------------------
    # Timestamp + Metadata (Encapsulation)
    # ---------------------------------------------------------
    @staticmethod
    def _timestamp() -> str:
        """Method implementation."""
        return datetime.now().isoformat()

    def _base_metadata(self) -> dict[str, Any]:
        """Common metadata for all JSON reports."""
        return {
            "timestamp": self._timestamp(),
            "report_type": self.report_type,
            "status": "success",
        }

    # ---------------------------------------------------------
    # Validation (Template Method Hook)
    # ---------------------------------------------------------
    def _validate_result(self, result: ParserResult) -> None:
        """Method implementation."""
        if not result.content_items:
            raise ValueError("ParserResult has no content items")

    # ---------------------------------------------------------
    # Formatting logic (Template Method Hook)
    # ---------------------------------------------------------
    def _extract_pages(self, result: ParserResult) -> list[int]:
        """Method implementation."""
        return [item.page for item in result.content_items]

    def _statistics(self, result: ParserResult) -> dict[str, Any]:
        """Method implementation."""
        pages = self._extract_pages(result)
        return {
            "total_pages": max(pages) if pages else 0,
            "toc_entries": len(result.toc_entries),
            "content_items": len(result.content_items),
        }

    def _summary(self, result: ParserResult) -> dict[str, bool]:
        """Method implementation."""
        return {
            "toc_extracted": bool(result.toc_entries),
            "content_extracted": bool(result.content_items),
        }

    def _format_data(self, result: ParserResult) -> dict[str, Any]:
        """Method implementation."""
        data = self._base_metadata()
        data.update(
            {
                "statistics": self._statistics(result),
                "validation": self._summary(result),
            }
        )
        return data

    # ---------------------------------------------------------
    # JSON Serialization (with Overloading)
    # ---------------------------------------------------------
    @overload
    def serialize(self, data: dict[str, Any]) -> str: ...

    @overload
    def serialize(self, data: dict[str, Any], *, compact: bool) -> str: ...

    def serialize(self, data: dict[str, Any], *, compact: bool = False) -> str:
        """
        Overloaded serializer:
        - serialize(data)
        - serialize(data, compact=True) → minified JSON
        """
        if compact:
            return json.dumps(data, separators=(",", ":"))
        return json.dumps(data, indent=2)

    # ---------------------------------------------------------
    # Write File (Template Method Hook)
    # Must return bytes written
    # ---------------------------------------------------------
    def _write_to_file(self, data: dict[str, Any], path: Path) -> int:
        """Method implementation."""
        try:
            serialized = self.serialize(data)
            with path.open("w", encoding="utf-8") as f:
                f.write(serialized)

            return path.stat().st_size  # bytes written

        except OSError as e:
            raise OSError(f"Failed to write JSON report: {e}") from e

    # ---------------------------------------------------------
    # Helper Overload: prepare_output_path
    # ---------------------------------------------------------
    @overload
    def prepare_output_path(self, base_path: Path) -> Path: ...

    @overload
    def prepare_output_path(
        self, base_path: Path, *, force_ext: bool
    ) -> Path: ...

    def prepare_output_path(
        self, base_path: Path, *, force_ext: bool = False
    ) -> Path:
        """
        If force_ext=True → always replace extension.
        """
        if force_ext:
            return base_path.with_suffix(self.output_extension)

        # Only add extension if missing
        if base_path.suffix.lower() != self.output_extension:
            return base_path.with_suffix(self.output_extension)

        return base_path

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        """Method implementation."""
        return "JSONReportGenerator(.json)"

    def __repr__(self) -> str:
        """Method implementation."""
        return "JSONReportGenerator()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, JSONReportGenerator)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __len__(self) -> int:
        """Method implementation."""
        return 1

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, JSONReportGenerator):
            return NotImplemented
        return self.report_type < other.report_type

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in self.report_type

    def __int__(self) -> int:
        """Method implementation."""
        return 1

    def __float__(self) -> float:
        """Method implementation."""
        return 1.0

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, JSONReportGenerator):
            return NotImplemented
        return self.report_type > other.report_type

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other
