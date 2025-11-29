"""
Enterprise-grade OOP import validation tests.
"""


from __future__ import annotations

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
from src.core.interfaces.pipeline_interface import PipelineInterface
from src.search.jsonl_searcher import JSONLSearcher
from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.utils import timer as timer_module

# ============================================================
# Base Abstract Test (Abstraction)
# ============================================================

class BaseImportTest(ABC):
    """Abstract base class for import validation tests."""

    @abstractmethod
    def run(self) -> bool:
        """Execute the import test and return success status."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        """Validate test preconditions."""
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup after test."""
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return "BaseImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Composition Example (HAS-A Relationship)
# ============================================================

class ImportLogger:
    """Small logger for demonstrating composition in tests."""

    def log(self, module_name: str, success: bool) -> str:
        status = "SUCCESS" if success else "FAILED"
        return f"[IMPORT CHECK] {module_name}: {status}"

    def __str__(self) -> str:
        return "ImportLogger()"

    def __repr__(self) -> str:
        return "ImportLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ImportLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class CompositionImportTest(BaseImportTest):
    """Test demonstrating composition with dynamic import."""

    def __init__(self, module_name: str):
        self._module_name = module_name
        self._logger = ImportLogger()
        self.__instance_id = id(self)
        self.__created = True

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        try:
            importlib.import_module(self._module_name)
            msg = self._logger.log(self._module_name, True)
            assert "SUCCESS" in msg, (
                "Logger failed to report success"
            )
            return True
        except ImportError as e:
            msg = self._logger.log(self._module_name, False)
            raise ImportError(
                f"Failed to import {self._module_name}: {e}"
            ) from e

    def __str__(self) -> str:
        return "CompositionImportTest()"

    def __repr__(self) -> str:
        return "CompositionImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CompositionImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Concrete Import Tests
# ============================================================

class ConfigImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    @property
    def passed(self) -> bool:
        return self.__passed

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert src.core.config.base_config is not None, (
            "base_config is None"
        )
        assert src.core.config.constants is not None, (
            "constants is None"
        )
        assert hasattr(src.core.config.constants, "ParserMode"), (
            "Missing ParserMode"
        )
        return True

    def __str__(self) -> str:
        return "ConfigImportTest()"

    def __repr__(self) -> str:
        return "ConfigImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ConfigImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class CoreModuleImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert src.orchestrator.pipeline_orchestrator is not None, (
            "pipeline_orchestrator missing"
        )
        assert src.parser.pdf_parser is not None, (
            "pdf_parser missing"
        )
        assert src.parser.toc_extractor is not None, (
            "toc_extractor missing"
        )
        assert hasattr(src.parser.pdf_parser, "PDFParser"), (
            "Missing PDFParser"
        )
        return True

    def __str__(self) -> str:
        return "CoreModuleImportTest()"

    def __repr__(self) -> str:
        return "CoreModuleImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CoreModuleImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class LoggerImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert src.utils.logger is not None, (
            "logger module missing"
        )
        assert hasattr(src.utils.logger, "info"), (
            "logger missing info()"
        )
        assert hasattr(src.utils.logger, "error"), (
            "logger missing error()"
        )
        return True

    def __str__(self) -> str:
        return "LoggerImportTest()"

    def __repr__(self) -> str:
        return "LoggerImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LoggerImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class UtilsImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert src.parser.base_parser is not None, (
            "base_parser missing"
        )
        assert timer_module is not None, "timer module missing"
        assert callable(timer_module), (
            "timer decorator not callable"
        )
        return True

    def __str__(self) -> str:
        return "UtilsImportTest()"

    def __repr__(self) -> str:
        return "UtilsImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UtilsImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class InterfaceImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert hasattr(PipelineInterface, "__name__"), (
            "PipelineInterface missing"
        )
        assert hasattr(PipelineInterface, "execute"), (
            "Missing execute()"
        )
        assert hasattr(PipelineInterface, "validate"), (
            "Missing validate()"
        )
        return True

    def __str__(self) -> str:
        return "InterfaceImportTest()"

    def __repr__(self) -> str:
        return "InterfaceImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, InterfaceImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class SupportModuleImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert hasattr(JSONReportGenerator, "__name__"), (
            "JSONReportGenerator missing"
        )
        assert hasattr(ExcelReportGenerator, "__name__"), (
            "ExcelReportGenerator missing"
        )
        assert hasattr(JSONLSearcher, "__name__"), (
            "JSONLSearcher missing"
        )
        assert hasattr(JSONLSearcher, "search"), (
            "JSONLSearcher missing search()"
        )
        return True

    def __str__(self) -> str:
        return "SupportModuleImportTest()"

    def __repr__(self) -> str:
        return "SupportModuleImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SupportModuleImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ModelImportTest(BaseImportTest):
    def __init__(self) -> None:
        self.__test_id = id(self)
        self.__passed = False

    @property
    def test_id(self) -> int:
        return self.__test_id

    def validate(self) -> bool:
        return True

    def cleanup(self) -> None:
        pass

    def run(self) -> bool:
        self.__passed = True
        assert src.core.config.models is not None, (
            "models module missing"
        )
        assert hasattr(src.core.config.models, "ParserResult"), (
            "Missing ParserResult"
        )
        assert hasattr(src.core.config.models, "Metadata"), (
            "Missing Metadata"
        )
        return True

    def __str__(self) -> str:
        return "ModelImportTest()"

    def __repr__(self) -> str:
        return "ModelImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ModelImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Polymorphic Test Runner
# ============================================================

class ImportTestRunner:
    """Executes BaseImportTest objects polymorphically."""

    def __init__(self):
        self.__tests: list[BaseImportTest] = []
        self.__instance_id = id(self)
        self.__run_count = 0

    @property
    def tests(self) -> list[BaseImportTest]:
        return list(self.__tests)

    @property
    def run_count(self) -> int:
        return self.__run_count

    def add_test(self, test: BaseImportTest) -> None:
        self.__tests.append(test)

    def run_all(self) -> bool:
        """Return True only if *all* tests pass."""
        self.__run_count += 1
        for test in self.__tests:
            try:
                if not test.run():
                    print(f"[FAILED] {test}")
                    return False
            except AssertionError as e:
                print(f"[ASSERTION ERROR] {test}: {e}")
                return False
            except Exception as e:
                print(f"[ERROR] {test}: {e}")
                return False
        return True

    def __str__(self) -> str:
        return "ImportTestRunner()"

    def __repr__(self) -> str:
        return "ImportTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ImportTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# PyTest Entry
# ============================================================

def test_all_imports():
    """Execute full import validation test suite."""
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
