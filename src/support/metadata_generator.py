"""Metadata file generator."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Optional

from src.core.config.config_loader import ConfigLoader
from src.core.config.models import Metadata, ParserResult
from src.support.base_report_generator import BaseReportGenerator

MAX_CONTENT_ITEMS_FOR_KEYWORDS = 100


class MetadataGenerator(BaseReportGenerator):
    """Generate metadata JSONL file."""

    def __init__(self, config: Optional[ConfigLoader] = None) -> None:
        super().__init__()
        self.__config = config or ConfigLoader()

    def _validate_result(self, result: ParserResult) -> None:
        """Validate result has TOC entries."""
        if not result.toc_entries:
            raise ValueError("Result has no TOC entries")

    def _format_data(self, result: ParserResult) -> dict[str, Any]:
        """Format data as metadata dict."""
        pages = [i.page for i in result.content_items]
        levels: dict[str, int] = {}
        for e in result.toc_entries:
            k = f"level_{e.level}"
            levels[k] = levels.get(k, 0) + 1
        types: dict[str, int] = {}
        for i in result.content_items:
            types[i.content_type] = types.get(i.content_type, 0) + 1

        major_sections = sum(
            1 for e in result.toc_entries if e.level == 1
        )
        key_terms = self._extract_key_terms(
            result, MAX_CONTENT_ITEMS_FOR_KEYWORDS
        )

        metadata = Metadata(
            total_pages=max(pages) if pages else 0,
            total_toc_entries=len(result.toc_entries),
            total_content_items=len(result.content_items),
            toc_levels=levels,
            content_types=types,
        )

        data = asdict(metadata)
        data["major_sections"] = major_sections
        data["key_terms_count"] = len(key_terms)
        return data

    def _write_to_file(self, data: dict[str, Any], path: Path) -> None:
        """Write metadata to JSONL file."""
        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(f"{json.dumps(data)}\n")
        except OSError as e:
            raise OSError(
                f"Failed to save metadata to {path}: {e}"
            ) from e

    def get_file_extension(self) -> str:
        """Get file extension."""
        return "jsonl"

    def _extract_key_terms(self, result: ParserResult, limit: int) -> set[str]:
        """Extract key terms from content up to specified limit."""
        terms: set[str] = set()
        keywords = self.__config.get_keywords()
        for item in result.content_items[:limit]:
            content_lower = item.content.lower()
            for keyword in keywords:
                if keyword in content_lower:
                    terms.add(keyword)
        return terms


