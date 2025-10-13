#!/usr/bin/env python3
# USB PD Specification Parser - Search Entry Point
"""Search entry point with OOP principles."""

import logging
import sys
from abc import ABC, abstractmethod

from src.support.search.jsonl_search import JSONLSearcher
from src.support.search.search_display import SearchDisplay
from src.support.search.search_app import SearchApp
class BaseRunner(ABC):  # Abstraction
    """Abstract runner (Abstraction, Encapsulation)."""

    def __init__(self):
        self._app = None  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod  # Abstraction
    def create_app(self, file_path: str) -> SearchApp:
        pass

    def run(self, term: str, file_path: str) -> None:  # Template method
        # Sanitize inputs to prevent command injection
        safe_term = self._sanitize_input(term)
        self._app = self.create_app(file_path)  # Encapsulation
        self._app.run(safe_term)  # Polymorphism

    def _sanitize_input(self, term: str) -> str:  # Encapsulation
        """Sanitize search term to prevent command injection."""
        # Remove dangerous characters and limit length
        safe_chars = "".join(c for c in term if c.isalnum() or c in " -_")
        return safe_chars[:100]  # Limit length


class SearchRunner(BaseRunner):  # Inheritance
    """Search runner (Inheritance, Polymorphism)."""

    def create_app(self, file_path: str) -> SearchApp:  # Polymorphism
        searcher = JSONLSearcher(file_path)  # Factory pattern
        display = SearchDisplay()
        return SearchApp(searcher, display)


class RunnerFactory:  # Abstraction
    """Runner factory (Abstraction, Encapsulation)."""

    @staticmethod  # Encapsulation
    def create_runner(runner_type: str = "search") -> BaseRunner:
        if runner_type == "search":
            return SearchRunner()  # Polymorphism
        raise ValueError(f"Invalid runner type: {runner_type}")


def main():
    """Main entry point using OOP principles."""
    # Setup stream logger to capture all output to parser.log
    from pathlib import Path
    
    log_file = Path("outputs") / "parser.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger to write to file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, mode='a'),  # Append to existing log
            logging.StreamHandler()  # Also keep console output
        ]
    )
    
    logger = logging.getLogger(__name__)

    if len(sys.argv) < 2:
        logger.error("Usage: python search.py <search_term> [jsonl_file]")
        sys.exit(1)

    term = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else "outputs/usb_pd_spec.jsonl"

    try:
        # Factory pattern (Abstraction)
        runner = RunnerFactory.create_runner("search")  # Polymorphism
        runner.run(term, file_path)  # Polymorphism
    except Exception as e:
        logger.error(f"Search failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
