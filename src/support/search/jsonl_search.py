"""Module for searching through JSONL files."""

import json
from typing import Any

from src.config.constants import CONTENT_PREVIEW_LENGTH
from src.utils.decorators import log_execution, timing

from .base_search import BaseSearcher  # Importing the base class


class JSONLSearcher(BaseSearcher):  # Inheritance
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
                            matches.append(
                                {
                                    "page": item.get("page", "N/A"),
                                    "type": item.get("type", "N/A"),
                                    "content": (
                                        content[:CONTENT_PREVIEW_LENGTH] + "..."
                                        if len(content) > CONTENT_PREVIEW_LENGTH
                                        else content
                                    ),
                                }
                            )
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            self._logger.error("File not found: %s", self._file_path)

        self._logger.info(
            "Search completed: Found %s matches for '%s'", len(matches), term
        )
        return matches
