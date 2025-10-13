import logging
from typing import Any


class SearchDisplay:  # Encapsulation
    def __init__(self, max_results: int = 10):
        self._max_results = max_results  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)

    def show(self, matches: list[dict[str, Any]], term: str) -> None:  # Abstraction
        self._logger.info(
            f"Displaying {min(len(matches), self._max_results)} of {len(matches)} matches for '{term}'"
        )
        print(f"Found {len(matches)} matches for '{term}':")
        for match in matches[: self._max_results]:
            print(f"Page {match['page']} ({match['type']}): {match['content']}")
        if len(matches) > self._max_results:
            print(f"... and {len(matches) - self._max_results} more matches")
            self._logger.info(
                f"Truncated display: showing {self._max_results} of {len(matches)} total matches"
            )
