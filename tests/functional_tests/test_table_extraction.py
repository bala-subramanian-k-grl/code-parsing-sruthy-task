"""
Table extraction test suite with OOP design.
Tests TableExtractor and TableExtractionPipeline functionality.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod


class TableTestLogger:
    """Logger for table extraction tests."""

    def log(self, message: str) -> None:
        print(f"[TABLE TEST] {message}")


class BaseTableTest(ABC):
    """Abstract base class for table extraction tests."""

    def __init__(self) -> None:
        self._logger = TableTestLogger()
        self._result: bool | None = None
        self._errors: list[str] = []
        self._start_time: float = 0.0
        self._end_time: float = 0.0

    def setup(self) -> None:
        self._logger.log(f"Setting up {self.__class__.__name__}")
        self._start_time = time.time()

    @abstractmethod
    def run_test(self) -> bool:
        """Child classes override with test logic."""
        pass

    def teardown(self) -> None:
        self._end_time = time.time()
        duration = round(self._end_time - self._start_time, 4)
        self._logger.log(f"Teardown {self.__class__.__name__} ({duration}s)")

    def run(self) -> bool:
        try:
            self.setup()
            self._result = self.run_test()
        except Exception as e:
            self._errors.append(str(e))
            self._logger.log(f"ERROR: {e}")
            self._result = False
        finally:
            self.teardown()
        return bool(self._result)


class TableExtractorInitTest(BaseTableTest):
    """Test TableExtractor initialization."""

    def run_test(self) -> bool:
        self._logger.log("Testing TableExtractor initialization...")
        from src.extractors.table_extractor import TableExtractor

        extractor = TableExtractor()
        return (
            hasattr(extractor, "extract") and
            hasattr(extractor, "get_metadata") and
            extractor.extractor_type == "table"
        )


class TableExtractorMethodsTest(BaseTableTest):
    """Test TableExtractor has required methods."""

    def run_test(self) -> bool:
        self._logger.log("Testing TableExtractor methods...")
        from src.extractors.table_extractor import TableExtractor

        return (
            hasattr(TableExtractor, "extract") and
            hasattr(TableExtractor, "get_metadata") and
            hasattr(TableExtractor, "priority")
        )


class TablePipelineInitTest(BaseTableTest):
    """Test TableExtractionPipeline initialization."""

    def run_test(self) -> bool:
        self._logger.log("Testing TableExtractionPipeline initialization...")
        from src.orchestrator.table_extraction_pipeline import (
            TableExtractionPipeline,
        )

        return (
            hasattr(TableExtractionPipeline, "extract_and_save") and
            hasattr(TableExtractionPipeline, "validate_pipeline")
        )


class TableWriterInitTest(BaseTableTest):
    """Test TableWriter initialization."""

    def run_test(self) -> bool:
        self._logger.log("Testing TableWriter initialization...")
        from src.writers.table_writer import TableWriter

        writer = TableWriter("test_doc")
        return (
            hasattr(writer, "write_tables") and
            hasattr(writer, "get_metadata")
        )


class TableTestRunner:
    """Runs table extraction tests."""

    def __init__(self) -> None:
        self._tests: list[BaseTableTest] = []

    def add_test(self, test: BaseTableTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        results: list[bool] = []
        for test in self._tests:
            result = test.run()
            status = "PASSED" if result else "FAILED"
            print(f"[RESULT] {test.__class__.__name__}: {status}")
            results.append(result)
        return all(results)


def test_table_extraction_suite():
    """Pytest entry point for table extraction tests."""
    runner = TableTestRunner()

    runner.add_test(TableExtractorInitTest())
    runner.add_test(TableExtractorMethodsTest())
    runner.add_test(TablePipelineInitTest())
    runner.add_test(TableWriterInitTest())

    assert runner.run_all()
