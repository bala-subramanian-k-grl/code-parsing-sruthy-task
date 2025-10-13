# USB PD Specification Parser - Edge Case Tests
"""Minimal edge case tests with OOP principles."""

from abc import ABC, abstractmethod

from src.config import Config


class BaseEdgeTest(ABC):  # Abstraction
    def __init__(self):
        self._errors: list[str] = []  # Encapsulation

    @abstractmethod  # Abstraction
    def test_edge_case(self) -> bool:
        pass


class ConfigEdgeTest(BaseEdgeTest):  # Inheritance
    def test_edge_case(self) -> bool:  # Polymorphism
        try:
            config = Config("nonexistent.yml")
            pdf_file = config.pdf_input_file
            return len(str(pdf_file)) > 0
        except (FileNotFoundError, ValueError) as e:
            self._errors.append(str(e))
            return False


class ModelEdgeTest(BaseEdgeTest):  # Inheritance
    def test_edge_case(self) -> bool:  # Polymorphism
        from src.core.models import BaseContent

        try:
            BaseContent(page=1, content="test")
            return True
        except ValueError as e:
            self._errors.append(str(e))
            return False


class EdgeTestRunner:  # Encapsulation
    def __init__(self):
        self._tests: list[BaseEdgeTest] = []  # Encapsulation

    def add(self, test: BaseEdgeTest) -> None:  # Polymorphism
        self._tests.append(test)

    def run_all(self) -> bool:  # Abstraction
        results: list[bool] = []
        for test in self._tests:
            try:
                results.append(test.test_edge_case())
            except (ValueError, OSError, RuntimeError, AttributeError) as e:
                print(f"Test {test.__class__.__name__} failed: {e}")
                results.append(False)
        return all(results)


def test_config_edge():
    runner = EdgeTestRunner()
    runner.add(ConfigEdgeTest())
    assert runner.run_all()


def test_model_edge():
    runner = EdgeTestRunner()
    runner.add(ModelEdgeTest())
    assert runner.run_all()
