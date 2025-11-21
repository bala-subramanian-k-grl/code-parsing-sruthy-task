"""Metadata file generator."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Union

from src.core.config.config_loader import ConfigLoader
from src.core.config.models import Metadata, ParserResult
from src.core.interfaces.report_interface import IReportGenerator

MAX_CONTENT_ITEMS_FOR_KEYWORDS = 100


class MetadataGenerator(IReportGenerator):
    """Generate metadata JSONL file."""

    def __init__(self, config: Union[ConfigLoader, None] = None) -> None:
        self.__config = config or ConfigLoader()

    @property
    def config(self) -> ConfigLoader:
        """Get configuration loader."""
        return self.__config

    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate metadata file."""
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

        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(f"{json.dumps(data)}\n")
        except OSError as e:
            raise OSError(f"Failed to save metadata to {path}: {e}") from e

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

    def __str__(self) -> str:
        """String representation."""
        return "MetadataGenerator(format=jsonl)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return "MetadataGenerator()"
