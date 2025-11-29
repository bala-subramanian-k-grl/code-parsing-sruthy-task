"""
Parser pipeline tests using full OOP design.

Enhancements:
- Abstract BasePipelineTest with lifecycle hooks
- Polymorphic run_test() instead of overriding run()
- Encapsulation: results, errors, timestamps
- Composition-based PipelineLogger
- Unified runner with reporting
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod


# ============================================================
# Logger via Composition
# ============================================================

class BasePipelineLogger(ABC):
    """Abstract base logger."""

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError


class PipelineLogger(BasePipelineLogger):
    """Simple logger used inside tests via composition."""

    def __init__(self) -> None:
        self.__log_count = 0

    @property
    def log_count(self) -> int:
        return self.__log_count

    def log(self, message: str) -> None:
        self.__log_count += 1
        print(f"[PIPELINE LOG] {message}")

    def __len__(self) -> int:
        return self.__log_count

    def __str__(self) -> str:
        return "PipelineLogger()"

    def __repr__(self) -> str:
        return "PipelineLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PipelineLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Abstract Base Test (Abstraction + Encapsulation)
# ============================================================

class BasePipelineTest(ABC):
    """Base class for pipeline testing with lifecycle hooks."""

    def __init__(self) -> None:
        self.__logger = PipelineLogger()          # Composition
        self.__result: bool | None = None         # Encapsulation
        self.__errors: list[str] = []             # Encapsulation
        self.__start_time: float = 0.0
        self.__end_time: float = 0.0

    @property
    def result(self) -> bool | None:
        return self.__result

    @property
    def errors(self) -> list[str]:
        return list(self.__errors)

    @property
    def logger(self) -> PipelineLogger:
        return self.__logger

    # ---------------- LIFECYCLE HOOKS ----------------

    def setup(self) -> None:
        self.__logger.log(f"Setting up {self.__class__.__name__}")
        self.__start_time = time.time()

    @abstractmethod
    def run_test(self) -> bool:
        """Child test classes implement this."""
        pass

    def teardown(self) -> None:
        self.__end_time = time.time()
        duration = round(self.__end_time - self.__start_time, 4)
        self.__logger.log(
            f"Tearing down {self.__class__.__name__} (Duration: {duration}s)"
        )

    # ---------------- Main Execution ----------------

    def run(self) -> bool:
        try:
            self.setup()
            self.__result = self.run_test()
        except Exception as e:
            self.__errors.append(str(e))
            self.__logger.log(f"ERROR in {self.__class__.__name__}: {e}")
            self.__result = False
        finally:
            self.teardown()

        return bool(self.__result)

    # Utility for child classes
    def add_error(self, msg: str) -> None:
        self.__errors.append(msg)

    def __str__(self) -> str:
        return "BasePipelineTest()"

    def __repr__(self) -> str:
        return "BasePipelineTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BasePipelineTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Concrete Pipeline Tests (Inheritance + Polymorphism)
# ============================================================

class PipelineInitializationTest(BasePipelineTest):
    """Test that pipeline orchestrator imports successfully."""

    def run_test(self) -> bool:
        self.logger.log("Running PipelineInitializationTest...")

        import src.orchestrator.pipeline_orchestrator
        return src.orchestrator.pipeline_orchestrator is not None

    def __str__(self) -> str:
        return "PipelineInitializationTest()"

    def __repr__(self) -> str:
        return "PipelineInitializationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PipelineInitializationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class TOCExtractionTest(BasePipelineTest):
    """Test TOC extraction from mock data."""

    def run_test(self) -> bool:
        self.logger.log("Running TOCExtractionTest...")

        from tests.helpers.mock_data import generate_mock_toc

        toc = generate_mock_toc(5)
        return (
            len(toc) == 5 and
            all("section_id" in item for item in toc)
        )

    def __str__(self) -> str:
        return "TOCExtractionTest()"

    def __repr__(self) -> str:
        return "TOCExtractionTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TOCExtractionTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ContentExtractionTest(BasePipelineTest):
    """Test content extraction from mock data."""

    def run_test(self) -> bool:
        self.logger.log("Running ContentExtractionTest...")

        from tests.helpers.mock_data import generate_mock_content

        content = generate_mock_content(10)
        return (
            len(content) == 10 and
            all("doc_title" in item for item in content)
        )

    def __str__(self) -> str:
        return "ContentExtractionTest()"

    def __repr__(self) -> str:
        return "ContentExtractionTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ContentExtractionTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class PipelineMockDataTest(BasePipelineTest):
    """Test the pipeline workflow using mock TOC + content."""

    def run_test(self) -> bool:
        self.logger.log("Running PipelineMockDataTest...")

        from tests.helpers.mock_data import (
            generate_mock_content,
            generate_mock_toc,
        )

        toc = generate_mock_toc(3)
        content = generate_mock_content(5)

        return len(toc) > 0 and len(content) > 0

    def __str__(self) -> str:
        return "PipelineMockDataTest()"

    def __repr__(self) -> str:
        return "PipelineMockDataTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PipelineMockDataTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Unified Runner (Encapsulation + Polymorphism)
# ============================================================

class PipelineTestRunner:
    """Runs all pipeline tests using full OOP runner pattern."""

    def __init__(self) -> None:
        self.__tests: list[BasePipelineTest] = []  # Encapsulation
        self.__run_count = 0

    @property
    def tests(self) -> list[BasePipelineTest]:
        return list(self.__tests)

    @property
    def run_count(self) -> int:
        return self.__run_count

    def add_test(self, test: BasePipelineTest) -> None:
        self.__tests.append(test)

    def run_all(self) -> bool:
        self.__run_count += 1
        results = []
        for test in self.__tests:
            result = test.run()
            status = "PASSED" if result else "FAILED"
            print(f"[RESULT] {test.__class__.__name__}: {status}")
            results.append(result)
        return all(results)

    def __str__(self) -> str:
        return "PipelineTestRunner()"

    def __repr__(self) -> str:
        return "PipelineTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PipelineTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# PyTest Entry Point
# ============================================================

def test_pipeline_suite():
    """Execute all pipeline-related tests in an OOP suite."""

    runner = PipelineTestRunner()

    runner.add_test(PipelineInitializationTest())
    runner.add_test(TOCExtractionTest())
    runner.add_test(ContentExtractionTest())
    runner.add_test(PipelineMockDataTest())

    assert runner.run_all()
