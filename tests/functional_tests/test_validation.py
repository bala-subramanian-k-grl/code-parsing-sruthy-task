"""
XLS validation tests with full OOP design.

Enhancements:
- BaseValidationTest with lifecycle hooks (setup/run_test/teardown)
- Composition-based logging
- Encapsulation of internal result & errors
- Polymorphic run_test() implementations
- Unified ValidationTestRunner with reporting
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

# ============================================================
# Logger (Composition)
# ============================================================


class ValidationLogger:
    """Simple logger injected via composition."""

    def log(self, message: str) -> None:
        print(f"[VALIDATION LOG] {message}")

    def __str__(self) -> str:
        return "ValidationLogger()"

    def __repr__(self) -> str:
        return "ValidationLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidationLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Base Abstract Validation Test (Abstraction + Encapsulation)
# ============================================================

class BaseValidationTest(ABC):
    """Base class for XLS/content validation tests with full lifecycle."""

    def __init__(self) -> None:
        self._logger = ValidationLogger()      # Composition
        self._errors: list[str] = []           # Encapsulation
        self._result: bool | None = None       # Encapsulation
        self._start_time: float = 0.0
        self._end_time: float = 0.0
        self.__instance_id = id(self)
        self.__created = True

    # ---------------- Lifecycle Hooks ----------------

    def setup(self) -> None:
        self._logger.log(f"Setting up {self.__class__.__name__}")
        self._start_time = time.time()

    @abstractmethod
    def run_test(self) -> bool:
        """Child classes implement actual validation logic."""
        pass

    def teardown(self) -> None:
        self._end_time = time.time()
        duration = round(self._end_time - self._start_time, 4)
        self._logger.log(
            f"Tearing down {self.__class__.__name__} (Duration: {duration}s)"
        )

    # ---------------- Main Execution Wrapper ----------------

    def run(self) -> bool:
        try:
            self.setup()
            self._result = self.run_test()
        except Exception as e:
            self._errors.append(str(e))
            self._logger.log(f"ERROR in {self.__class__.__name__}: {e}")
            self._result = False
        finally:
            self.teardown()

        return bool(self._result)

    def add_error(self, msg: str) -> None:
        """Store internal error message."""
        self._errors.append(msg)

    def __str__(self) -> str:
        return "BaseValidationTest()"

    def __repr__(self) -> str:
        return "BaseValidationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseValidationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Concrete Validation Tests (Inheritance + Polymorphism)
# ============================================================

class ValidationStructureTest(BaseValidationTest):
    """Check structure of TOC and content validation."""

    def run_test(self) -> bool:
        self._logger.log("Running ValidationStructureTest...")

        from tests.helpers.validation_utils import (validate_content_item,
                                                    validate_toc_entry)

        toc_entry: dict[str, Any] = {
            "section_id": "s1",
            "title": "Test",
            "page": 1,
            "level": 1,
        }
        content_item: dict[str, Any] = {
            "doc_title": "Test",
            "section_id": "p1_0",
            "title": "Content",
            "page": 1,
            "level": 1,
            "full_path": "Content",
        }

        return (
            validate_toc_entry(toc_entry)
            and validate_content_item(content_item)
        )

    def __str__(self) -> str:
        return "ValidationStructureTest()"

    def __repr__(self) -> str:
        return "ValidationStructureTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidationStructureTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ValidationErrorCountTest(BaseValidationTest):
    """Verify that validation error counting works."""

    def run_test(self) -> bool:
        self._logger.log("Running ValidationErrorCountTest...")

        from tests.helpers.validation_utils import count_validation_errors

        data: list[dict[str, Any]] = [
            {"valid": True},
            {"invalid": False},
        ]

        def validator(item: dict[str, Any]) -> bool:
            return "valid" in item

        errors = count_validation_errors(data, validator)
        return errors == 1

    def __str__(self) -> str:
        return "ValidationErrorCountTest()"

    def __repr__(self) -> str:
        return "ValidationErrorCountTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidationErrorCountTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ExcelGenerationTest(BaseValidationTest):
    """Verify that the Excel validation generator initializes properly."""

    def run_test(self) -> bool:
        self._logger.log("Running ExcelGenerationTest...")

        from src.support.excel_report_generator import ExcelReportGenerator

        try:
            generator = ExcelReportGenerator()
            return generator is not None
        except Exception as exc:
            self.add_error(str(exc))
            return False

    def __str__(self) -> str:
        return "ExcelGenerationTest()"

    def __repr__(self) -> str:
        return "ExcelGenerationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExcelGenerationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Unified Runner for All Validation Tests
# ============================================================

class ValidationTestRunner:
    """Runs validation tests using polymorphism with reporting."""

    def __init__(self) -> None:
        self._tests: list[BaseValidationTest] = []
        self.__instance_id = id(self)
        self.__created = True

    def add_test(self, test: BaseValidationTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        results: list[bool] = []
        for test in self._tests:
            result = test.run()
            status = "PASSED" if result else "FAILED"
            print(f"[RESULT] {test.__class__.__name__}: {status}")
            results.append(result)
        return all(results)

    def __str__(self) -> str:
        return "ValidationTestRunner()"

    def __repr__(self) -> str:
        return "ValidationTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidationTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Pytest Entry Point
# ============================================================

def test_validation_suite():
    """Run all XLS/content validation tests in OOP runner form."""

    runner = ValidationTestRunner()

    runner.add_test(ValidationStructureTest())
    runner.add_test(ValidationErrorCountTest())
    runner.add_test(ExcelGenerationTest())

    assert runner.run_all()
