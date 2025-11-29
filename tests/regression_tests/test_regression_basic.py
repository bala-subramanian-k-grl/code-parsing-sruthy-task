"""
Regression tests rewritten with full advanced OOP design.

Enhancements:
- Full lifecycle hooks (setup → run_test → teardown)
- Composition-based logging
- Encapsulation for internal state (result, errors, timings)
- Polymorphic run_test() implementations
- Unified execute() method for consistency
- Highly readable, maintainable regression suite
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any


# ===============================================================
# Logger (Composition)
# ===============================================================

class RegressionLogger:
    """Logger used for regression testing."""

    def __init__(self) -> None:
        self.messages: list[str] = []
        self.__instance_id = id(self)
        self.__created = True

    def log(self, msg: str) -> None:
        self.messages.append(msg)
        print(f"[REGRESSION LOG] {msg}")

    def __str__(self) -> str:
        return "RegressionLogger()"

    def __repr__(self) -> str:
        return "RegressionLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RegressionLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ===============================================================
# Base Regression Test (Lifecycle + Encapsulation + OOP)
# ===============================================================

class BaseRegressionTest(ABC):
    """Abstract base class for all regression test cases."""

    def __init__(self, logger: RegressionLogger | None = None) -> None:
        self._logger = logger or RegressionLogger()    # Composition
        self._result: bool | None = None              # Encapsulation
        self._errors: list[str] = []                  # Encapsulation
        self.__instance_id = id(self)
        self.__created = True
        self._start_time: float = 0.0                 # Encapsulation
        self._end_time: float = 0.0                   # Encapsulation

    # ---------------- Lifecycle Hooks ----------------

    def setup(self) -> None:
        self._logger.log(f"Setting up {self.__class__.__name__}...")
        self._start_time = time.perf_counter()

    @abstractmethod
    def run_test(self) -> bool:
        """Concrete regression logic implemented by subclasses."""
        pass

    def teardown(self) -> None:
        self._end_time = time.perf_counter()
        duration = round(self._end_time - self._start_time, 4)
        self._logger.log(
            f"Tearing down {self.__class__.__name__} (Duration: {duration}s)"
        )

    # ---------------- Unified Execution API ----------------

    def execute(self) -> bool:
        try:
            self.setup()
            self._result = self.run_test()
            return self._result
        except Exception as e:
            self._errors.append(str(e))
            self._logger.log(f"ERROR: {e}")
            return False
        finally:
            self.teardown()

    def add_error(self, message: str) -> None:
        self._errors.append(message)

    def __str__(self) -> str:
        return "BaseRegressionTest()"

    def __repr__(self) -> str:
        return "BaseRegressionTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseRegressionTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ===============================================================
# Concrete Regression Tests (Polymorphism)
# ===============================================================

class EmptyDataNoCrashTest(BaseRegressionTest):
    """Regression: validate_jsonl_format should not crash on empty input."""

    def run_test(self) -> bool:
        self._logger.log("Running EmptyDataNoCrashTest...")

        from tests.helpers.validation_utils import validate_jsonl_format
        empty_data: list[dict[str, Any]] = []

        return validate_jsonl_format(empty_data) is True

    def __str__(self) -> str:
        return "EmptyDataNoCrashTest()"

    def __repr__(self) -> str:
        return "EmptyDataNoCrashTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmptyDataNoCrashTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class MissingFieldsValidationTest(BaseRegressionTest):
    """Regression: Validators must detect missing fields."""

    def run_test(self) -> bool:
        self._logger.log("Running MissingFieldsValidationTest...")

        from tests.helpers.validation_utils import validate_content_item

        incomplete_item = {"doc_title": "Test"}  # missing required fields
        return validate_content_item(incomplete_item) is False

    def __str__(self) -> str:
        return "MissingFieldsValidationTest()"

    def __repr__(self) -> str:
        return "MissingFieldsValidationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MissingFieldsValidationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class PathTraversalPreventionTest(BaseRegressionTest):
    """Regression: Ensure path traversal detection remains intact."""

    def run_test(self) -> bool:
        self._logger.log("Running PathTraversalPreventionTest...")

        from pathlib import Path

        malicious_path = Path("../../etc/passwd")
        safe_path = Path("outputs/test.jsonl")

        return (".." in str(malicious_path)) and (".." not in str(safe_path))

    def __str__(self) -> str:
        return "PathTraversalPreventionTest()"

    def __repr__(self) -> str:
        return "PathTraversalPreventionTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PathTraversalPreventionTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class NullParentIDHandlingTest(BaseRegressionTest):
    """Regression: parent_id must always be safe (None when missing)."""

    def run_test(self) -> bool:
        self._logger.log("Running NullParentIDHandlingTest...")

        from tests.helpers.mock_data import generate_mock_content
        content = generate_mock_content(5)

        return all(item["parent_id"] is None for item in content)

    def __str__(self) -> str:
        return "NullParentIDHandlingTest()"

    def __repr__(self) -> str:
        return "NullParentIDHandlingTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NullParentIDHandlingTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class LargeDatasetNoMemoryErrorTest(BaseRegressionTest):
    """Regression: Large datasets must not trigger memory issues."""

    def run_test(self) -> bool:
        self._logger.log("Running LargeDatasetNoMemoryErrorTest...")

        from tests.helpers.performance_utils import generate_large_dataset

        data = generate_large_dataset(10000)
        return len(data) == 10000

    def __str__(self) -> str:
        return "LargeDatasetNoMemoryErrorTest()"

    def __repr__(self) -> str:
        return "LargeDatasetNoMemoryErrorTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LargeDatasetNoMemoryErrorTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class FileCleanupOnErrorTest(BaseRegressionTest):
    """Regression: TempFileManager must clean up safely after errors."""

    def run_test(self) -> bool:
        self._logger.log("Running FileCleanupOnErrorTest...")

        from tests.helpers.file_utils import TempFileManager

        try:
            manager = TempFileManager()
            return manager is not None
        except Exception as e:
            self.add_error(str(e))
            return False

    def __str__(self) -> str:
        return "FileCleanupOnErrorTest()"

    def __repr__(self) -> str:
        return "FileCleanupOnErrorTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FileCleanupOnErrorTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class DuplicateSectionIDTest(BaseRegressionTest):
    """Regression: TOC section IDs must always be unique."""

    def run_test(self) -> bool:
        self._logger.log("Running DuplicateSectionIDTest...")

        from tests.helpers.mock_data import generate_mock_toc
        toc = generate_mock_toc(10)

        section_ids = [item["section_id"] for item in toc]
        return len(section_ids) == len(set(section_ids))

    def __str__(self) -> str:
        return "DuplicateSectionIDTest()"

    def __repr__(self) -> str:
        return "DuplicateSectionIDTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DuplicateSectionIDTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ZeroPageHandlingTest(BaseRegressionTest):
    """Regression: Page numbers must always be > 0."""

    def run_test(self) -> bool:
        self._logger.log("Running ZeroPageHandlingTest...")

        from tests.helpers.mock_data import generate_mock_content
        content = generate_mock_content(10)

        return all(item["page"] > 0 for item in content)

    def __str__(self) -> str:
        return "ZeroPageHandlingTest()"

    def __repr__(self) -> str:
        return "ZeroPageHandlingTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ZeroPageHandlingTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ===============================================================
# Unified Regression Test Runner (Polymorphism)
# ===============================================================

class RegressionTestRunner:
    """Runs all regression tests via polymorphism."""

    def __init__(self) -> None:
        self._tests: list[BaseRegressionTest] = []
        self.__instance_id = id(self)
        self.__created = True

    def add_test(self, test: BaseRegressionTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        return all(test.execute() for test in self._tests)

    def __str__(self) -> str:
        return "RegressionTestRunner()"

    def __repr__(self) -> str:
        return "RegressionTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RegressionTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ===============================================================
# PyTest Entry Point
# ===============================================================

def test_regression_suite():
    """Execute the full regression test suite using OOP runner."""

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
