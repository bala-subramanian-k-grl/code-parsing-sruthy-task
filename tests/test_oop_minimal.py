# USB PD Specification Parser - OOP Minimal Tests
"""Minimal OOP tests with all 4 principles."""

from abc import ABC, abstractmethod


class BaseTest(ABC):  # Abstraction
    """Abstract test base (Abstraction, Encapsulation)."""

    def __init__(self, name: str):
        self._name = name  # Encapsulation

    @property  # Encapsulation: controlled access
    def name(self) -> str:
        """Get test name."""
        return self._name

    @abstractmethod  # Abstraction
    def run(self) -> bool:
        pass


class ConfigTest(BaseTest):  # Inheritance
    """Config test (Inheritance, Polymorphism)."""

    def run(self) -> bool:  # Polymorphism
        from src.config import Config

        config = Config("application.yml")
        pdf_file = config.pdf_input_file
        return len(str(pdf_file)) > 0


class ModelTest(BaseTest):  # Inheritance
    """Model test (Inheritance, Polymorphism)."""

    def run(self) -> bool:  # Polymorphism
        from src.core.models import BaseContent

        content = BaseContent(page=1, content="test")
        return content.page == 1


class OOPTestRunner:  # Encapsulation
    """Test runner (All 4 OOP principles)."""

    def __init__(self):
        self._tests: list[BaseTest] = []  # Encapsulation

    def add(self, test: BaseTest) -> None:  # Polymorphism
        self._tests.append(test)

    def run_all(self) -> dict[str, bool]:  # Abstraction
        results: dict[str, bool] = {test.name: test.run() for test in self._tests}
        return results


def test_oop_principles():
    """Test all 4 OOP principles in minimal code."""
    runner = OOPTestRunner()
    runner.add(ConfigTest("config"))  # Factory pattern
    runner.add(ModelTest("model"))

    results = runner.run_all()
    assert all(results.values())
