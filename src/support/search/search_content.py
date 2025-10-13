# USB PD Specification Parser - Search Content Module
"""Minimal search content with OOP principles."""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseSearcher(ABC):  # Abstraction
    def __init__(self, file_path: str):
        self._file_path = self._validate_path(file_path)  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)  # Encapsulation
        self._logger.info(f"Initialized searcher for file: {self._file_path.name}")

    def _validate_path(self, file_path: str) -> Path:  # Encapsulation
        try:
            # Sanitize input to prevent path traversal
            clean_path = Path(str(file_path).replace("..", "").replace("~", ""))
            resolved_path = clean_path.resolve(strict=False)
            working_dir = Path.cwd().resolve()

            # Prevent path traversal attacks
            if not resolved_path.is_relative_to(working_dir):
                raise ValueError(f"Path traversal detected: {file_path}")

            # Additional security check for file extension
            if resolved_path.suffix not in [".jsonl", ".json"]:
                raise ValueError(f"Invalid file type: {file_path}")

            return resolved_path
        except (OSError, ValueError) as e:
            raise ValueError(f"Invalid file path: {file_path} - {e}") from e

    @abstractmethod  # Abstraction
    def search(self, term: str) -> list[dict[str, Any]]:
        pass


class JSONLSearcher(BaseSearcher):  # Inheritance
    def search(self, term: str) -> list[dict[str, Any]]:  # Polymorphism
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
                                        content[:100] + "..."
                                        if len(content) > 100
                                        else content
                                    ),
                                }
                            )
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            self._logger.error(f"File not found: {self._file_path}")
        return matches


class SearchDisplay:  # Encapsulation
    def __init__(self, max_results: int = 10):
        self._max_results = max_results  # Encapsulation

    def show(self, matches: list[dict[str, Any]], term: str) -> None:  # Abstraction
        print(f"Found {len(matches)} matches for '{term}':")
        for match in matches[: self._max_results]:
            print(f"Page {match['page']} ({match['type']}): {match['content']}")
        if len(matches) > self._max_results:
            print(f"... and {len(matches) - self._max_results} more matches")


class SearchApp:  # Composition
    def __init__(self, searcher: BaseSearcher, display: SearchDisplay):
        self._searcher = searcher  # Encapsulation
        self._display = display  # Encapsulation

    def run(self, term: str) -> None:  # Polymorphism
        matches = self._searcher.search(term)  # Polymorphism
        self._display.show(matches, term)
