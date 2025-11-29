"""
Enterprise JSONL Searcher (OOP + Overloading + Polymorphism)
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Iterable, List, Dict, overload


class JSONLSearcher:
    """Search JSONL files for keywords."""

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path
        self.__search_count = 0
        self.__total_matches = 0
        self.__cached_lines: List[Dict[str, Any]] | None = None

    # =========================================================
    # Encapsulation
    # =========================================================

    @property
    def file_path(self) -> Path:
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        return self.__file_path.exists()

    @property
    def file_name(self) -> str:
        return self.__file_path.name

    @property
    def file_suffix(self) -> str:
        return self.__file_path.suffix.lower()

    @property
    def file_size(self) -> int:
        return self.__file_path.stat().st_size if self.file_exists else 0

    # =========================================================
    # Polymorphism
    # =========================================================

    @property
    def searcher_type(self) -> str:
        return "JSONL"

    def supports(self, ext: str) -> bool:
        return ext.lower() == ".jsonl"

    def validate(self) -> bool:
        return self.file_exists and self.file_suffix == ".jsonl"

    # =========================================================
    # Internal Helpers
    # =========================================================

    def _load_lines(self) -> List[Dict[str, Any]]:
        """Load JSONL lines once (caching)."""
        if self.__cached_lines is not None:
            return self.__cached_lines

        lines: List[Dict[str, Any]] = []
        try:
            with self.__file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        if isinstance(obj, dict):
                            lines.append(obj)
                    except json.JSONDecodeError:
                        continue
        except OSError as e:
            raise OSError(f"Failed to read file '{self.__file_path}': {e}")

        self.__cached_lines = lines
        return lines

    # =========================================================
    # Overloaded Search Methods
    # =========================================================

    # 1) search("keyword")
    @overload
    def search(self, keyword: str) -> int: ...

    # 2) search(["word1","word2"])
    @overload
    def search(self, keyword: Iterable[str]) -> int: ...

    # 3) search("keyword", case_sensitive=True)
    @overload
    def search(self, keyword: str, *, case_sensitive: bool) -> int: ...

    # 4) search("keyword", field="title")
    @overload
    def search(self, keyword: str, *, field: str) -> int: ...

    def search(
        self,
        keyword: str | Iterable[str],
        *,
        case_sensitive: bool = False,
        field: str = "any",
    ) -> int:
        """
        Overloaded Search:
        ------------------
        search("usb")                                 → search all fields
        search(["usb","pd"])                          → multiple keywords
        search("USB", case_sensitive=True)            → case-sensitive
        search("usb power", field="title")            → title only
        """

        self.__search_count += 1

        if not self.validate():
            raise ValueError(f"Invalid JSONL file: {self.__file_path}")

        lines = self._load_lines()
        fields = ["title", "content"] if field == "any" else [field]

        # Normalize keywords
        keywords = (
            [keyword] if isinstance(keyword, str) else list(keyword)
        )

        if not case_sensitive:
            keywords = [k.lower() for k in keywords]

        matches = 0

        for record in lines:
            for fld in fields:
                text = str(record.get(fld, ""))

                cmp_text = text if case_sensitive else text.lower()

                for kw in keywords:
                    matches += cmp_text.count(kw)

        self.__total_matches += matches
        return matches

    # =========================================================
    # Magic / Utility Methods
    # =========================================================

    def __str__(self) -> str:
        return f"JSONLSearcher({self.file_name})"

    def __repr__(self) -> str:
        return f"JSONLSearcher(path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, JSONLSearcher) and (
            self.__file_path == other.__file_path
        )

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path))

    def __len__(self) -> int:
        """Return number of JSONL lines."""
        return len(self._load_lines())

    def __contains__(self, keyword: str) -> bool:
        """Check if keyword appears in any line (fast search)."""
        return self.search(keyword) > 0

    def __bool__(self) -> bool:
        return self.file_exists

    def __getitem__(self, index: int) -> Dict[str, Any]:
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
