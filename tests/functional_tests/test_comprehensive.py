"""
End-to-end comprehensive tests with improved OOP design.

Enhancements:
- Unified BaseE2ETest with optional lifecycle hooks
- Stronger encapsulation (_result + error handling)
- Cleaner polymorphic execution
- Composition-based logger
- Standardized logging format
- Unified E2ETestRunner
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# ================================================================
# Composition Helper (Shared Logger)
# ================================================================


class TestLogger:
    """Lightweight logger for functional testing."""

    def __init__(self) -> None:
        self.__test_count = 0
        self.__pass_count = 0
        self.__fail_count = 0

    @property
    def test_count(self) -> int:
        return self.__test_count

    @property
    def pass_count(self) -> int:
        return self.__pass_count

    @property
    def fail_count(self) -> int:
        return self.__fail_count

    def log(self, msg: str) -> None:
        print(f"[E2E LOG] {msg}")

    def __str__(self) -> str:
        return "TestLogger()"

    def __repr__(self) -> str:
        return "TestLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TestLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ================================================================
# Base Abstraction for E2E Tests
# ================================================================

class BaseE2ETest(ABC):
    """
    Unified abstract base class for E2E tests.

    Provides:
    - Composition (logger)
    - Encapsulation (_result, _errors)
    - Polymorphic run()
    - Optional lifecycle hooks (before/after)
    """

    def __init__(self) -> None:
        self._logger = TestLogger()
        self._result: bool | None = None
        self._errors: list[str] = []
        self.__instance_id = id(self)
        self.__created = True

    # ---- Optional hooks for subclasses ----
    def before_run(self) -> None:
        """Hook before test execution."""
        return None

    def after_run(self) -> None:
        """Hook after test execution."""
        return None

    def add_error(self, msg: str) -> None:
        self._errors.append(msg)
        self._logger.log(f"[ERROR] {msg}")

    @abstractmethod
    def execute(self) -> bool:
        """Actual test logic."""
        raise NotImplementedError

    # ---- Unified run() method (Polymorphism) ----
    def run(self) -> bool:
        test_name = self.__class__.__name__
        self._logger.log(f"Running {test_name}...")

        self.before_run()

        try:
            self._result = self.execute()
        except Exception as e:
            self.add_error(str(e))
            self._result = False
        finally:
            self.after_run()

        if self._errors:
            self._logger.log(f"{test_name} encountered errors: {self._errors}")

        return bool(self._result)

    def __str__(self) -> str:
        return "BaseE2ETest()"

    def __repr__(self) -> str:
        return "BaseE2ETest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseE2ETest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ================================================================
# Concrete E2E Test Classes
# ================================================================

class PipelineMockTest(BaseE2ETest):
    """Validate pipeline using mock TOC + content."""

    def execute(self) -> bool:
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

        return (
            all(validate_toc_entry(item) for item in toc)
            and all(validate_content_item(item) for item in content)
        )

    def __str__(self) -> str:
        return "PipelineMockTest()"

    def __repr__(self) -> str:
        return "PipelineMockTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PipelineMockTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class OutputWriterTest(BaseE2ETest):
    """Verify JSON report generator imports correctly."""

    def execute(self) -> bool:
        import src.support.json_report_generator
        return src.support.json_report_generator is not None

    def __str__(self) -> str:
        return "OutputWriterTest()"

    def __repr__(self) -> str:
        return "OutputWriterTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, OutputWriterTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ConfigLoadingTest(BaseE2ETest):
    """Verify config loading module availability."""

    def execute(self) -> bool:
        import src.core.config.base_config
        return src.core.config.base_config is not None

    def __str__(self) -> str:
        return "ConfigLoadingTest()"

    def __repr__(self) -> str:
        return "ConfigLoadingTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ConfigLoadingTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class LoggerInitializationTest(BaseE2ETest):
    """Ensure logger module is importable."""

    def execute(self) -> bool:
        import src.utils.logger
        return src.utils.logger is not None

    def __str__(self) -> str:
        return "LoggerInitializationTest()"

    def __repr__(self) -> str:
        return "LoggerInitializationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LoggerInitializationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class EndToEndMockWorkflowTest(BaseE2ETest):
    """Verify mock JSONL data formatting flow."""

    def execute(self) -> bool:
        from tests.helpers.mock_data import generate_mock_content
        from tests.helpers.validation_utils import validate_jsonl_format

        data = generate_mock_content(20)
        return validate_jsonl_format(data) and len(data) == 20

    def __str__(self) -> str:
        return "EndToEndMockWorkflowTest()"

    def __repr__(self) -> str:
        return "EndToEndMockWorkflowTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EndToEndMockWorkflowTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ================================================================
# Unified Test Runner (Encapsulation + Polymorphism)
# ================================================================

class E2ETestRunner:
    """Executes all E2E tests using polymorphic dispatch."""

    def __init__(self) -> None:
        self._tests: list[BaseE2ETest] = []
        self.__instance_id = id(self)
        self.__created = True

    def add_test(self, test: BaseE2ETest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        """Execute all E2E tests and return global result."""
        return all(test.run() for test in self._tests)

    def __str__(self) -> str:
        return "E2ETestRunner()"

    def __repr__(self) -> str:
        return "E2ETestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, E2ETestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ================================================================
# PyTest Entry Point
# ================================================================

def test_end_to_end_suite():
    """Run the full E2E suite."""

    runner = E2ETestRunner()

    # Register tests
    runner.add_test(PipelineMockTest())
    runner.add_test(OutputWriterTest())
    runner.add_test(ConfigLoadingTest())
    runner.add_test(LoggerInitializationTest())
    runner.add_test(EndToEndMockWorkflowTest())

    assert runner.run_all(), "One or more E2E tests failed."
