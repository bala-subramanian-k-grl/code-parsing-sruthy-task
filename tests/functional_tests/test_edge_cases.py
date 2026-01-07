"""
Negative and edge case tests rewritten with strong OOP design.

"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

# ======================================================
# Logger via Composition
# ======================================================


class BaseEdgeLogger(ABC):
    """Abstract base logger."""

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError


class EdgeLogger(BaseEdgeLogger):
    """Simple logger injected via composition."""

    def __init__(self) -> None:
        self.__log_count = 0
        self.__messages: list[str] = []
        self.__logger_id = id(self)
        self.__enabled = True

    @property
    def logger_id(self) -> int:
        return self.__logger_id

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @property
    def log_count(self) -> int:
        return self.__log_count

    @property
    def messages(self) -> list[str]:
        return list(self.__messages)

    def log(self, message: str) -> None:
        self.__log_count += 1
        self.__messages.append(message)
        print(f"[EDGE TEST] {message}")

    def __str__(self) -> str:
        return "EdgeLogger()"

    def __repr__(self) -> str:
        return "EdgeLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EdgeLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ======================================================
# Abstract Base Class (Abstraction + Encapsulation)
# ======================================================

class BaseEdgeTest(ABC):
    """
    Abstract base test with lifecycle hooks:
    - setup()
    - run_test()   <-- Child classes override this
    - teardown()

    Provides encapsulated:
    - errors
    - result
    - timestamps
    """

    def __init__(self, logger: EdgeLogger | None = None) -> None:
        self.__logger = logger or EdgeLogger()  # Composition
        self.__errors: list[str] = []
        self.__result: bool | None = None
        self.__start_time: float = 0.0
        self.__end_time: float = 0.0
        self.__instance_id = id(self)
        self.__created = True
        self.__run_count = 0
        self.__test_name = self.__class__.__name__
        self.__is_active = False
        self.__pass_status = False
        self.__duration = 0.0
        self.__error_msg = ""
        self.__test_type = "edge"
        self.__priority = 1

    @property
    def priority(self) -> int:
        return self.__priority

    @property
    def test_type(self) -> str:
        return self.__test_type

    @property
    def error_msg(self) -> str:
        return self.__error_msg

    @property
    def pass_status(self) -> bool:
        return self.__pass_status

    @property
    def duration(self) -> float:
        return self.__duration

    @property
    def test_name(self) -> str:
        return self.__test_name

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def logger(self) -> EdgeLogger:
        return self.__logger

    @property
    def errors(self) -> list[str]:
        return list(self.__errors)

    @property
    def result(self) -> bool | None:
        return self.__result

    @property
    def run_count(self) -> int:
        return self.__run_count

    # ---- LIFECYCLE HOOKS ----
    def setup(self) -> None:
        self.__logger.log(f"Setting up {self.__class__.__name__}")
        self.__start_time = time.time()

    @abstractmethod
    def run_test(self) -> bool:
        """Child must implement actual test logic."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate test can run."""
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str:
        """Get test description."""
        raise NotImplementedError

    def teardown(self) -> None:
        self.__end_time = time.time()
        duration = round(self.__end_time - self.__start_time, 4)
        self.__logger.log(
            f"Tearing down {self.__class__.__name__} (Duration: {duration}s)"
        )

    # ---- MAIN EXECUTION ----
    def run(self) -> bool:
        self.__run_count += 1
        try:
            self.setup()
            self.__result = self.run_test()
        except Exception as e:
            self.__errors.append(str(e))
            self.__logger.log(f"ERROR: {e}")
            self.__result = False
        finally:
            self.teardown()

        return bool(self.__result)

    # ---- Utility for children ----
    def add_error(self, msg: str) -> None:
        self.__errors.append(msg)

    def __str__(self) -> str:
        return "BaseEdgeTest()"

    def __repr__(self) -> str:
        return "BaseEdgeTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseEdgeTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ======================================================
# Concrete Test Classes (Inheritance + Polymorphism)
# ======================================================

class EmptyDataTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    @property
    def status(self) -> str:
        return self.__status

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test empty data handling"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running EmptyDataTest...")
        from tests.helpers.validation_utils import validate_jsonl_format

        empty: list[dict[str, Any]] = []
        return validate_jsonl_format(empty)

    def __str__(self) -> str:
        return "EmptyDataTest()"

    def __repr__(self) -> str:
        return "EmptyDataTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmptyDataTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class InvalidTOCTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test invalid TOC entry handling"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running InvalidTOCTest...")
        from tests.helpers.validation_utils import validate_toc_entry

        invalid_entry = {"invalid": "data"}
        return not validate_toc_entry(invalid_entry)

    def __str__(self) -> str:
        return "InvalidTOCTest()"

    def __repr__(self) -> str:
        return "InvalidTOCTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, InvalidTOCTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class InvalidContentItemTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test invalid content item handling"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running InvalidContentItemTest...")
        from tests.helpers.validation_utils import validate_content_item

        bad_item = {"missing": "fields"}
        return not validate_content_item(bad_item)

    def __str__(self) -> str:
        return "InvalidContentItemTest()"

    def __repr__(self) -> str:
        return "InvalidContentItemTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, InvalidContentItemTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class NonexistentFileTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test nonexistent file handling"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running NonexistentFileTest...")
        from src.parser.pdf_parser import PDFParser

        pdf_path = Path("nonexistent.pdf")
        try:
            PDFParser(pdf_path)
            return False  # Should fail
        except FileNotFoundError:
            return True
        except Exception as e:
            self.add_error(str(e))
            return True

    def __str__(self) -> str:
        return "NonexistentFileTest()"

    def __repr__(self) -> str:
        return "NonexistentFileTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NonexistentFileTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class LargeDatasetTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test large dataset handling"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running LargeDatasetTest...")
        from tests.helpers.performance_utils import generate_large_dataset

        data = generate_large_dataset(1000)
        return len(data) == 1000

    def __str__(self) -> str:
        return "LargeDatasetTest()"

    def __repr__(self) -> str:
        return "LargeDatasetTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LargeDatasetTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class MalformedDataTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test malformed data handling"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running MalformedDataTest...")
        from tests.helpers.validation_utils import count_validation_errors

        malformed: list[dict[str, Any]] = [
            {"valid": True},
            {},
            {"valid": False},
        ]

        def validator(x: dict[str, Any]) -> bool:
            return "valid" in x and x["valid"] is True

        errors = count_validation_errors(malformed, validator)
        return errors == 2

    def __str__(self) -> str:
        return "MalformedDataTest()"

    def __repr__(self) -> str:
        return "MalformedDataTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MalformedDataTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class BoundaryConditionTest(BaseEdgeTest):
    def __init__(self) -> None:
        super().__init__()
        self.__test_id = id(self)
        self.__status = "pending"

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def get_description(self) -> str:
        return "Test boundary conditions"

    def run_test(self) -> bool:
        self.__status = "running"
        self.logger.log("Running BoundaryConditionTest...")
        from tests.helpers.mock_data import generate_mock_toc

        zero_items = generate_mock_toc(0)
        one_item = generate_mock_toc(1)

        return len(zero_items) == 0 and len(one_item) == 1

    def __str__(self) -> str:
        return "BoundaryConditionTest()"

    def __repr__(self) -> str:
        return "BoundaryConditionTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BoundaryConditionTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ======================================================
# Test Runner (Polymorphism + Encapsulation)
# ======================================================

class EdgeTestRunner:
    """Executes and reports results of all tests."""

    def __init__(self) -> None:
        self.__instance_id = id(self)
        self.__created = True
        self.__tests: list[BaseEdgeTest] = []
        self.__logger = EdgeLogger()
        self.__run_count = 0
        self.__pass_count = 0
        self.__fail_count = 0
        self.__total_tests = 0
        self.__runner_id = id(self)
        self.__suite_name = "EdgeTestSuite"
        self.__is_running = False

    @property
    def is_running(self) -> bool:
        return self.__is_running

    @property
    def suite_name(self) -> str:
        return self.__suite_name

    @property
    def runner_id(self) -> int:
        return self.__runner_id

    @property
    def fail_count(self) -> int:
        return self.__fail_count

    @property
    def total_tests(self) -> int:
        return self.__total_tests

    @property
    def tests(self) -> list[BaseEdgeTest]:
        return list(self.__tests)

    @property
    def run_count(self) -> int:
        return self.__run_count

    @property
    def pass_count(self) -> int:
        return self.__pass_count

    def add_test(self, test: BaseEdgeTest) -> None:
        self.__tests.append(test)
        self.__total_tests = len(self.__tests)

    def run_all(self) -> bool:
        self.__run_count += 1
        self.__logger.log("=== RUNNING EDGE CASE SUITE ===")

        results: list[bool] = []
        for test in self.__tests:
            result: bool = test.run()
            if result:
                self.__pass_count += 1
            status = "PASSED" if result else "FAILED"
            self.__logger.log(f"{test.__class__.__name__}: {status}")
            results.append(result)

        self.__logger.log("=== SUITE COMPLETE ===")
        return all(results)

    def __str__(self) -> str:
        return "EdgeTestRunner()"

    def __repr__(self) -> str:
        return "EdgeTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EdgeTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ======================================================
# Pytest Entry Point
# ======================================================

def test_edge_case_suite():
    runner = EdgeTestRunner()

    runner.add_test(EmptyDataTest())
    runner.add_test(InvalidTOCTest())
    runner.add_test(InvalidContentItemTest())
    runner.add_test(NonexistentFileTest())
    runner.add_test(LargeDatasetTest())
    runner.add_test(MalformedDataTest())
    runner.add_test(BoundaryConditionTest())

    assert runner.run_all()
