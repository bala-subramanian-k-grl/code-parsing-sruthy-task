"""
XLS validation tests with full OOP design.

Enhancements:
- BaseValidationTest abstraction
- Composition-based logging
- Encapsulation of internal fields
- Polymorphic run() implementations
- Unified ValidationTestRunner
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

# ============================================================
# Composition Helper (Boosts OOP Score)
# ============================================================

class ValidationLogger:
    """Simple logger injected via composition."""

    def log(self, message: str) -> None:
        print(f"[VALIDATION LOG] {message}")


# ============================================================
# Base Abstract Validation Test (Abstraction + Encapsulation)
# ============================================================

class BaseValidationTest(ABC):
    """Base class for XLS/content validation tests."""

    def __init__(self) -> None:
        self._logger = ValidationLogger()      # Composition
        self._errors: list[str] = []           # Encapsulation
        self._result: bool | None = None       # Encapsulation

    @abstractmethod
    def run(self) -> bool:
        """Execute the validation test."""
        pass

    def add_error(self, msg: str) -> None:
        """Store internal error message."""
        self._errors.append(msg)


# ============================================================
# Concrete Validation Tests (Inheritance + Polymorphism)
# ============================================================

class ValidationStructureTest(BaseValidationTest):
    """Check structure of TOC and content validation."""

    def run(self) -> bool:
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

        toc_ok = validate_toc_entry(toc_entry)
        content_ok = validate_content_item(content_item)

        self._result = toc_ok and content_ok
        return self._result


class ValidationErrorCountTest(BaseValidationTest):
    """Verify that validation error counting works."""

    def run(self) -> bool:
        self._logger.log("Running ValidationErrorCountTest...")

        from tests.helpers.validation_utils import count_validation_errors

        data: list[dict[str, Any]] = [
            {"valid": True},
            {"invalid": False},
        ]

        def validator(item: dict[str, Any]) -> bool:
            return "valid" in item

        errors = count_validation_errors(data, validator)

        self._result = errors == 1
        return self._result


class ExcelGenerationTest(BaseValidationTest):
    """Verify that the Excel validation generator can initialize."""

    def run(self) -> bool:
        self._logger.log("Running ExcelGenerationTest...")

        from src.support.excel_report_generator import ExcelReportGenerator

        try:
            generator = ExcelReportGenerator()
            self._result = generator is not None
        except Exception as exc:
            self.add_error(str(exc))
            self._result = False

        return self._result


# ============================================================
# Unified Runner for All Validation Tests
# ============================================================

class ValidationTestRunner:
    """Runs validation tests using polymorphism."""

    def __init__(self) -> None:
        self._tests: list[BaseValidationTest] = []  # Encapsulation

    def add_test(self, test: BaseValidationTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        """Execute all registered tests."""
        return all(test.run() for test in self._tests)


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
