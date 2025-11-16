"""Base test suite and runner."""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class TestProtocol(Protocol):
    """Protocol defining the interface for test objects."""

    def run(self) -> dict[str, Any]:
        """Run a single test and return its results."""
        ...


class BaseSuite(ABC):
    """Abstract base class for test suites."""

    def __init__(self) -> None:
        """Initialize suite."""
        self._tests: list[TestProtocol] = []

    @abstractmethod
    def run(self) -> dict[str, Any]:
        """Run test suite and return aggregated results."""

    def add_test(self, test: TestProtocol) -> None:
        """Add test to suite."""
        self._tests.append(test)

    @property
    def tests(self) -> list[TestProtocol]:
        """Get all tests in the suite."""
        return self._tests

    def _execute_all_tests(self) -> list[dict[str, Any]]:
        """Execute all tests and return their results."""
        results: list[dict[str, Any]] = []
        for test in self._tests:
            try:
                results.append(test.run())
            except Exception as e:
                results.append({
                    "error": str(e),
                    "test_name": getattr(test, "__name__", "unknown"),
                })
        return results
