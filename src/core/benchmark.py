# USB PD Specification Parser - Performance Benchmarking
"""Minimal benchmarks with OOP principles."""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any


class BaseBenchmark(ABC):  # Abstraction
    def __init__(self, name: str) -> None:
        """Initialize benchmark with name."""
        self.__name = name  # Private

    @property
    def _name(self) -> str:  # Protected property for subclasses
        """Get benchmark name for subclasses."""
        return self.__name

    @abstractmethod  # Abstraction
    def run(self) -> dict[str, Any]:
        pass


class ConfigBenchmark(BaseBenchmark):  # Inheritance
    def run(self) -> dict[str, Any]:  # Polymorphism
        """Run config benchmark."""
        from src.config import Config

        config = Config("application.yml")  # Create once, reuse
        start = time.perf_counter()
        for _ in range(100):
            _ = config.pdf_input_file
        elapsed = time.perf_counter() - start
        return {"name": self._name, "time": elapsed, "ops": 100}


class ModelBenchmark(BaseBenchmark):  # Inheritance
    def run(self) -> dict[str, Any]:  # Polymorphism
        """Run model benchmark."""
        start = time.perf_counter()
        from src.core.models import BaseContent

        for i in range(200):
            BaseContent(page=i + 1, content=f"test {i}")
        elapsed = time.perf_counter() - start
        return {"name": self._name, "time": elapsed, "ops": 200}


class BenchmarkRunner:  # Encapsulation
    def __init__(self) -> None:
        """Initialize benchmark runner."""
        self.__benchmarks: list[BaseBenchmark] = []  # Private

    def add(self, benchmark: BaseBenchmark) -> None:  # Polymorphism
        """Add benchmark to runner."""
        self.__benchmarks.append(benchmark)

    def run_all(self) -> None:  # Abstraction
        """Run all benchmarks."""
        for benchmark in self.__benchmarks:
            result = benchmark.run()  # Polymorphism
            name = result["name"]
            time_val = result["time"]
            ops = result["ops"]
            msg = f"{name}: {time_val:.3f}s ({ops} ops)"
            print(msg)


def main() -> None:
    """Main benchmark entry point."""
    logging.basicConfig(level=logging.INFO)
    runner = BenchmarkRunner()
    runner.add(ConfigBenchmark("Config"))
    runner.add(ModelBenchmark("Model"))
    runner.run_all()


if __name__ == "__main__":
    main()
