"""Module for displaying search result with logging and encapsulation."""

import logging
from typing import Any


class SearchDisplay:  # Encapsulation
    def __init__(self, max_results: int = 10):
        """Initialize search display with max results limit."""
        self.__max_results = max_results  # Private
        class_name = self.__class__.__name__
        self.__logger = logging.getLogger(class_name)  # Private

    def show(self, matches: list[dict[str, Any]], term: str) -> None:
        """Display search results with pagination."""
        display_count = min(len(matches), self.__max_results)
        total_count = len(matches)
        msg = (
            f"Displaying {display_count} of {total_count} "
            f"matches for '{term}'"
        )
        self.__logger.info(msg)
        count = len(matches)
        print(f"Found {count} matches for '{term}':")
        for match in matches[: self.__max_results]:
            page_info = f"Page {match['page']} ({match['type']})"
            print(f"{page_info}: {match['content']}")
        if len(matches) > self.__max_results:
            remaining = len(matches) - self.__max_results
            print(f"... and {remaining} more matches")
            total = len(matches)
            truncate_msg = (
                f"Truncated display: showing {self.__max_results} "
                f"of {total} total matches"
            )
            self.__logger.info(truncate_msg)
