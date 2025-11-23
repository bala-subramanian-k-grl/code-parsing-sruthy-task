"""JSON report generator with improved OOP design + added methods."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from src.core.config.models import ParserResult
from src.support.base_report_generator import BaseReportGenerator


class JSONReportGenerator(BaseReportGenerator):
    """Generate JSON report file with enhanced OOP principles and additional methods."""

    @property
    def report_type(self) -> str:
        return "JSON"

    @property
    def output_extension(self) -> str:
        return ".json"


    def generate_timestamp(self) -> str:
        """Return current timestamp (encapsulation)."""
        return datetime.now().isoformat()

    def generate_metadata(self) -> Dict[str, Any]:
        """Common metadata block (reusable across all JSON reports)."""
        return {
            "timestamp": self.generate_timestamp(),
            "report_type": self.report_type,
            "status": "completed",
        }

    def prepare_output_path(self, base_path: Path) -> Path:
        """
        Prepare output path with correct extension.
        Subclasses can override for custom behavior.
        """
        return base_path.with_suffix(self.output_extension)

    def serialize(self, data: Dict[str, Any]) -> str:
        """
        Polymorphic JSON serialization method.
        Can be overridden for:
        - compressed JSON
        - encrypted JSON
        - minified JSON
        """
        return json.dumps(data, indent=2)

    def log_report_created(self, path: Path) -> None:
        """
        Optional hook method for logging/reporting (polymorphic).
        Subclasses may override.
        """
        # You can integrate app-wide logging here if needed
        pass

    def create_report(self, result: ParserResult, output_path: Path) -> Path:
        """
        High-level template method.
        Combines validation → formatting → serialization → writing.
        """
        self._validate_result(result)
        data = self._format_data(result)
        full_path = self.prepare_output_path(output_path)
        self._write_to_file(data, full_path)
        self.log_report_created(full_path)
        return full_path

    def _validate_result(self, result: ParserResult) -> None:
        if not result.content_items:
            raise ValueError("Result has no content items")

    def _extract_pages(self, result: ParserResult) -> list[int]:
        return [item.page for item in result.content_items]

    def _build_statistics(self, result: ParserResult) -> Dict[str, Any]:
        pages = self._extract_pages(result)
        return {
            "total_pages": max(pages) if pages else 0,
            "toc_entries": len(result.toc_entries),
            "content_items": len(result.content_items),
        }

    def _build_validation_summary(self, result: ParserResult) -> Dict[str, bool]:
        return {
            "toc_extracted": bool(result.toc_entries),
            "content_extracted": bool(result.content_items),
        }

    def _format_data(self, result: ParserResult) -> Dict[str, Any]:
        base_metadata = self.generate_metadata()
        base_metadata.update({
            "statistics": self._build_statistics(result),
            "validation": self._build_validation_summary(result),
        })
        return base_metadata

    def _write_to_file(self, data: Dict[str, Any], path: Path) -> None:
        try:
            serialized = self.serialize(data)
            with path.open("w", encoding="utf-8") as f:
                f.write(serialized)
        except OSError as e:
            raise OSError(f"Failed to save JSON report to {path}: {e}") from e

    def get_file_extension(self) -> str:
        return "json"
