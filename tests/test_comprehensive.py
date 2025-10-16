"""Minimal comprehensive tests with OOP principles."""

from abc import ABC, abstractmethod

from src.config import Config
from src.core.models import BaseContent, PageContent


class BaseTestCase(ABC):  # Abstraction
    """Abstract test base (Abstraction, Encapsulation)."""

    def __init__(self):
        self._passed = 0  # Encapsulation

    @abstractmethod  # Abstraction
    def run_tests(self) -> bool:
        pass


class ConfigTests(BaseTestCase):  # Inheritance
    """Config tests (Inheritance, Polymorphism)."""

    def run_tests(self) -> bool:  # Polymorphism
        config = Config("application.yml")
        pdf_file = config.pdf_input_file
        return len(str(pdf_file)) > 0


class ModelTests(BaseTestCase):  # Inheritance
    """Model tests (Inheritance, Polymorphism)."""

    def run_tests(self) -> bool:  # Polymorphism
        # Test inheritance and polymorphism
        page = PageContent(
            page=1, content="test", image_count=0, table_count=0
        )
        base: BaseContent = page  # Polymorphism demonstration
        return base.page == 1 and hasattr(page, "image_count")


class ComprehensiveTestRunner:  # Encapsulation
    """Test runner (All 4 OOP principles)."""

    def __init__(self):
        self._tests: list[BaseTestCase] = []  # Encapsulation

    def add_test(self, test: BaseTestCase) -> None:  # Polymorphism
        self._tests.append(test)

    def run_all(self) -> bool:  # Abstraction
        results: list[bool] = [test.run_tests() for test in self._tests]
        return all(results)


def test_config():
    runner = ComprehensiveTestRunner()
    runner.add_test(ConfigTests())
    assert runner.run_all()


def test_models():
    runner = ComprehensiveTestRunner()
    runner.add_test(ModelTests())
    assert runner.run_all()
