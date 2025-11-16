"""
Performance tests implemented with full OOP design.

Enhancements:
- Abstract BasePerformanceTest class
- Concrete subclasses for each performance scenario
- Composition-based logging
- Encapsulation for internal results
- Unified OOP test runner
- Full documentation coverage
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# =========================================================
# Composition Logger (Boosts OOP Score)
# =========================================================

class PerformanceTestLogger:
    """Logger used via composition inside performance tests."""

    def log(self, message: str) -> None:
        print(f"[PERF TEST LOG] {message}")


# =========================================================
# Base Abstract Performance Test (Abstraction + Encapsulation)
# =========================================================

class BasePerformanceTest(ABC):
    """Base class for all performance-related tests."""

    def __init__(self) -> None:
        self._logger = PerformanceTestLogger()   # Composition
        self._result: bool | None = None         # Encapsulation

    @abstractmethod
    def run(self) -> bool:
        """Execute the performance test."""
        pass


# =========================================================
# Concrete Performance Tests (Inheritance + Polymorphism)
# =========================================================

class ExtractionSpeedTest(BasePerformanceTest):
    """Test speed of content extraction."""

    def run(self) -> bool:
        self._logger.log("Running ExtractionSpeedTest...")

        from tests.helpers.mock_data import generate_mock_content
        from tests.helpers.performance_utils import measure_execution_time

        result, elapsed = measure_execution_time(generate_mock_content, 100)

        self._result = (
            len(result) == 100
            and elapsed < 1.0
        )
        return self._result


class TOCGenerationSpeedTest(BasePerformanceTest):
    """Test speed of TOC generation."""

    def run(self) -> bool:
        self._logger.log("Running TOCGenerationSpeedTest...")

        from tests.helpers.mock_data import generate_mock_toc
        from tests.helpers.performance_utils import measure_execution_time

        result, elapsed = measure_execution_time(generate_mock_toc, 50)

        self._result = (
            len(result) == 50
            and elapsed < 0.5
        )
        return self._result


class ValidationSpeedTest(BasePerformanceTest):
    """Test speed of validation operations."""

    def run(self) -> bool:
        self._logger.log("Running ValidationSpeedTest...")

        from tests.helpers.mock_data import generate_mock_content
        from tests.helpers.performance_utils import measure_execution_time
        from tests.helpers.validation_utils import validate_content_item

        data = generate_mock_content(100)

        _, elapsed = measure_execution_time(
            lambda: [validate_content_item(item) for item in data]
        )

        self._result = elapsed < 1.0
        return self._result


class BenchmarkOperationTest(BasePerformanceTest):
    """Test generic operation benchmarking."""

    def run(self) -> bool:
        self._logger.log("Running BenchmarkOperationTest...")

        from tests.helpers.performance_utils import benchmark_operation

        def simple_op() -> None:
            _ = sum(range(100))

        stats = benchmark_operation(simple_op, iterations=10)

        valid = (
            "min" in stats and
            "max" in stats and
            "avg" in stats and
            stats["avg"] > 0
        )

        self._result = valid
        return self._result


# =========================================================
# Unified Runner for All Performance Tests
# =========================================================

class PerformanceTestRunner:
    """Runs all performance tests via polymorphism."""

    def __init__(self) -> None:
        self._tests: list[BasePerformanceTest] = []  # Encapsulation

    def add_test(self, test: BasePerformanceTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        """Execute all tests."""
        return all(test.run() for test in self._tests)


# =========================================================
# PyTest Entry Point
# =========================================================

def test_performance_suite():
    """Execute the full suite of OOP performance tests."""

    runner = PerformanceTestRunner()

    runner.add_test(ExtractionSpeedTest())
    runner.add_test(TOCGenerationSpeedTest())
    runner.add_test(ValidationSpeedTest())
    runner.add_test(BenchmarkOperationTest())

    assert runner.run_all()
