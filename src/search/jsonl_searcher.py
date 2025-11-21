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

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self.__file_path.exists()

    @property
    def file_name(self) -> str:
        """Get file name."""
        return self.__file_path.name

    @property
    def file_size(self) -> int:
        """Get file size."""
        return self.__file_path.stat().st_size if self.__file_path.exists() else 0

    @property
    def file_suffix(self) -> str:
        """Get file suffix."""
        return self.__file_path.suffix

    @property
    def file_parent(self) -> Path:
        """Get file parent directory."""
        return self.__file_path.parent

    @property
    def file_stem(self) -> str:
        """Get file stem."""
        return self.__file_path.stem

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JSONLSearcher):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path))

    def __len__(self) -> int:
        return len(str(self.__file_path))

    def __bool__(self) -> bool:
        return self.__file_path.exists()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, JSONLSearcher):
            return NotImplemented
        return str(self.__file_path) < str(other.__file_path)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, text: str) -> bool:
        """Check if text in file path."""
        return text in str(self.__file_path)
