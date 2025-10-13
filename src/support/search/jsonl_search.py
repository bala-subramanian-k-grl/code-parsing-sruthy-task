
import json
from typing import Any
from .base_search import BaseSearcher  # Importing the base class
class JSONLSearcher(BaseSearcher):  # Inheritance
    def search(self, term: str) -> list[dict[str, Any]]:  # Polymorphism
        self._logger.info(f"Starting search for term: '{term}'")
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
        
        self._logger.info(f"Search completed: Found {len(matches)} matches for '{term}'")
        return matches