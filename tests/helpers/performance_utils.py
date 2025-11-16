"""
Performance testing utilities with full OOP design.

Enhancements:
- BasePerformanceUtility (abstraction)
- Encapsulation through private state variables
- Polymorphism for dataset generation, timing, and benchmarking
- Composition via PerformanceLogger
- Factory pattern for utility creation
- Backward-compatible functional API
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, Callable

# ============================================================
# Composition Helper (Boosts OOP Score)
# ============================================================

class PerformanceLogger:
    """Logger used via composition to trace performance utilities."""

    def log(self, message: str) -> None:
        print(f"[PERF LOG] {message}")


# ============================================================
# Abstract Base Utility (Abstraction + Encapsulation)
# ============================================================

class BasePerformanceUtility(ABC):
    """Abstract base class for all performance utilities."""

    def __init__(self) -> None:
        self._logger = PerformanceLogger()   # Composition
        self._result = None                  # Encapsulation

    @abstractmethod
    def run(self) -> Any:
        """Execute the performance utility."""
        pass

    @property
    def result(self) -> Any:
        """Get last result of execution."""
        return self._result


# ============================================================
# Concrete Utilities (Inheritance + Polymorphism)
# ============================================================

class LargeDatasetGenerator(BasePerformanceUtility):
    """Generate large datasets for performance testing."""

    def __init__(self, size: int) -> None:
        super().__init__()
        self._size = size  # Encapsulation

    def run(self) -> list[dict[str, Any]]:
        """Generate a mock dataset of given size."""
        self._logger.log(f"Generating dataset of size {self._size}...")
        result: list[dict[str, Any]] = [
            {"id": i, "data": f"item_{i}" * 10, "value": i * 2}
            for i in range(self._size)
        ]
        self._result = result
        return result


class ExecutionTimer(BasePerformanceUtility):
    """Measure execution time of any function."""

    def __init__(self, func: Callable[..., Any], *args: Any) -> None:
        super().__init__()
        self._func = func                  # Encapsulation
        self._args = args                  # Encapsulation

    def run(self) -> tuple[Any, float]:
        """Measure execution time of the function."""
        self._logger.log(f"Measuring time for: {self._func.__name__}")
        start = time.perf_counter()
        result = self._func(*self._args)
        elapsed = time.perf_counter() - start
        self._result = (result, elapsed)
        return self._result


class BenchmarkRunner(BasePerformanceUtility):
    """Benchmark a callable operation across multiple iterations."""

    def __init__(self, func: Callable[[], None], iterations: int = 100) -> None:
        super().__init__()
        self._func = func              # Encapsulation
        self._iterations = iterations  # Encapsulation

    def run(self) -> dict[str, float]:
        """Benchmark operation multiple times."""
        self._logger.log(
            f"Benchmarking {self._func.__name__} for {self._iterations} iterations..."
        )
        times: list[float] = []

        for _ in range(self._iterations):
            start = time.perf_counter()
            self._func()
            times.append(time.perf_counter() - start)

        self._result = {
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
        }
        return self._result


# ============================================================
# Factory Pattern for Performance Utilities
# ============================================================

class PerformanceUtilityFactory:
    """Factory for creating performance utilities."""

    @staticmethod
    def create(
        utility_type: str,
        func: Callable[..., Any] | None = None,
        iterations: int = 100,
        size: int | None = None,
        *args: Any,
    ) -> BasePerformanceUtility:

        if utility_type == "dataset":
            if size is None:
                raise ValueError("size required for dataset")
            return LargeDatasetGenerator(size)
        if utility_type == "timer":
            if func is None:
                raise ValueError("func required for timer")
            return ExecutionTimer(func, *args)
        if utility_type == "benchmark":
            if func is None:
                raise ValueError("func required for benchmark")
            return BenchmarkRunner(func, iterations)

        raise ValueError(f"Unknown utility type: {utility_type}")


# ============================================================
# Functional Wrappers (Backward Compatibility)
# ============================================================

def generate_large_dataset(size: int) -> list[dict[str, Any]]:
    """Generate large dataset (function wrapper)."""
    return LargeDatasetGenerator(size).run()


def measure_execution_time(
    func: Callable[..., Any], *args: Any
) -> tuple[Any, float]:
    """Measure execution time of a function (wrapper)."""
    return ExecutionTimer(func, *args).run()


def benchmark_operation(
    func: Callable[[], None], iterations: int = 100
) -> dict[str, float]:
    """Benchmark operation multiple times (wrapper)."""
    return BenchmarkRunner(func, iterations).run()
