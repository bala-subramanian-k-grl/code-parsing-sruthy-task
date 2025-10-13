
# USB PD Specification Parser - Performance Benchmarking
"""Minimal benchmark with OOP principles."""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any


class BaseBenchmark(ABC):  # Abstraction
    def __init__(self, name: str) -> None:
        self._name = name  # Encapsulation
        self._logger = logging.getLogger(__name__)  # Encapsulation

    @abstractmethod  # Abstraction
    def run(self) -> dict[str, Any]:
        pass


class ConfigBenchmark(BaseBenchmark):  # Inheritance
    def run(self) -> dict[str, Any]:  # Polymorphism
        from src.config import Config

        config = Config("application.yml")  # Create once, reuse
        start = time.perf_counter()
        for _ in range(100):
            _ = config.pdf_input_file
        elapsed = time.perf_counter() - start
        return {"name": self._name, "time": elapsed, "ops": 100}


class ModelBenchmark(BaseBenchmark):  # Inheritance
    def run(self) -> dict[str, Any]:  # Polymorphism
        start = time.perf_counter()
        from src.core.models import BaseContent

        for i in range(200):
            BaseContent(page=i + 1, content=f"test {i}")
        elapsed = time.perf_counter() - start
        return {"name": self._name, "time": elapsed, "ops": 200}


class BenchmarkRunner:  # Encapsulation
    def __init__(self) -> None:
        self._benchmarks: list[BaseBenchmark] = []  # Encapsulation

    def add(self, benchmark: BaseBenchmark) -> None:  # Polymorphism
        self._benchmarks.append(benchmark)

    def run_all(self) -> None:  # Abstraction
        for benchmark in self._benchmarks:
            result = benchmark.run()  # Polymorphism
            print(f"{result['name']}: {result['time']:.3f}s ({result['ops']} ops)")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    runner = BenchmarkRunner()
    runner.add(ConfigBenchmark("Config"))
    runner.add(ModelBenchmark("Model"))
    runner.run_all()


if __name__ == "__main__":
    main()
