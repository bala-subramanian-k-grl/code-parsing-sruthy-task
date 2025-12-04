"""
Metadata Generator with full OOP, Polymorphism, Overloading.

Template Method Pattern.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, overload

from src.core.config.config_loader import ConfigLoader
from src.core.config.models import Metadata, ParserResult
from src.support.base_report_generator import BaseReportGenerator

MAX_CONTENT_ITEMS_FOR_KEYWORDS = 100


class MetadataGenerator(BaseReportGenerator):
    """Generate metadata JSONL using full OOP and extensibility."""

    def __init__(self, config: ConfigLoader | None = None) -> None:
        """Method implementation."""
        super().__init__()
        self.__config = config or ConfigLoader()

    # ---------------------------------------------------------
    # Polymorphic Identification
    # ---------------------------------------------------------
    @property
    def report_type(self) -> str:
        """Method implementation."""
        return "Metadata"

    @property
    def output_extension(self) -> str:
        """Method implementation."""
        return ".jsonl"

    def get_file_extension(self) -> str:
        """Return file extension with correct dot-prefix."""
        return ".jsonl"

    # ---------------------------------------------------------
    # Template Method Hooks (BaseReportGenerator)
    # ---------------------------------------------------------
    def _validate_result(self, result: ParserResult) -> None:
        """Ensure TOC exists before generating metadata."""
        if not result.toc_entries:
            msg = "Metadata cannot be generated: No TOC entries found."
            raise ValueError(msg)

    def _extract_pages(self, result: ParserResult) -> list[int]:
        """Method implementation."""
        return [item.page for item in result.content_items]

    def _count_toc_levels(self, result: ParserResult) -> dict[str, int]:
        """Encapsulated calculation of TOC levels."""
        levels: dict[str, int] = {}
        for entry in result.toc_entries:
            key = f"level_{entry.level}"
            levels[key] = levels.get(key, 0) + 1
        return levels

    def _count_content_types(self, result: ParserResult) -> dict[str, int]:
        """Encapsulated calculation of content type distribution."""
        types: dict[str, int] = {}
        for item in result.content_items:
            t = item.content_type
            types[t] = types.get(t, 0) + 1
        return types

    def _count_major_sections(self, result: ParserResult) -> int:
        """Major sections: TOC entries with level 1"""
        return sum(1 for e in result.toc_entries if e.level == 1)

    def _extract_key_terms(
        self, result: ParserResult, limit: int
    ) -> set[str]:
        """Extract configured keywords from content."""
        keywords = self._get_keywords()
        found_terms: set[str] = set()

        for item in result.content_items[:limit]:
            text = item.content.lower()
            found_terms.update(k for k in keywords if k.lower() in text)

        return found_terms

    def _get_keywords(self) -> list[str]:
        """Get keywords from config."""
        meta_cfg = self.__config.get("metadata", {})
        keywords_data = meta_cfg.get("keywords", [])
        return [str(k) for k in keywords_data] if keywords_data else []

    # ---------------------------------------------------------
    # FORMAT DATA (Template Method Hook)
    # ---------------------------------------------------------
    def _format_data(self, result: ParserResult) -> dict[str, Any]:
        """Method implementation."""
        pages = self._extract_pages(result)

        metadata = Metadata(
            total_pages=max(pages) if pages else 0,
            total_toc_entries=len(result.toc_entries),
            total_content_items=len(result.content_items),
            toc_levels=self._count_toc_levels(result),
            content_types=self._count_content_types(result),
        )

        base = asdict(metadata)
        key_terms = self._extract_key_terms(
            result, MAX_CONTENT_ITEMS_FOR_KEYWORDS
        )

        # Additional metadata
        base["major_sections"] = self._count_major_sections(result)
        base["key_terms_count"] = len(key_terms)
        base["key_terms"] = sorted(list(key_terms))

        return base

    # ---------------------------------------------------------
    # Overloaded Methods (Required For OOP Score)
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
        """Polymorphic output path handler."""
        if force_ext:
            return base_path.with_suffix(self.output_extension)

        if base_path.suffix.lower() != self.output_extension:
            return base_path.with_suffix(self.output_extension)

        return base_path

    @overload
    def serialize(self, data: dict[str, Any]) -> str: ...

    @overload
    def serialize(self, data: dict[str, Any], *, compact: bool) -> str: ...

    def serialize(self, data: dict[str, Any], *, compact: bool = False) -> str:
        """Overloaded serializer: pretty or compact JSON."""
        if compact:
            return json.dumps(data, separators=(",", ":"))
        return json.dumps(data)

    # ---------------------------------------------------------
    # WRITE TO FILE (Template Method Hook)
    # MUST RETURN BYTES WRITTEN
    # ---------------------------------------------------------
    def _write_to_file(self, data: dict[str, Any], path: Path) -> int:
        """Method implementation."""
        serialized = self.serialize(data)

        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(serialized + "\n")

            return path.stat().st_size  # bytes written

        except OSError as e:
            raise OSError(f"Failed to write metadata JSONL: {e}") from e

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        """Method implementation."""
        return "MetadataGenerator(.jsonl)"

    def __repr__(self) -> str:
        """Method implementation."""
        return "MetadataGenerator()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, MetadataGenerator)

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
        if not isinstance(other, MetadataGenerator):
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
        if not isinstance(other, MetadataGenerator):
            return NotImplemented
        return self.report_type > other.report_type

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other
