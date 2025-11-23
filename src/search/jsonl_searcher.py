"""JSONL file searcher with enterprise OOP structure."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any


class JSONLSearcher:
    """Search JSONL files for keywords."""

    def __init__(self, file_path: Path) -> None:
        """Initialize searcher with file path."""
        self.__file_path = file_path

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------

    @property
    def file_path(self) -> Path:
        """Get file path."""
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self.__file_path.exists()

    @property
    def file_name(self) -> str:
        return self.__file_path.name

    @property
    def file_suffix(self) -> str:
        return self.__file_path.suffix.lower()

    @property
    def file_parent(self) -> Path:
        return self.__file_path.parent

    @property
    def file_size(self) -> int:
        if not self.file_exists:
            return 0
        return self.__file_path.stat().st_size

    @property
    def file_stem(self) -> str:
        return self.__file_path.stem

    # ---------------------------------------------------------
    # Polymorphism (OOP extensibility)
    # ---------------------------------------------------------

    @property
    def searcher_type(self) -> str:
        """Polymorphic identifier."""
        return "JSONL"

    def supports(self, extension: str) -> bool:
        """Return True if searcher can handle this file type."""
        return extension.lower() == ".jsonl"

    def validate(self) -> bool:
        """Check if file is valid for searching."""
        return self.file_exists and self.file_suffix == ".jsonl"

    # ---------------------------------------------------------
    # Main Search Operation
    # ---------------------------------------------------------

    def search(self, keyword: str) -> int:
        """Search for a keyword and return number of occurrences."""

        if not self.validate():
            raise ValueError(
                f"Invalid file for JSONL search: {self.__file_path}"
            )

        keyword_lower = keyword.lower()
        count = 0

        try:
            with self.__file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data: Any = json.loads(line)
                        if not isinstance(data, dict):
                            continue

                        content = str(data.get("content", "")).lower()
                        title = str(data.get("title", "")).lower()

                        count += content.count(keyword_lower)
                        count += title.count(keyword_lower)

                    except json.JSONDecodeError:
                        # Skip invalid lines silently
                        continue

        except OSError as e:
            raise OSError(
                f"Failed to read file '{self.__file_path}': {e}"
            ) from e

        return count

    # ---------------------------------------------------------
    # Magic / Utility Methods
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return f"JSONLSearcher(file={self.file_name})"

    def __repr__(self) -> str:
        return f"JSONLSearcher(file_path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JSONLSearcher):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path))

    def __len__(self) -> int:
        return len(str(self.__file_path))

    def __bool__(self) -> bool:
        return self.file_exists

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, JSONLSearcher):
            return NotImplemented
        return str(self.__file_path) < str(other.__file_path)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, text: str) -> bool:
        """Check if text appears in file path."""
        return text.lower() in str(self.__file_path).lower()
