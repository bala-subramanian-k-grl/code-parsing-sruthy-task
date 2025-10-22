"""JSONL search with polymorphism."""

import json
from typing import Any

from src.config.constants import CONTENT_PREVIEW_LENGTH
from src.utils.decorators import log_execution, timing

from .base_search import BaseSearcher  # Importing the base class


class JSONLSearcher(BaseSearcher):  # Polymorphic implementation
    """JSONL file searcher with polymorphism."""

    def get_search_type(self) -> str:  # Polymorphism
        """Get search implementation type."""
        return "jsonl"
    @timing
    @log_execution
    def search(self, term: str) -> list[dict[str, Any]]:  # Polymorphism
        self._logger.info("Starting search for term: '%s'", term)
        matches: list[dict[str, Any]] = []
        try:
            with open(self._file_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        item: dict[str, Any] = json.loads(line)
                        content: str = item.get("content", "")
                        if term.lower() in content.lower():
                            preview = content[:CONTENT_PREVIEW_LENGTH]
                            if len(content) > CONTENT_PREVIEW_LENGTH:
                                preview += "..."
                            matches.append(
                                {
                                    "page": item.get("page", "N/A"),
                                    "type": item.get("type", "N/A"),
                                    "content": preview,
                                }
                            )
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            self._logger.error("File not found: %s", self._file_path)

        match_count = len(matches)
        self._logger.info(
            "Search completed: Found %s matches for '%s'", match_count, term
        )
        return matches
