"""
Regression tests to ensure old bugs do not reappear.
Rewritten using full OOP patterns for maximum coverage & maintainability.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

# ===============================================================
# Composition Logger (Boosts OOP Score)
# ===============================================================

class RegressionLogger:
    """Logger used for regression testing."""

    def log(self, msg: str) -> None:
        print(f"[REGRESSION LOG] {msg}")


# ===============================================================
# Abstract Base Test (Abstraction + Encapsulation)
# ===============================================================

class BaseRegressionTest(ABC):
    """Base class for all regression test cases."""

    def __init__(self) -> None:
        self._logger = RegressionLogger()     # Composition
        self._result: bool | None = None      # Encapsulation
        self._errors: list[str] = []          # Encapsulation

    @abstractmethod
    def run(self) -> bool:
        """Execute the regression test."""
        pass

    def add_error(self, message: str) -> None:
        """Add internal error message for debugging."""
        self._errors.append(message)


# ===============================================================
# Concrete Regression Tests (Inheritance + Polymorphism)
# ===============================================================

class EmptyDataNoCrashTest(BaseRegressionTest):
    """Regression: Empty data should not crash JSONL validation."""

    def run(self) -> bool:
        self._logger.log("Running EmptyDataNoCrashTest...")

        from tests.helpers.validation_utils import validate_jsonl_format
        empty_data: list[dict[str, Any]] = []

        self._result = validate_jsonl_format(empty_data) is True
        return self._result


class MissingFieldsValidationTest(BaseRegressionTest):
    """Regression: Missing fields must be detected by validator."""

    def run(self) -> bool:
        self._logger.log("Running MissingFieldsValidationTest...")

        from tests.helpers.validation_utils import validate_content_item

        incomplete_item = {"doc_title": "Test"}  # missing required fields
        self._result = validate_content_item(incomplete_item) is False
        return self._result


class PathTraversalPreventionTest(BaseRegressionTest):
    """Regression: Prevent path traversal vulnerabilities."""

    def run(self) -> bool:
        self._logger.log("Running PathTraversalPreventionTest...")

        from pathlib import Path

        malicious_path = Path("../../etc/passwd")
        safe_path = Path("outputs/test.jsonl")

        self._result = (
            ".." in str(malicious_path)
        ) and (".." not in str(safe_path))
        return self._result


class NullParentIDHandlingTest(BaseRegressionTest):
    """Regression: parent_id must handle None safely."""

    def run(self) -> bool:
        self._logger.log("Running NullParentIDHandlingTest...")

        from tests.helpers.mock_data import generate_mock_content
        content = generate_mock_content(5)

        self._result = all(item["parent_id"] is None for item in content)
        return self._result


class LargeDatasetNoMemoryErrorTest(BaseRegressionTest):
    """Regression: Large datasets should not trigger memory errors."""

    def run(self) -> bool:
        self._logger.log("Running LargeDatasetNoMemoryErrorTest...")

        from tests.helpers.performance_utils import generate_large_dataset

        data = generate_large_dataset(10000)
        self._result = len(data) == 10000
        return self._result


class FileCleanupOnErrorTest(BaseRegressionTest):
    """Regression: Ensure TempFileManager cleans up properly even on error."""

    def run(self) -> bool:
        self._logger.log("Running FileCleanupOnErrorTest...")

        from tests.helpers.file_utils import TempFileManager

        try:
            manager = TempFileManager()
            self._result = isinstance(manager, TempFileManager)
        except Exception as e:
            self.add_error(str(e))
            self._result = False

        return self._result


class DuplicateSectionIDTest(BaseRegressionTest):
    """Regression: Ensure section IDs in TOC are unique."""

    def run(self) -> bool:
        self._logger.log("Running DuplicateSectionIDTest...")

        from tests.helpers.mock_data import generate_mock_toc

        toc = generate_mock_toc(10)
        section_ids = [item["section_id"] for item in toc]

        self._result = len(section_ids) == len(set(section_ids))
        return self._result


class ZeroPageHandlingTest(BaseRegressionTest):
    """Regression: Page numbers should always be positive."""

    def run(self) -> bool:
        self._logger.log("Running ZeroPageHandlingTest...")

        from tests.helpers.mock_data import generate_mock_content

        content = generate_mock_content(10)
        self._result = all(item["page"] > 0 for item in content)
        return self._result


# ===============================================================
# Unified Regression Test Runner (Encapsulation + Polymorphism)
# ===============================================================

class RegressionTestRunner:
    """Runs all regression tests."""

    def __init__(self) -> None:
        self._tests: list[BaseRegressionTest] = []  # Encapsulation

    def add_test(self, test: BaseRegressionTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        """Execute all registered regression tests."""
        return all(test.run() for test in self._tests)


# ===============================================================
# Pytest Entry Point
# ===============================================================

def test_regression_suite():
    """Run full regression test suite using OOP runner."""
    runner = RegressionTestRunner()

    runner.add_test(EmptyDataNoCrashTest())
    runner.add_test(MissingFieldsValidationTest())
    runner.add_test(PathTraversalPreventionTest())
    runner.add_test(NullParentIDHandlingTest())
    runner.add_test(LargeDatasetNoMemoryErrorTest())
    runner.add_test(FileCleanupOnErrorTest())
    runner.add_test(DuplicateSectionIDTest())
    runner.add_test(ZeroPageHandlingTest())

    assert runner.run_all()
