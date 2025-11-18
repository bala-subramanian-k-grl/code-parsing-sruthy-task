"""JSONL file searcher."""

import json
from pathlib import Path
from typing import Any


class JSONLSearcher:
    """Search JSONL files for keywords."""

    def search(self, keyword: str, file_path: Path) -> int:
        """Search for keyword and return count."""
        count = 0
        keyword_lower = keyword.lower()

        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with file_path.open("r", encoding="utf-8") as f:
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
            raise OSError(f"Error reading file {file_path}: {e}") from e

        return count
