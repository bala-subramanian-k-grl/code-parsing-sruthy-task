"""Search application that integrates search functionality and display."""

from typing import Any

from .base_search import BaseSearcher
from .search_display import SearchDisplay


class SearchApp:  # Composition
    def __init__(self, searcher: BaseSearcher, display: SearchDisplay):
        self.__searcher = searcher  # Private encapsulation
        self.__display = display  # Private encapsulation
        self.__search_history: list[str] = []  # Private history
        self.__result_cache: dict[str, list[Any]] = {}  # Private cache

    def __str__(self) -> str:  # Magic Method
        return f"SearchApp(searcher={type(self.__searcher).__name__})"

    def __len__(self) -> int:  # Magic Method
        """Return number of searches performed."""
        return len(self.__search_history)

    def __contains__(self, term: str) -> bool:  # Magic Method
        """Check if term was searched before."""
        return term in self.__search_history

    def __call__(self, term: str) -> None:  # Magic Method
        return self.run(term)

    def run(self, term: str) -> None:  # Polymorphism
        validated_term = self.__validate_search_term(term)
        matches = self.__get_cached_or_search(validated_term)
        self.__show_results(matches, validated_term)
        self.__add_to_history(validated_term)

    def run_cached(self, term: str) -> None:  # Polymorphism
        """Run search with caching enabled."""
        self.run(term)

    def run_fresh(self, term: str) -> None:  # Polymorphism
        """Run search without using cache."""
        validated_term = self.__validate_search_term(term)
        matches = self.__perform_search(validated_term)
        self.__show_results(matches, validated_term)
        self.__add_to_history(validated_term)

    def __validate_search_term(
        self, term: str
    ) -> str:  # Private - only used internally
        """Validate search term."""
        if not term or not term.strip():
            raise ValueError("Search term cannot be empty")
        return term.strip()

    def __perform_search(
        self, term: str
    ) -> list[Any]:  # Private - only used internally
        """Perform the search operation."""
        return self.__searcher.search(term)  # Polymorphism

    def __show_results(
        self, matches: list[Any], term: str
    ) -> None:  # Private - only used internally
        """Show results."""
        self.__display.show(matches, term)

    def __get_cached_or_search(
        self, term: str
    ) -> list[Any]:  # Private - only used internally
        """Get results from cache or perform new search."""
        if term in self.__result_cache:
            return self.__result_cache[term]

        results = self.__perform_search(term)
        self.__result_cache[term] = results
        return results

    def __add_to_history(
        self, term: str
    ) -> None:  # Private - only used internally
        """Add search term to history."""
        if term not in self.__search_history:
            self.__search_history.append(term)

    @property
    def search_history(self) -> list[str]:
        """Get search history (read-only)."""
        return self.__search_history.copy()

    @property
    def cache_size(self) -> int:
        """Get current cache size."""
        return len(self.__result_cache)

    def clear_cache(self) -> None:
        """Clear search result cache."""
        self.__result_cache.clear()

    def clear_history(self) -> None:
        """Clear search history."""
        self.__search_history.clear()


class FastSearchApp(SearchApp):  # Inheritance + Polymorphism
    """Fast search application variant."""

    def run(self, term: str) -> None:  # Method override
        """Fast search execution."""
        super().run_fresh(term)  # Skip cache for speed


class CachedSearchApp(SearchApp):  # Inheritance + Polymorphism
    """Cached search application variant."""

    def run(self, term: str) -> None:  # Method override
        """Cached search execution."""
        super().run_cached(term)  # Always use cache
