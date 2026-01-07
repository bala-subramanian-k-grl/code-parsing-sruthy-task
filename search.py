"""
Professional search CLI with OOP principles.
Supports searching in content, tables, figures, and TOC.
"""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.search.jsonl_searcher import JSONLSearcher
from src.utils.logger import logger
from src.utils.timer import timer


class SearchError(Exception):
    """Custom exception for search errors."""
    pass


class BaseSearchConfig(ABC):
    """Abstract base for search configuration."""

    def __init__(self, keyword: str, file_type: str = "content") -> None:
        self._keyword = keyword
        self._file_type = file_type
        self._file_map = {
            "content": "outputs/usb_pd_spec.jsonl",
            "tables": "outputs/extracted_tables.jsonl",
            "figures": "outputs/extracted_figures.jsonl",
            "toc": "outputs/usb_pd_toc.jsonl"
        }

    @property
    def keyword(self) -> str:
        """Get search keyword."""
        return self._keyword

    @property
    def file_type(self) -> str:
        """Get file type."""
        return self._file_type

    @property
    def file_path(self) -> Path:
        """Get file path for search."""
        path_str = self._file_map.get(self._file_type, self._file_map["content"])
        return Path(path_str)

    @abstractmethod
    def validate(self) -> None:
        """Validate configuration."""
        pass

    def __str__(self) -> str:
        return f"SearchConfig(keyword={self._keyword}, type={self._file_type})"

    def __repr__(self) -> str:
        return f"SearchConfig(keyword={self._keyword!r}, file_type={self._file_type!r})"


class SearchConfig(BaseSearchConfig):
    """Concrete search configuration with validation."""

    def validate(self) -> None:
        """Validate search configuration."""
        if not self._keyword or not self._keyword.strip():
            raise SearchError("Keyword cannot be empty")

        if self._file_type not in self._file_map:
            valid = ", ".join(self._file_map.keys())
            raise SearchError(f"Invalid file type. Valid: {valid}")

        if not self.file_path.exists():
            raise SearchError(f"File not found: {self.file_path}")


class SearchExecutor:
    """Execute search operations with encapsulation."""

    def __init__(self, config: SearchConfig) -> None:
        self._config = config
        self._results_count = 0
        self._searcher: JSONLSearcher | None = None

    @property
    def results_count(self) -> int:
        """Get number of results found."""
        return self._results_count

    def execute(self) -> int:
        """Execute search and return result count."""
        self._config.validate()

        logger.info(
            f"Searching for '{self._config.keyword}' "
            f"in {self._config.file_path.name}"
        )

        try:
            self._searcher = JSONLSearcher(self._config.file_path)
            self._results_count = self._searcher.search(self._config.keyword)

            logger.info(
                f"Found '{self._config.keyword}' {self._results_count} times "
                f"in {self._config.file_path.name}"
            )

            return self._results_count

        except (OSError, ValueError) as e:
            logger.error(f"Search failed: {e}")
            raise SearchError(f"Search execution failed: {e}") from e

    def get_metadata(self) -> dict[str, Any]:
        """Get search metadata."""
        return {
            "keyword": self._config.keyword,
            "file_type": self._config.file_type,
            "file_path": str(self._config.file_path),
            "results_count": self._results_count
        }

    def __str__(self) -> str:
        return f"SearchExecutor(results={self._results_count})"

    def __repr__(self) -> str:
        return f"SearchExecutor(config={self._config!r}, results={self._results_count})"

    def __len__(self) -> int:
        return self._results_count

    def __bool__(self) -> bool:
        return self._results_count > 0


class SearchCLI:
    """Command-line interface for search operations."""

    def __init__(self, args: list[str]) -> None:
        self._args = args
        self._config: SearchConfig | None = None
        self._executor: SearchExecutor | None = None

    def run(self) -> int:
        """Run CLI application."""
        try:
            if not self._parse_args():
                self._show_usage()
                return 1

            self._config = SearchConfig(
                self._args[1],
                self._args[2] if len(self._args) > 2 else "content"
            )

            self._executor = SearchExecutor(self._config)

            print(f"\nSearching for '{self._config.keyword}' "
                  f"in {self._config.file_type}...\n")

            count = self._executor.execute()

            print(f"\nFound {count} matches for '{self._config.keyword}'")

            return 0

        except SearchError as e:
            print(f"Error: {e}")
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}")
            return 1

    def _parse_args(self) -> bool:
        """Parse command-line arguments."""
        return len(self._args) >= 2

    def _show_usage(self) -> None:
        """Display usage information."""
        print("Usage: python search.py <keyword> [file_type]")
        print("  file_type: content (default), tables, figures, toc")
        print("\nExamples:")
        print("  python search.py 'Power Delivery'")
        print("  python search.py voltage tables")
        print("  python search.py diagram figures")

    def __str__(self) -> str:
        return "SearchCLI()"

    def __repr__(self) -> str:
        return f"SearchCLI(args={self._args!r})"


@timer
def main() -> None:
    """Main entry point with OOP design."""
    cli = SearchCLI(sys.argv)
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
