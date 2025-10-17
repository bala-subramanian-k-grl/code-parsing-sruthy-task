"""Search entry point with OOP principles."""

import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from src.config.constants import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SEARCH_FILE,
    MAX_TERM_LENGTH,
)
from src.loggers.logger import get_logger
from src.support.search.jsonl_search import JSONLSearcher
from src.support.search.search_app import SearchApp
from src.support.search.search_display import SearchDisplay
from src.utils.decorators import timing


class BaseRunner(ABC):  # Abstraction
    """Abstract runner (Abstraction, Encapsulation)."""

    def __init__(self) -> None:
        """Initialize base runner."""
        self._app = None  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod  # Abstraction
    def create_app(self, file_path: str) -> SearchApp:
        pass

    @timing
    def run(self, term: str, file_path: str) -> None:  # Template method
        """Run search with sanitized inputs."""
        # Sanitize inputs to prevent command injection
        safe_term = self._sanitize_input(term)
        self._app = self.create_app(file_path)  # Encapsulation
        self._app.run(safe_term)  # Polymorphism

    def _sanitize_input(self, term: str) -> str:  # Encapsulation
        """Sanitize search term to prevent command injection."""
        # Remove dangerous characters and limit length
        safe_chars = "".join(c for c in term if c.isalnum() or c in " -_")
        return safe_chars[:MAX_TERM_LENGTH]  # Limit length


class SearchRunner(BaseRunner):  # Inheritance
    """Search runner (Inheritance, Polymorphism)."""

    def create_app(self, file_path: str) -> SearchApp:  # Polymorphism
        """Create search application."""
        searcher = JSONLSearcher(file_path)  # Factory pattern
        display = SearchDisplay()
        return SearchApp(searcher, display)


class RunnerFactory:  # Abstraction
    """Runner factory (Abstraction, Encapsulation)."""

    @staticmethod  # Encapsulation
    def create_runner(runner_type: str = "search") -> BaseRunner:
        """Create runner instance."""
        if runner_type == "search":
            return SearchRunner()  # Polymorphism
        raise ValueError(f"Invalid runner type: {runner_type}")


@timing
def main() -> None:
    """Main entry point using OOP principles."""
    logger = get_logger(__name__, Path(DEFAULT_OUTPUT_DIR))

    if len(sys.argv) < 2:
        logger.error("Usage: python search.py <search_term> [jsonl_file]")
        sys.exit(1)

    term = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SEARCH_FILE

    try:
        # Factory pattern (Abstraction)
        runner = RunnerFactory.create_runner("search")  # Polymorphism
        runner.run(term, file_path)  # Polymorphism
    except Exception as e:
        logger.error(f"Search failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
