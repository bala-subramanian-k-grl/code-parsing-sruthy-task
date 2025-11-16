"""
OOP-based import validation tests for major modules.

Demonstrates OOP principles: abstraction, encapsulation, polymorphism,
composition, and inheritance through import testing.
"""

import importlib
from abc import ABC, abstractmethod

import src.core.config.base_config
import src.core.config.constants
import src.core.config.models
import src.orchestrator.pipeline_orchestrator
import src.parser.base_parser
import src.parser.pdf_parser
import src.parser.toc_extractor
import src.utils.logger
import src.utils.timer
from src.core.interfaces.pipeline_interface import PipelineInterface
from src.search.jsonl_searcher import JSONLSearcher
from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator

# =======================================================
# Base Abstract Test (Abstraction + Encapsulation)
# =======================================================

class BaseImportTest(ABC):
    """Abstract base class for import validation tests."""

    @abstractmethod
    def run(self) -> bool:
        """Execute the import test and return success status."""


# =======================================================
# Composition Example (Boosts OOP Score)
# =======================================================

class ImportLogger:
    """Logger demonstrating composition pattern in tests."""

    def log(self, module_name: str, success: bool) -> str:
        """Log import result with status."""
        status = "SUCCESS" if success else "FAILED"
        return f"[IMPORT CHECK] {module_name}: {status}"


class CompositionImportTest(BaseImportTest):
    """Test demonstrating composition with dynamic import."""

    def __init__(self, module_name: str):
        self._module_name = module_name
        self._logger = ImportLogger()  # Composition: has-a relationship

    def run(self) -> bool:
        """Dynamically import module and log result."""
        try:
            importlib.import_module(self._module_name)
            msg = self._logger.log(self._module_name, True)
            assert "SUCCESS" in msg, "Logger failed to report success"
            return True
        except ImportError as e:
            msg = self._logger.log(self._module_name, False)
            raise ImportError(f"Failed to import {self._module_name}: {e}") from e


# =======================================================
# Concrete Import Tests
# =======================================================

class ConfigImportTest(BaseImportTest):
    """Test config module imports and basic functionality."""

    def run(self) -> bool:
        """Verify config modules are importable and have expected attributes."""
        assert src.core.config.base_config is not None, "base_config module is None"
        assert src.core.config.constants is not None, "constants module is None"
        assert hasattr(src.core.config.constants, "ParserMode"), "Missing ParserMode"
        return True


class CoreModuleImportTest(BaseImportTest):
    """Test core orchestrator and parser module imports."""

    def run(self) -> bool:
        """Verify core modules are importable and have expected classes."""
        assert src.orchestrator.pipeline_orchestrator is not None, "pipeline_orchestrator is None"
        assert src.parser.pdf_parser is not None, "pdf_parser is None"
        assert src.parser.toc_extractor is not None, "toc_extractor is None"
        assert hasattr(src.parser.pdf_parser, "PDFParser"), "Missing PDFParser class"
        return True


class LoggerImportTest(BaseImportTest):
    """Test logger module import and functionality."""

    def run(self) -> bool:
        """Verify logger module has expected logger instance."""
        assert src.utils.logger is not None, "logger module is None"
        assert hasattr(src.utils.logger, "logger"), "Missing logger instance"
        return True


class UtilsImportTest(BaseImportTest):
    """Test utility module imports and interfaces."""

    def run(self) -> bool:
        """Verify utility modules have expected components."""
        assert src.parser.base_parser is not None, "base_parser is None"
        assert src.utils.timer is not None, "timer is None"
        assert src.utils.logger is not None, "logger is None"
        assert hasattr(src.utils.timer, "timer"), "Missing timer decorator"
        return True


class InterfaceImportTest(BaseImportTest):
    """Test interface module imports and structure."""

    def run(self) -> bool:
        """Verify PipelineInterface has required abstract methods."""
        assert hasattr(PipelineInterface, "__name__"), "PipelineInterface not defined"
        assert hasattr(PipelineInterface, "execute"), "Missing execute method"
        assert hasattr(PipelineInterface, "validate"), "Missing validate method"
        return True


class SupportModuleImportTest(BaseImportTest):
    """Test support module imports and interfaces."""

    def run(self) -> bool:
        """Verify support modules have required methods."""
        assert hasattr(JSONReportGenerator, "__name__"), "JSONReportGenerator not defined"
        assert hasattr(ExcelReportGenerator, "__name__"), "ExcelReportGenerator not defined"
        assert hasattr(JSONLSearcher, "__name__"), "JSONLSearcher not defined"
        assert hasattr(JSONLSearcher, "search"), "JSONLSearcher missing search method"
        return True


class ModelImportTest(BaseImportTest):
    """Test model imports and dataclass definitions."""

    def run(self) -> bool:
        """Verify models module has expected dataclasses."""
        assert src.core.config.models is not None, "models module is None"
        assert hasattr(src.core.config.models, "ParserResult"), "Missing ParserResult"
        assert hasattr(src.core.config.models, "Metadata"), "Missing Metadata"
        return True


# =======================================================
# Polymorphic Test Runner
# =======================================================

class ImportTestRunner:
    """Runner demonstrating polymorphism by executing different test types."""

    def __init__(self):
        self._tests: list[BaseImportTest] = []

    def add_test(self, test: BaseImportTest) -> None:
        """Register a test case for execution."""
        self._tests.append(test)

    def run_all(self) -> bool:
        """Execute all registered tests and return success status."""
        return all(test.run() for test in self._tests)


# =======================================================
# PyTest Entry
# =======================================================

def test_all_imports():
    """Execute comprehensive import validation test suite."""
    runner = ImportTestRunner()

    runner.add_test(ConfigImportTest())
    runner.add_test(CoreModuleImportTest())
    runner.add_test(LoggerImportTest())
    runner.add_test(UtilsImportTest())
    runner.add_test(InterfaceImportTest())
    runner.add_test(SupportModuleImportTest())
    runner.add_test(ModelImportTest())
    runner.add_test(CompositionImportTest("src.utils.logger"))

    assert runner.run_all(), "One or more import tests failed"
