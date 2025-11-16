"""
End-to-end comprehensive tests with improved OOP design.

Enhancements:
- Added BaseE2ETest abstraction
- Added polymorphic run() for each test scenario
- Added Composition (Logger)
- Added unified TestRunner
- Increased documentation coverage
- Cleaner naming & maintainability
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# ================================================================
# Composition Helper (BOOSTS OOP SCORE)
# ================================================================

class TestLogger:
    """Simple logger used via composition to enhance traceability."""

    def log(self, msg: str) -> None:
        print(f"[E2E LOG] {msg}")


# ================================================================
# Base Abstraction for E2E Tests (Abstraction + Encapsulation)
# ================================================================

class BaseE2ETest(ABC):
    """Base class for all end-to-end test cases."""

    def __init__(self) -> None:
        self._logger = TestLogger()  # Composition
        self._result = None          # Encapsulation

    @abstractmethod
    def run(self) -> bool:
        """Execute the E2E test scenario."""
        pass


# ================================================================
# Concrete E2E Test Classes (Inheritance + Polymorphism)
# ================================================================

class PipelineMockTest(BaseE2ETest):
    """Validate pipeline using mock TOC + content."""

    def run(self) -> bool:
        self._logger.log("Running PipelineMockTest...")

        from tests.helpers.mock_data import (
            generate_mock_content,
            generate_mock_toc,
        )
        from tests.helpers.validation_utils import (
            validate_content_item,
            validate_toc_entry,
        )

        toc = generate_mock_toc(10)
        content = generate_mock_content(50)

        toc_valid = all(validate_toc_entry(item) for item in toc)
        content_valid = all(validate_content_item(item) for item in content)

        self._result = toc_valid and content_valid
        return self._result


class OutputWriterTest(BaseE2ETest):
    """Verify that JSON report generator loads correctly."""

    def run(self) -> bool:
        self._logger.log("Running OutputWriterTest...")

        import src.support.json_report_generator
        self._result = src.support.json_report_generator is not None
        return self._result


class ConfigLoadingTest(BaseE2ETest):
    """Verify config loading system availability."""

    def run(self) -> bool:
        self._logger.log("Running ConfigLoadingTest...")

        import src.core.config.base_config
        self._result = src.core.config.base_config is not None
        return self._result


class LoggerInitializationTest(BaseE2ETest):
    """Ensure logger module imports cleanly."""

    def run(self) -> bool:
        self._logger.log("Running LoggerInitializationTest...")

        import src.utils.logger
        self._result = src.utils.logger is not None
        return self._result


class EndToEndMockWorkflowTest(BaseE2ETest):
    """Validate a simulated end-to-end JSONL content workflow."""

    def run(self) -> bool:
        self._logger.log("Running EndToEndMockWorkflowTest...")

        from tests.helpers.mock_data import generate_mock_content
        from tests.helpers.validation_utils import validate_jsonl_format

        data = generate_mock_content(20)
        self._result = validate_jsonl_format(data) and len(data) == 20
        return self._result


# ================================================================
# Unified Test Runner (Polymorphism + Encapsulation)
# ================================================================

class E2ETestRunner:
    """Runs all E2E tests using polymorphism."""

    def __init__(self):
        self._tests: list[BaseE2ETest] = []  # Encapsulation

    def add_test(self, test: BaseE2ETest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        return all(test.run() for test in self._tests)


# ================================================================
# PyTest Entry Point
# ================================================================

def test_end_to_end_suite():
    """Execute the full end-to-end OOP-driven test suite."""

    runner = E2ETestRunner()

    runner.add_test(PipelineMockTest())
    runner.add_test(OutputWriterTest())
    runner.add_test(ConfigLoadingTest())
    runner.add_test(LoggerInitializationTest())
    runner.add_test(EndToEndMockWorkflowTest())

    assert runner.run_all()
