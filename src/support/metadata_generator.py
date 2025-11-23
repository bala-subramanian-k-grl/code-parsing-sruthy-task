"""Metadata file generator with improved OOP design."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Optional, Dict

from src.core.config.config_loader import ConfigLoader
from src.core.config.models import Metadata, ParserResult
from src.support.base_report_generator import BaseReportGenerator

MAX_CONTENT_ITEMS_FOR_KEYWORDS = 100


class MetadataGenerator(BaseReportGenerator):
    """Generate metadata JSONL file with enhanced OOP principles."""

    def __init__(self, config: Optional[ConfigLoader] = None) -> None:
        super().__init__()
        self.__config = config or ConfigLoader()

    @property
    def report_type(self) -> str:
        return "Metadata"

    @property
    def output_extension(self) -> str:
        return ".jsonl"

    def create_report(self, result: ParserResult, path: Path) -> Path:
        """
        High-level template method using Template Method Pattern.
        Validates → formats → writes → logs.
        """
        self._validate_result(result)
        formatted = self._format_data(result)
        final_path = self.prepare_output_path(path)
        self._write_to_file(formatted, final_path)
        self._log_report_created(final_path)
        return final_path

    def prepare_output_path(self, base_path: Path) -> Path:
        """Polymorphic extension point: allows future custom naming rules."""
        return base_path.with_suffix(self.output_extension)

    def _log_report_created(self, path: Path) -> None:
        """Optional extension hook for logging or analytics."""
        # No-op by default; subclasses or mixins can override
        pass

    def _validate_result(self, result: ParserResult) -> None:
        if not result.toc_entries:
            raise ValueError("Result has no TOC entries")


    def _count_toc_levels(self, result: ParserResult) -> Dict[str, int]:
        """Encapsulated calculation of TOC level distribution."""
        levels: Dict[str, int] = {}
        for entry in result.toc_entries:
            key = f"level_{entry.level}"
            levels[key] = levels.get(key, 0) + 1
        return levels

    def _count_content_types(self, result: ParserResult) -> Dict[str, int]:
        """Encapsulated calculation of content type distribution."""
        types: Dict[str, int] = {}
        for item in result.content_items:
            types[item.content_type] = types.get(item.content_type, 0) + 1
        return types

    def _count_major_sections(self, result: ParserResult) -> int:
        """Encapsulation: major sections = TOC entries with level 1."""
        return sum(1 for e in result.toc_entries if e.level == 1)

    def _extract_key_terms(self, result: ParserResult, limit: int) -> set[str]:
        """Extract key terms from content using keywords from config."""
        keywords = self.__config.get_keywords()
        found_terms: set[str] = set()

        for item in result.content_items[:limit]:
            content_lower = item.content.lower()
            for keyword in keywords:
                if keyword in content_lower:
                    found_terms.add(keyword)

        return found_terms

    def _extract_pages(self, result: ParserResult) -> list[int]:
        """Encapsulated page extraction."""
        return [i.page for i in result.content_items]

    def _format_data(self, result: ParserResult) -> Dict[str, Any]:
        """Format final metadata structure."""
        pages = self._extract_pages(result)

        metadata = Metadata(
            total_pages=max(pages) if pages else 0,
            total_toc_entries=len(result.toc_entries),
            total_content_items=len(result.content_items),
            toc_levels=self._count_toc_levels(result),
            content_types=self._count_content_types(result),
        )

        # Convert dataclass to dict
        data = asdict(metadata)

        # Add additional calculated metadata
        key_terms = self._extract_key_terms(result, MAX_CONTENT_ITEMS_FOR_KEYWORDS)

        data["major_sections"] = self._count_major_sections(result)
        data["key_terms_count"] = len(key_terms)

        return data

    def _write_to_file(self, data: Dict[str, Any], path: Path) -> None:
        """Write metadata to JSONL file."""
        try:
            with path.open("w", encoding="utf-8") as file:
                file.write(json.dumps(data) + "\n")

        except OSError as e:
            raise OSError(f"Failed to save metadata to {path}: {e}") from e


    def get_file_extension(self) -> str:
        return "jsonl"
