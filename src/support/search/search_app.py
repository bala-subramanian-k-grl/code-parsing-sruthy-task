from .base_search import BaseSearcher
from .search_display import SearchDisplay


class SearchApp:  # Composition
    def __init__(self, searcher: BaseSearcher, display: SearchDisplay):
        self._searcher = searcher  # Encapsulation
        self._display = display  # Encapsulation

    def run(self, term: str) -> None:  # Polymorphism
        matches = self._searcher.search(term)  # Polymorphism
        self._display.show(matches, term)