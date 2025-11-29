"""
Advanced OOP principles tests with lifecycle.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# Logger (Composition)
# ============================================================

class ExtractorLogger:
    """Simple logger used to demonstrate composition."""
    def __init__(self) -> None:
        self.__messages: list[str] = []
        self.__log_count = 0

    @property
    def messages(self) -> list[str]:
        return self.__messages

    @property
    def log_count(self) -> int:
        return self.__log_count

    def log(self, message: str) -> None:
        self.__messages.append(message)
        self.__log_count += 1

    def __str__(self) -> str:
        return f"ExtractorLogger(logs={self.__log_count})"

    def __len__(self) -> int:
        return self.__log_count

    def __bool__(self) -> bool:
        return self.__log_count > 0

    def __repr__(self) -> str:
        return "ExtractorLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExtractorLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ============================================================
# Base Extractor (Abstraction + Encapsulation + Lifecycle)
# ============================================================

class AbstractExtractor(ABC):
    """Abstract extractor with full OOP lifecycle."""

    def __init__(self, logger: ExtractorLogger | None = None) -> None:
        self.__logger = logger or ExtractorLogger()   # Composition
        self.__data: list[str] = []                  # Encapsulation
        self.__started = False                       # Encapsulation
        self.__finished = False                      # Encapsulation

    @property
    def data(self) -> list[str]:
        return self.__data

    @property
    def started(self) -> bool:
        return self.__started

    @property
    def finished(self) -> bool:
        return self.__finished

    @property
    def logger(self) -> ExtractorLogger:
        return self.__logger

    def setup(self) -> None:
        self.__logger.log("setup")
        self.__started = True

    @abstractmethod
    def run_extract(self) -> list[str]:
        """Concrete extract implementations override this method."""
        pass

    def teardown(self) -> None:
        self.__finished = True
        self.__logger.log("teardown")

    def extract(self) -> list[str]:
        """Public lifecycle-controlled extract method."""
        self.setup()
        self.__data = self.run_extract()
        self.teardown()
        return self.__data

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> bool:
        return self.__finished

    def __len__(self) -> int:
        return len(self.__data)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AbstractExtractor)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ============================================================
# Concrete Extractor (Inheritance + Polymorphism)
# ============================================================

class ConcreteExtractor(AbstractExtractor):
    """Concrete extractor implementation."""

    def run_extract(self) -> list[str]:
        self.logger.log("extracting")
        return ["item1", "item2"]

    def __str__(self) -> str:
        return "ConcreteExtractor()"

    def __repr__(self) -> str:
        return "ConcreteExtractor()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ConcreteExtractor)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Test Suite
# ============================================================

class TestOOPPrinciples:
    """Test core OOP principles using enhanced lifecycle-based extractor."""

    def __init__(self) -> None:
        self.__test_count = 0

    @property
    def test_count(self) -> int:
        return self.__test_count

    def test_abstraction(self) -> None:
        self.__test_count += 1
        extractor = ConcreteExtractor()
        assert isinstance(extractor, AbstractExtractor)
        assert hasattr(extractor, "extract")

    def test_polymorphism(self) -> None:
        self.__test_count += 1
        extractors: list[AbstractExtractor] = [
            ConcreteExtractor(),
            ConcreteExtractor(),
        ]
        results = [e.extract() for e in extractors]

        assert results == [["item1", "item2"], ["item1", "item2"]]

    def test_lifecycle(self) -> None:
        self.__test_count += 1
        logger = ExtractorLogger()
        extractor = ConcreteExtractor(logger)
        output = extractor.extract()

        assert output == ["item1", "item2"]
        assert logger.messages == ["setup", "extracting", "teardown"]

    def test_encapsulation(self) -> None:
        self.__test_count += 1

        class Encapsulated:
            def __init__(self) -> None:
                self.__private = "hidden"

            def reveal(self) -> str:
                return self.__private

            def __str__(self) -> str:
                return "Encapsulated()"

            def __repr__(self) -> str:
                return "Encapsulated()"

            def __eq__(self, other: object) -> bool:
                return isinstance(other, Encapsulated)

            def __hash__(self) -> int:
                return hash(self.__class__.__name__)

            def __bool__(self) -> bool:
                return True

        obj = Encapsulated()
        assert obj.reveal() == "hidden"
        assert not hasattr(obj, "__private")

    def __str__(self) -> str:
        return "TestOOPPrinciples()"

    def __repr__(self) -> str:
        return "TestOOPPrinciples()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TestOOPPrinciples)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
