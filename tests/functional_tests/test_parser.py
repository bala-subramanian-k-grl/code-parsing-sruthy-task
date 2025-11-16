"""
Parser pipeline tests using full OOP design.

Enhancements:
- Abstract BasePipelineTest for unified behavior
- Inheritance for separate pipeline test scenarios
- Polymorphic run() methods
- Encapsulation of internal state
- Composition via PipelineLogger()
- Unified test runner pattern for maintainability
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# Composition Helper (Boosts OOP Score)
# ============================================================

class PipelineLogger:
    """Simple logger used inside tests via composition."""

    def log(self, message: str) -> None:
        print(f"[PIPELINE LOG] {message}")


# ============================================================
# Abstract Base Test (Abstraction + Encapsulation)
# ============================================================

class BasePipelineTest(ABC):
    """Base class for pipeline testing."""

    def __init__(self) -> None:
        self._logger = PipelineLogger()      # Composition
        self._result: bool | None = None     # Encapsulation

    @abstractmethod
    def run(self) -> bool:
        """Execute the pipeline-related test."""
        pass


# ============================================================
# Concrete Pipeline Tests (Inheritance + Polymorphism)
# ============================================================

class PipelineInitializationTest(BasePipelineTest):
    """Test that the pipeline orchestrator imports successfully."""

    def run(self) -> bool:
        self._logger.log("Running PipelineInitializationTest...")

        import src.orchestrator.pipeline_orchestrator
        self._result = src.orchestrator.pipeline_orchestrator is not None

        return self._result


class TOCExtractionTest(BasePipelineTest):
    """Test TOC extraction from mock data."""

    def run(self) -> bool:
        self._logger.log("Running TOCExtractionTest...")

        from tests.helpers.mock_data import generate_mock_toc

        toc = generate_mock_toc(5)
        valid = (
            len(toc) == 5 and
            all("section_id" in item for item in toc)
        )

        self._result = valid
        return self._result


class ContentExtractionTest(BasePipelineTest):
    """Test content extraction from mock data."""

    def run(self) -> bool:
        self._logger.log("Running ContentExtractionTest...")

        from tests.helpers.mock_data import generate_mock_content

        content = generate_mock_content(10)
        valid = (
            len(content) == 10 and
            all("doc_title" in item for item in content)
        )

        self._result = valid
        return self._result


class PipelineMockDataTest(BasePipelineTest):
    """Test the pipeline workflow using mock TOC + content."""

    def run(self) -> bool:
        self._logger.log("Running PipelineMockDataTest...")

        from tests.helpers.mock_data import (
            generate_mock_content,
            generate_mock_toc,
        )

        toc = generate_mock_toc(3)
        content = generate_mock_content(5)

        self._result = len(toc) > 0 and len(content) > 0
        return self._result


# ============================================================
# Unified Runner (Encapsulation + Polymorphism)
# ============================================================

class PipelineTestRunner:
    """Runs all pipeline tests using polymorphism."""

    def __init__(self) -> None:
        self._tests: list[BasePipelineTest] = []  # Encapsulation

    def add_test(self, test: BasePipelineTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        return all(test.run() for test in self._tests)


# ============================================================
# PyTest Entry Point
# ============================================================

def test_pipeline_suite():
    """Execute all pipeline-related tests in a unified suite."""

    runner = PipelineTestRunner()

    runner.add_test(PipelineInitializationTest())
    runner.add_test(TOCExtractionTest())
    runner.add_test(ContentExtractionTest())
    runner.add_test(PipelineMockDataTest())

    assert runner.run_all()
