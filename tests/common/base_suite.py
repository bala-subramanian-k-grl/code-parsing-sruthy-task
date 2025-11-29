"""Base test suite and runner (clean enterprise OOP version)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TestProtocol(Protocol):
    """Protocol defining the interface for test objects."""

    def run(self) -> dict[str, Any]:
        """Run a single test and return its results."""
        ...


class BaseSuite(ABC):
    """Abstract base class for test suites."""

    def __init__(self) -> None:
        """Initialize suite with an empty test list."""
        self.__tests: list[TestProtocol] = []
        self.__run_count = 0
        self.__pass_count = 0
        self.__fail_count = 0

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    @abstractmethod
    def run(self) -> dict[str, Any]:
        """Run test suite and return aggregated results."""
        raise NotImplementedError

    def add_test(self, test: TestProtocol) -> None:
        """Add a test to the suite."""
        self.__tests.append(test)

    @property
    def tests(self) -> list[TestProtocol]:
        """Return all registered tests."""
        return self.__tests

    @property
    def run_count(self) -> int:
        return self.__run_count

    @property
    def pass_count(self) -> int:
        return self.__pass_count

    @property
    def fail_count(self) -> int:
        return self.__fail_count

    # ------------------------------------------------------------
    # Internal executor (template behavior)
    # ------------------------------------------------------------
    def _execute_all_tests(self) -> list[dict[str, Any]]:
        """
        Execute all tests and return their individual results.
        Safely captures errors and continues running remaining tests.
        """
        self.__run_count += 1
        results: list[dict[str, Any]] = []

        for test in self.__tests:
            try:
                result = test.run()
                results.append(result)
                if result.get("status") == "passed":
                    self.__pass_count += 1
                else:
                    self.__fail_count += 1
            except Exception as e:
                self.__fail_count += 1
                results.append({
                    "status": "error",
                    "error": str(e),
                    "test_name": getattr(
                        test, "__class__", type(test)
                    ).__name__,
                })

        return results

    # ------------------------------------------------------------
    # Pythonic utilities (makes suite easier to work with)
    # ------------------------------------------------------------
    def __len__(self) -> int:
        """Return number of tests in the suite."""
        return len(self.__tests)

    def __iter__(self):
        """Iterate directly over registered tests."""
        return iter(self.__tests)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(tests={len(self)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> bool:
        return len(self.__tests) > 0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)
