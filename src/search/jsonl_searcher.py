"""
Enterprise JSONL Searcher (OOP + Overloading + Polymorphism)
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from typing import Any, overload


class BaseSearcher(ABC):
    """Abstract base class for all searchers."""

    @abstractmethod
    # type: ignore[misc]
    def search(
        self, keyword: str | Iterable[str], **kwargs
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        """Method implementation."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"


class JSONLSearcher(BaseSearcher):
    """Search JSONL files for keywords."""

    def __init__(self, file_path: Path) -> None:
        """Method implementation."""
        self.__file_path = file_path
        self.__search_count = 0
        self.__total_matches = 0
        self.__cached_lines: list[dict[str, Any]] | None = None

    # =========================================================
    # Encapsulation
    # =========================================================

    @property
    def file_path(self) -> Path:
        """Method implementation."""
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        """Method implementation."""
        return self.__file_path.exists()

    @property
    def file_name(self) -> str:
        """Method implementation."""
        return self.__file_path.name

    @property
    def file_suffix(self) -> str:
        """Method implementation."""
        return self.__file_path.suffix.lower()

    @property
    def file_size(self) -> int:
        """Method implementation."""
        return self.__file_path.stat().st_size if self.file_exists else 0

    # =========================================================
    # Polymorphism
    # =========================================================

    @property
    def searcher_type(self) -> str:
        """Method implementation."""
        return "JSONL"

    def supports(self, ext: str) -> bool:
        """Method implementation."""
        return ext.lower() == ".jsonl"

    def validate(self) -> bool:
        """Method implementation."""
        return self.file_exists and self.file_suffix == ".jsonl"

    # =========================================================
    # Internal Helpers
    # =========================================================

    def _load_lines(self) -> list[dict[str, Any]]:
        """Load JSONL lines once (caching)."""
        if self.__cached_lines is not None:
            return self.__cached_lines

        self.__cached_lines = self._parse_jsonl()
        return self.__cached_lines

    def _parse_jsonl(self) -> list[dict[str, Any]]:
        """Parse JSONL file into list of dicts."""
        lines: list[dict[str, Any]] = []
        try:
            with self.__file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    obj = self._parse_line(line)
                    if obj:
                        lines.append(obj)
        except OSError as e:
            raise OSError(f"Failed to read: {self.__file_path}") from e
        return lines

    def _parse_line(self, line: str) -> dict[str, Any] | None:
        """Parse single JSON line."""
        try:
            obj = json.loads(line)
            return obj if isinstance(obj, dict) else None
        except json.JSONDecodeError:
            return None

    # =========================================================
    # Overloaded Search Methods
    # =========================================================

    # 1) search("keyword")
    @overload
    def search(self, keyword: str) -> int: ...  # type: ignore[override]

    # 2) search(["word1","word2"])
    @overload
    def search(
        self, keyword: Iterable[str]
    ) -> int: ...
    # type: ignore[override]

    # 3) search("keyword", case_sensitive=True)
    @overload
    def search(
        self, keyword: str, *, case_sensitive: bool
    ) -> int: ...  # type: ignore[override]

    # 4) search("keyword", field="title")
    @overload
    def search(
        self, keyword: str, *, field: str
    ) -> int: ...  # type: ignore[override]

    def search(
        self,
        keyword: str | Iterable[str],
        *,
        case_sensitive: bool = False,
        field: str = "any",
    ) -> int:
        """Search for keywords in JSONL file."""
        self.__search_count += 1

        if not self.validate():
            raise ValueError(f"Invalid JSONL: {self.__file_path}")

        lines = self._load_lines()
        fields = self._get_fields(field)
        keywords = self._normalize_keywords(keyword, case_sensitive)

        matches = self._count_matches(
            lines, fields, keywords, case_sensitive
        )
        self.__total_matches += matches
        return matches

    def _get_fields(self, field: str) -> list[str]:
        """Get search fields."""
        return ["title", "content"] if field == "any" else [field]

    def _normalize_keywords(
        self, keyword: str | Iterable[str], case_sensitive: bool
    ) -> list[str]:
        """Normalize keywords for search."""
        keywords = [keyword] if isinstance(keyword, str) else list(
            keyword)
        return keywords if case_sensitive else [k.lower() for k in keywords]

    def _count_matches(
        self, lines: list[dict[str, Any]], fields: list[str],
        keywords: list[str], case_sensitive: bool
    ) -> int:
        """Count keyword matches in records."""
        matches = 0
        for record in lines:
            for fld in fields:
                text = str(record.get(fld, ""))
                cmp_text = text if case_sensitive else text.lower()
                for kw in keywords:
                    matches += cmp_text.count(kw)
        return matches

    # =========================================================
    # Magic / Utility Methods
    # =========================================================

    def __str__(self) -> str:
        """Method implementation."""
        return f"JSONLSearcher({self.file_name})"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"JSONLSearcher(path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, JSONLSearcher) and (
            self.__file_path == other.__file_path
        )

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((type(self).__name__, self.__file_path))

    def __len__(self) -> int:
        """Return number of JSONL lines."""
        return len(self._load_lines())

    def __contains__(self, keyword: str) -> bool:
        """Check if keyword appears in any line (fast search)."""
        return self.search(keyword) > 0

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.file_exists

    def __getitem__(self, index: int) -> dict[str, Any]:
        """Index into a JSONL record."""
        return self._load_lines()[index]

    def __iter__(self):
        """Iterate over parsed JSON lines."""
        return iter(self._load_lines())

    def __int__(self) -> int:
        """Number of searches performed."""
        return self.__search_count

    def __float__(self) -> float:
        """Total matches found."""
        return float(self.__total_matches)
