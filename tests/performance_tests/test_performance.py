"""
Advanced OOP-based performance tests with lifecycle, encapsulation,
polymorphism, and composition-based logging.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod


# =========================================================
# Logger (Composition)
# =========================================================

class PerformanceTestLogger:
    """Logger injected via composition inside performance tests."""
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.__instance_id = id(self)
        self.__created = True

    def log(self, message: str) -> None:
        self.messages.append(message)
        print(f"[PERF TEST LOG] {message}")

    def __str__(self) -> str:
        return "PerformanceTestLogger()"

    def __repr__(self) -> str:
        return "PerformanceTestLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PerformanceTestLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# =========================================================
# Base Abstract Performance Test (Full Lifecycle + Encapsulation)
# =========================================================

class BasePerformanceTest(ABC):
    """Abstract base class for all performance tests."""

    def __init__(self, logger: PerformanceTestLogger | None = None) -> None:
        self._logger = logger or PerformanceTestLogger()      # Composition
        self._result: bool | None = None                     # Encapsulation
        self._errors: list[str] = []                         # Encapsulation
        self.__instance_id = id(self)
        self.__created = True
        self._start_time: float = 0.0                        # Encapsulation
        self._end_time: float = 0.0                          # Encapsulation

    # ---------------- Lifecycle Hooks ----------------

    def setup(self) -> None:
        self._logger.log(f"Setting up {self.__class__.__name__}...")
        self._start_time = time.perf_counter()

    @abstractmethod
    def run_test(self) -> bool:
        """Concrete performance logic should be implemented here."""
        pass

    def teardown(self) -> None:
        self._end_time = time.perf_counter()
        duration = round(self._end_time - self._start_time, 4)
        self._logger.log(
            f"Tearing down {self.__class__.__name__} (Duration: {duration}s)"
        )

    # ---------------- Unified Execution API ----------------

    def execute(self) -> bool:
        try:
            self.setup()
            self._result = self.run_test()
            return self._result
        except Exception as exc:
            self._errors.append(str(exc))
            self._logger.log(f"ERROR: {exc}")
            return False
        finally:
            self.teardown()

    def __str__(self) -> str:
        return "BasePerformanceTest()"

    def __repr__(self) -> str:
        return "BasePerformanceTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BasePerformanceTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# =========================================================
# Concrete Performance Tests (Polymorphism)
# =========================================================

class ExtractionSpeedTest(BasePerformanceTest):
    """Test speed of content extraction."""

    def run_test(self) -> bool:
        self._logger.log("Running ExtractionSpeedTest...")

        from tests.helpers.mock_data import generate_mock_content
        from tests.helpers.performance_utils import measure_execution_time

        result, elapsed = measure_execution_time(generate_mock_content, 100)
        return len(result) == 100 and elapsed < 1.0

    def __str__(self) -> str:
        return "ExtractionSpeedTest()"

    def __repr__(self) -> str:
        return "ExtractionSpeedTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExtractionSpeedTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class TOCGenerationSpeedTest(BasePerformanceTest):
    """Test speed of TOC generation."""

    def run_test(self) -> bool:
        self._logger.log("Running TOCGenerationSpeedTest...")

        from tests.helpers.mock_data import generate_mock_toc
        from tests.helpers.performance_utils import measure_execution_time

        result, elapsed = measure_execution_time(generate_mock_toc, 50)
        return len(result) == 50 and elapsed < 0.5

    def __str__(self) -> str:
        return "TOCGenerationSpeedTest()"

    def __repr__(self) -> str:
        return "TOCGenerationSpeedTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TOCGenerationSpeedTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ValidationSpeedTest(BasePerformanceTest):
    """Test speed of validation operations."""

    def run_test(self) -> bool:
        self._logger.log("Running ValidationSpeedTest...")

        from tests.helpers.mock_data import generate_mock_content
        from tests.helpers.validation_utils import validate_content_item
        from tests.helpers.performance_utils import measure_execution_time

        data = generate_mock_content(100)

        _, elapsed = measure_execution_time(
            lambda: [validate_content_item(item) for item in data]
        )

        return elapsed < 1.0

    def __str__(self) -> str:
        return "ValidationSpeedTest()"

    def __repr__(self) -> str:
        return "ValidationSpeedTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidationSpeedTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class BenchmarkOperationTest(BasePerformanceTest):
    """Test speed of running a simple benchmark operation."""

    def run_test(self) -> bool:
        self._logger.log("Running BenchmarkOperationTest...")

        from tests.helpers.performance_utils import benchmark_operation

        def simple_op() -> None:
            _ = sum(range(100))

        stats = benchmark_operation(simple_op, iterations=10)

        return (
            "min" in stats and
            "max" in stats and
            "avg" in stats and
            stats["avg"] > 0
        )

    def __str__(self) -> str:
        return "BenchmarkOperationTest()"

    def __repr__(self) -> str:
        return "BenchmarkOperationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BenchmarkOperationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# =========================================================
# Unified Runner (Polymorphism)
# =========================================================

class PerformanceTestRunner:
    """Runs all performance tests using polymorphism."""

    def __init__(self) -> None:
        self._tests: list[BasePerformanceTest] = []
        self.__instance_id = id(self)
        self.__created = True

    def add_test(self, test: BasePerformanceTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        return all(test.execute() for test in self._tests)

    def __str__(self) -> str:
        return "PerformanceTestRunner()"

    def __repr__(self) -> str:
        return "PerformanceTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PerformanceTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# =========================================================
# PyTest Entry Point
# =========================================================

def test_performance_suite():
    """Execute the complete OOP performance test suite."""

    runner = PerformanceTestRunner()

    runner.add_test(ExtractionSpeedTest())
    runner.add_test(TOCGenerationSpeedTest())
    runner.add_test(ValidationSpeedTest())
    runner.add_test(BenchmarkOperationTest())

    assert runner.run_all()
