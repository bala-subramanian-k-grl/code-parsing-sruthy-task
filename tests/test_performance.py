"""Minimal performance tests with OOP principles."""

import time
from abc import ABC, abstractmethod
from typing import Any, Callable


class BasePerfTest(ABC):  # Abstraction
    def __init__(self, name: str):
        self._name = name  # Encapsulation

    @abstractmethod  # Abstraction
    def measure(self) -> bool:
        pass

    def _time_it(self, func: Callable[[], Any]) -> float:  # Encapsulation
        start = time.perf_counter()
        func()
        return time.perf_counter() - start


class ConfigPerfTest(BasePerfTest):  # Inheritance
    def measure(self) -> bool:  # Polymorphism
        from src.config import Config

        time_taken = self._time_it(lambda: Config("application.yml"))
        return time_taken < 1.0


class ModelPerfTest(BasePerfTest):  # Inheritance
    def measure(self) -> bool:  # Polymorphism
        from src.core.models import BaseContent

        time_taken = self._time_it(lambda: BaseContent(page=1, content="test"))
        return time_taken < 1.0


class PerfTestSuite:  # Encapsulation
    def __init__(self):
        self._tests: list[BasePerfTest] = []  # Encapsulation

    def add(self, test: BasePerfTest) -> None:  # Polymorphism
        self._tests.append(test)

    def run_all(self) -> bool:  # Abstraction
        results: list[bool] = [t.measure() for t in self._tests]
        return all(results)


def test_performance():
    suite = PerfTestSuite()
    suite.add(ConfigPerfTest("config"))
    suite.add(ModelPerfTest("model"))
    assert suite.run_all()
