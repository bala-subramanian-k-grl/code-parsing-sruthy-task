# USB PD Specification Parser - Minimal Tests
"""Minimal tests with all 4 OOP principles."""

from abc import ABC, abstractmethod


class BaseTest(ABC):  # Abstraction
    def __init__(self, name: str):
        self._name = name  # Encapsulation

    @abstractmethod  # Abstraction
    def execute(self) -> bool:
        pass


class ConfigTest(BaseTest):  # Inheritance
    def execute(self) -> bool:  # Polymorphism
        from src.config import Config

        pdf_file = Config("application.yml").pdf_input_file
        return len(str(pdf_file)) > 0


class ModelTest(BaseTest):  # Inheritance
    def execute(self) -> bool:  # Polymorphism
        from src.core.models import BaseContent

        return BaseContent(page=1, content="test").page == 1


class MinimalTestSuite:  # Encapsulation
    def __init__(self):
        self._tests: list[BaseTest] = []  # Encapsulation

    def add(self, test: BaseTest) -> None:  # Polymorphism
        self._tests.append(test)

    def run(self) -> bool:  # Abstraction
        results: list[bool] = [t.execute() for t in self._tests]
        return all(results)


def test_all():
    suite = MinimalTestSuite()
    suite.add(ConfigTest("config"))
    suite.add(ModelTest("model"))
    assert suite.run()
