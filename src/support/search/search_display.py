"""Module for displaying search results with logging and encapsulation."""

import logging
from typing import Any


class SearchDisplay:  # Encapsulation
    def __init__(self, max_results: int = 10):
        """Initialize search display with max results limit."""
        self._max_results = max_results  # Encapsulation
        class_name = self.__class__.__name__
        self._logger = logging.getLogger(class_name)

    def show(self, matches: list[dict[str, Any]], term: str) -> None:
        """Display search results with pagination."""
        display_count = min(len(matches), self._max_results)
        total_count = len(matches)
        msg = f"Displaying {display_count} of {total_count} matches for '{term}'"
        self._logger.info(msg)
        count = len(matches)
        print(f"Found {count} matches for '{term}':")
        for match in matches[: self._max_results]:
            page_info = f"Page {match['page']} ({match['type']})"
            print(f"{page_info}: {match['content']}")
        if len(matches) > self._max_results:
            remaining = len(matches) - self._max_results
            print(f"... and {remaining} more matches")
            total = len(matches)
            truncate_msg = (
                f"Truncated display: showing {self._max_results} "
                f"of {total} total matches"
            )
            self._logger.info(truncate_msg)
