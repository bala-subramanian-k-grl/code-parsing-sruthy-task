from .base_search import BaseSearcher
from .search_display import SearchDisplay


class SearchApp:  # Composition
    def __init__(self, searcher: BaseSearcher, display: SearchDisplay):
        self._searcher = searcher  # Encapsulation
        self._display = display  # Encapsulation
    
    def __str__(self) -> str:  # Magic Method
        return f"SearchApp(searcher={type(self._searcher).__name__})"
    
    def __call__(self, term: str) -> None:  # Magic Method
        return self.run(term)

    def run(self, term: str) -> None:  # Polymorphism
        matches = self._searcher.search(term)  # Polymorphism
        self._display.show(matches, term)