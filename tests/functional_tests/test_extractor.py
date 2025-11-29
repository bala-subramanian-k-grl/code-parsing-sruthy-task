"""
Extractor test suite with full OOP improvements.
Matches architecture of Edge Case Suite:
- Lifecycle hooks (setup / run_test / teardown)
- Encapsulation of internal state
- Polymorphic run_test()
- Composition-based logging
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod

# ============================================================
# Logger via Composition
# ============================================================

class ExtractorLogger:
    """Simple logger for tracing extractor test execution."""

    def log(self, message: str) -> None:
        print(f"[EXTRACTOR LOG] {message}")

    def __str__(self) -> str:
        return "ExtractorLogger()"

    def __repr__(self) -> str:
        return "ExtractorLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExtractorLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Abstract Base Test (Abstraction + Encapsulation)
# ============================================================

class BaseExtractorTest(ABC):
    """Abstract base class for extractor tests (Full OOP)."""

    def __init__(self) -> None:
        self._logger = ExtractorLogger()        # Composition
        self._result: bool | None = None        # Encapsulation
        self._errors: list[str] = []            # Encapsulation
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
        """Child classes override this with actual test logic."""
        pass

    def teardown(self) -> None:
        self._end_time = time.time()
        duration = round(self._end_time - self._start_time, 4)
        self._logger.log(
            f"Tearing down {self.__class__.__name__} (Duration: {duration}s)"
        )

    # ---------------- Main execution ----------------

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
        self._errors.append(msg)

    def __str__(self) -> str:
        return "BaseExtractorTest()"

    def __repr__(self) -> str:
        return "BaseExtractorTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseExtractorTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Concrete Tests (Inheritance + Polymorphism)
# ============================================================

class PDFExtractorInitializationTest(BaseExtractorTest):
    """Test that PDF Parser initializes and required methods exist."""

    def run_test(self) -> bool:
        self._logger.log("Running PDFExtractorInitializationTest...")

        from src.parser.pdf_parser import PDFParser

        return (
            hasattr(PDFParser, "parse")
            and hasattr(PDFParser, "__init__")
        )

    def __str__(self) -> str:
        return "PDFExtractorInitializationTest()"

    def __repr__(self) -> str:
        return "PDFExtractorInitializationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PDFExtractorInitializationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class TOCExtractorInitializationTest(BaseExtractorTest):
    """Test that TOC extractor initializes and required methods exist."""

    def run_test(self) -> bool:
        self._logger.log("Running TOCExtractorInitializationTest...")

        from src.parser.toc_extractor import TOCExtractor

        return (
            hasattr(TOCExtractor, "extract") and
            hasattr(TOCExtractor, "__init__")
        )

    def __str__(self) -> str:
        return "TOCExtractorInitializationTest()"

    def __repr__(self) -> str:
        return "TOCExtractorInitializationTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TOCExtractorInitializationTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ParserFactoryTest(BaseExtractorTest):
    """Test that ParserFactory is instantiable and provides factory method."""

    def run_test(self) -> bool:
        self._logger.log("Running ParserFactoryTest...")

        from src.parser.parser_factory import ParserFactory

        factory = ParserFactory()
        return hasattr(factory, "create_parser")

    def __str__(self) -> str:
        return "ParserFactoryTest()"

    def __repr__(self) -> str:
        return "ParserFactoryTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ParserFactoryTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class BaseParserImportTest(BaseExtractorTest):
    """Test successful import of BaseParser."""

    def run_test(self) -> bool:
        self._logger.log("Running BaseParserImportTest...")

        from src.parser.base_parser import BaseParser

        return hasattr(BaseParser, "__name__")

    def __str__(self) -> str:
        return "BaseParserImportTest()"

    def __repr__(self) -> str:
        return "BaseParserImportTest()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseParserImportTest)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Unified Test Runner (Encapsulation + Polymorphism)
# ============================================================

class ExtractorTestRunner:
    """Runs extractor-related tests using OOP runner pattern."""

    def __init__(self) -> None:
        self._tests: list[BaseExtractorTest] = []
        self.__instance_id = id(self)
        self.__created = True

    def add_test(self, test: BaseExtractorTest) -> None:
        self._tests.append(test)

    def run_all(self) -> bool:
        results: list[bool] = []
        for test in self._tests:
            result: bool = test.run()
            status = "PASSED" if result else "FAILED"
            print(f"[RESULT] {test.__class__.__name__}: {status}")
            results.append(result)
        return all(results)

    def __str__(self) -> str:
        return "ExtractorTestRunner()"

    def __repr__(self) -> str:
        return "ExtractorTestRunner()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExtractorTestRunner)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Pytest Entry Point
# ============================================================

def test_extractor_suite():
    runner = ExtractorTestRunner()

    runner.add_test(PDFExtractorInitializationTest())
    runner.add_test(TOCExtractorInitializationTest())
    runner.add_test(ParserFactoryTest())
    runner.add_test(BaseParserImportTest())

    assert runner.run_all()
