# USB PD Specification Parser - Extractor Tests
"""Minimal extractor tests with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractorTest(ABC):  # Abstraction
    def __init__(self):
        self._result: Any = None  # Encapsulation

    @abstractmethod  # Abstraction
    def run_test(self) -> bool:
        pass


class MockExtractorTest(BaseExtractorTest):  # Inheritance
    def run_test(self) -> bool:  # Polymorphism
        from src.utils.base import BaseExtractor

        class MockExtractor(BaseExtractor):
            def extract(self, file_path: Path) -> list[dict[str, Any]]:
                return [{"mock": "data"}]

        try:
            test_file = Path("test.pdf")
            test_file.touch()
            config = {"test": "config"}
            extractor = MockExtractor(config)
            self._result = extractor.extract(test_file)
            test_file.unlink()
            return len(self._result) > 0
        except (OSError, ValueError, RuntimeError):
            return False


class ExtractorTestSuite:  # Encapsulation
    def __init__(self):
        self._tests: list[BaseExtractorTest] = []  # Encapsulation

    def add_test(self, test: BaseExtractorTest) -> None:  # Polymorphism
        self._tests.append(test)

    def run_all(self) -> bool:  # Abstraction
        results: list[bool] = [t.run_test() for t in self._tests]
        return all(results)


def test_extractor():
    suite = ExtractorTestSuite()
    suite.add_test(MockExtractorTest())
    assert suite.run_all()
