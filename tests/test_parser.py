# USB PD Specification Parser - Parser Tests
"""Minimal parser tests with OOP principles."""

from abc import ABC, abstractmethod

from src.config import Config


class BasePipelineTest(ABC):  # Abstraction
    def __init__(self):
        self._config = Config("application.yml")  # Encapsulation

    @abstractmethod  # Abstraction
    def test_pipeline(self) -> bool:
        pass


class MockPipelineTest(BasePipelineTest):  # Inheritance
    def test_pipeline(self) -> bool:  # Polymorphism
        from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

        try:
            orchestrator = PipelineOrchestrator("application.yml")
            return hasattr(orchestrator, "_config")
        except (ValueError, OSError, RuntimeError) as e:
            print(f"Test failed: {e}")
            return False


class ConfigPipelineTest(BasePipelineTest):  # Inheritance
    def test_pipeline(self) -> bool:  # Polymorphism
        pdf_file = self._config.pdf_input_file
        return len(str(pdf_file)) > 0


class PipelineTestRunner:  # Encapsulation
    def __init__(self):
        self._tests: list[BasePipelineTest] = []  # Encapsulation

    def add_test(self, test: BasePipelineTest) -> None:  # Polymorphism
        self._tests.append(test)

    def run_all(self) -> bool:  # Abstraction
        results: list[bool] = [t.test_pipeline() for t in self._tests]
        return all(results)


def test_pipeline():
    runner = PipelineTestRunner()
    runner.add_test(MockPipelineTest())
    runner.add_test(ConfigPipelineTest())
    assert runner.run_all()
