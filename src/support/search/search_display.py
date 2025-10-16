"""Module for displaying search results with logging and encapsulation."""

import logging
from typing import Any


class SearchDisplay:  # Encapsulation
    def __init__(self, max_results: int = 10):
        self._max_results = max_results  # Encapsulation
        self._logger = logging.getLogger(
            self.__class__.__name__
        )

    def show(self, matches: list[dict[str, Any]], term: str) -> None:  # Abstraction
        display_count = min(len(matches), self._max_results)
        total_count = len(matches)
        self._logger.info(
            f"Displaying {display_count} of {total_count} matches for '{term}'"
        )
        print(f"Found {len(matches)} matches for '{term}':")
        for match in matches[: self._max_results]:
            page_info = f"Page {match['page']} ({match['type']})"
            print(f"{page_info}: {match['content']}")
        if len(matches) > self._max_results:
            remaining = len(matches) - self._max_results
            print(f"... and {remaining} more matches")
            truncate_msg = (
                f"Truncated display: showing {self._max_results} "
                f"of {len(matches)} total matches"
            )
            self._logger.info(truncate_msg)
