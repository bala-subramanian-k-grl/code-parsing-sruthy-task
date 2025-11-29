"""
Performance testing utilities with full OOP design.

Enhancements:
- Lifecycle hooks (setup → run_operation → teardown)
- Encapsulation: _result, _errors, _start_time, _end_time
- Advanced polymorphism through run_operation()
- Composition-based logging (PerformanceLogger)
- Factory pattern for utility creation
- Consistent with mock_data, file_utils, validation_utils design
- Backward-compatible functional API preserved
"""

from __future__ import annotations

import time
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable

# ============================================================
# Logger (Composition)
# ============================================================

class BasePerformanceLogger(ABC):
    """Abstract base logger for performance."""

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError


class PerformanceLogger(BasePerformanceLogger):
    """Logger used via composition to trace performance utilities."""

    def __init__(self) -> None:
        self.__log_count = 0

    def log(self, message: str) -> None:
        self.__log_count += 1
        print(f"[PERF LOG] {message}")

    def __str__(self) -> str:
        return f"PerformanceLogger(logs={self.__log_count})"

    def __len__(self) -> int:
        return self.__log_count

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "PerformanceLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PerformanceLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ============================================================
# Abstract Performance Utility (Full OOP)
# ============================================================

class BasePerformanceUtility(ABC):
    """
    Abstract base class for performance utilities.

    Provides:
    - Encapsulated state (_result, _errors, times)
    - Composition-based logging
    - Lifecycle pipeline:
        setup() → run_operation() → teardown()
    - Unified API: execute()
    """

    def __init__(self, logger: PerformanceLogger | None = None) -> None:
        self._logger = logger or PerformanceLogger()     # Composition
        self._result: Any = None                        # Encapsulation
        self._errors: list[str] = []                    # Encapsulation
        self._start_time: float = 0.0                   # Encapsulation
        self._end_time: float = 0.0                     # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    # ------------------- Lifecycle Hooks -------------------

    def setup(self) -> None:
        self._logger.log(f"Setting up {self.__class__.__name__}...")
        self._start_time = time.perf_counter()

    @abstractmethod
    def run_operation(self) -> Any:
        """Child classes implement the core operation."""
        pass

    def teardown(self) -> None:
        self._end_time = time.perf_counter()
        elapsed = round(self._end_time - self._start_time, 4)
        self._logger.log(
            f"Tearing down {self.__class__.__name__} "
            f"(Duration: {elapsed}s)"
        )

    # ------------------- Unified Public API -------------------

    def execute(self) -> Any:
        """
        Execute the performance utility using lifecycle hooks.
        """
        try:
            self.setup()
            self._result = self.run_operation()
        except Exception as e:
            self._errors.append(str(e))
            self._logger.log(f"ERROR: {e}")
            raise
        finally:
            self.teardown()
        return self._result

    # ------------------- Public Accessors -------------------

    @property
    def result(self) -> Any:
        return self._result

    @property
    def errors(self) -> list[str]:
        return list(self._errors)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> bool:
        return len(self._errors) == 0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ============================================================
# Concrete Utilities (Inheritance + Polymorphism)
# ============================================================

class LargeDatasetGenerator(BasePerformanceUtility):
    """Generate large mock datasets."""

    def __init__(
        self, size: int, logger: PerformanceLogger | None = None
    ) -> None:
        super().__init__(logger)
        self._size = size  # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    def run_operation(self) -> list[dict[str, Any]]:
        self._logger.log(f"Generating dataset of size {self._size}...")

        return [
            {"id": i, "data": f"item_{i}" * 10, "value": i * 2}
            for i in range(self._size)
        ]

    def __str__(self) -> str:
        return "LargeDatasetGenerator()"

    def __repr__(self) -> str:
        return "LargeDatasetGenerator()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LargeDatasetGenerator)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ExecutionTimer(BasePerformanceUtility):
    """Measure execution time of any function."""

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        logger: PerformanceLogger | None = None
    ) -> None:
        super().__init__(logger)
        self._func = func     # Encapsulation
        self._args = args     # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    def run_operation(self) -> tuple[Any, float]:
        self._logger.log(
            f"Measuring time for: {self._func.__name__}"
        )

        start = time.perf_counter()
        result = self._func(*self._args)
        elapsed = time.perf_counter() - start

        return result, elapsed

    def __str__(self) -> str:
        return "ExecutionTimer()"

    def __repr__(self) -> str:
        return "ExecutionTimer()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExecutionTimer)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class BenchmarkRunner(BasePerformanceUtility):
    """Benchmark an operation across multiple iterations."""

    def __init__(
        self,
        func: Callable[[], None],
        iterations: int = 100,
        logger: PerformanceLogger | None = None
    ) -> None:
        super().__init__(logger)
        self._func = func                # Encapsulation
        self._iterations = iterations    # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    def run_operation(self) -> dict[str, float]:
        self._logger.log(
            f"Benchmarking {self._func.__name__} for "
            f"{self._iterations} iterations..."
        )

        times: list[float] = []
        for _ in range(self._iterations):
            start = time.perf_counter()
            self._func()
            times.append(time.perf_counter() - start)

        return {
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
        }

    def __str__(self) -> str:
        return "BenchmarkRunner()"

    def __repr__(self) -> str:
        return "BenchmarkRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BenchmarkRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Factory Pattern
# ============================================================

class BasePerformanceFactory(ABC):
    """Abstract base factory for performance utilities."""

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class PerformanceUtilityFactory(BasePerformanceFactory):
    """Factory for creating performance utilities."""

    def __init__(self) -> None:
        self.__creation_count = 0

    def create(
        self,
        utility_type: str,
        func: Callable[..., Any] | None = None,
        iterations: int = 100,
        size: int | None = None,
        *args: Any,
        logger: PerformanceLogger | None = None
    ) -> BasePerformanceUtility:

        if utility_type == "dataset":
            if size is None:
                raise ValueError("size required for dataset generator")
            self.__creation_count += 1
            return LargeDatasetGenerator(size, logger)

        if utility_type == "timer":
            if func is None:
                raise ValueError("func required for timer utility")
            self.__creation_count += 1
            return ExecutionTimer(func, *args, logger=logger)

        if utility_type == "benchmark":
            if func is None:
                raise ValueError("func required for benchmark utility")
            self.__creation_count += 1
            return BenchmarkRunner(func, iterations, logger)

        raise ValueError(f"Unknown utility type: {utility_type}")

    def __str__(self) -> str:
        return f"PerformanceUtilityFactory(created={self.__creation_count})"

    def __len__(self) -> int:
        return self.__creation_count

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "PerformanceUtilityFactory()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PerformanceUtilityFactory)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ============================================================
# Backward-Compatible Functional API
# ============================================================

def generate_large_dataset(size: int) -> list[dict[str, Any]]:
    return LargeDatasetGenerator(size).execute()


def measure_execution_time(
    func: Callable[..., Any], *args: Any
) -> tuple[Any, float]:
    return ExecutionTimer(func, *args).execute()


def benchmark_operation(
    func: Callable[[], None], iterations: int = 100
) -> dict[str, float]:
    return BenchmarkRunner(func, iterations).execute()
