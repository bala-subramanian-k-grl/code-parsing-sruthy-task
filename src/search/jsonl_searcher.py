"""JSONL file searcher."""

import json
from pathlib import Path
from typing import Any


class JSONLSearcher:
    """Search JSONL files for keywords."""

    def __init__(self, file_path: Path) -> None:
        """Initialize searcher with file path."""
        self.__file_path = file_path

    @property
    def file_path(self) -> Path:
        """Get file path."""
        return self.__file_path

    def search(self, keyword: str) -> int:
        """Search for keyword and return count."""
        count = 0
        keyword_lower = keyword.lower()

        if not self.__file_path.is_file():
            raise FileNotFoundError(f"File not found: {self.__file_path}")

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
                        continue
        except OSError as e:
            raise OSError(f"Error reading file {self.__file_path}: {e}") from e

        return count

    def __str__(self) -> str:
        """String representation."""
        return f"JSONLSearcher(file={self.__file_path.name})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"JSONLSearcher(file_path={self.__file_path!r})"
