"""
Advanced strategy pattern tests with lifecycle.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

# ============================================================
# Logger for Composition
# ============================================================


class StrategyLogger:
    """Logger injected into strategies and context for OOP testing."""
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.__instance_id = id(self)
        self.__created = True

    def log(self, message: str) -> None:
        self.messages.append(message)

    def __str__(self) -> str:
        return "StrategyLogger()"

    def __repr__(self) -> str:
        return "StrategyLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, StrategyLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Strategy Interface (Abstraction)
# ============================================================

class ExtractionStrategy(ABC):
    """Abstract extraction strategy with lifecycle."""

    def __init__(self, logger: StrategyLogger | None = None) -> None:
        self._logger = logger or StrategyLogger()   # Composition
        self.__instance_id = id(self)
        self.__created = True

    def setup(self) -> None:
        self._logger.log(f"{self.__class__.__name__}: setup")

    @abstractmethod
    def run_extract(self, data: Any) -> list[Any]:
        """Perform extraction."""
        pass

    def teardown(self) -> None:
        self._logger.log(f"{self.__class__.__name__}: teardown")

    def extract(self, data: Any) -> list[Any]:
        """Public lifecycle wrapper."""
        self.setup()
        result = self.run_extract(data)
        self.teardown()
        return result

    def __str__(self) -> str:
        return "ExtractionStrategy()"

    def __repr__(self) -> str:
        return "ExtractionStrategy()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExtractionStrategy)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Concrete Strategies (Polymorphism)
# ============================================================

class SimpleStrategy(ExtractionStrategy):
    """Simple extraction strategy."""

    def run_extract(self, data: Any) -> list[Any]:
        self._logger.log("SimpleStrategy: extracting")
        return [data]

    def __str__(self) -> str:
        return "SimpleStrategy()"

    def __repr__(self) -> str:
        return "SimpleStrategy()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SimpleStrategy)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ComplexStrategy(ExtractionStrategy):
    """Complex extraction strategy that produces two items."""

    def run_extract(self, data: Any) -> list[Any]:
        self._logger.log("ComplexStrategy: extracting")
        return [data, data]

    def __str__(self) -> str:
        return "ComplexStrategy()"

    def __repr__(self) -> str:
        return "ComplexStrategy()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ComplexStrategy)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Context Applying Strategy (Strategy Pattern)
# ============================================================

class Extractor:
    """Context class using strategy pattern."""

    def __init__(self, strategy: ExtractionStrategy) -> None:
        self._strategy = strategy  # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    def process(self, data: Any) -> list[Any]:
        """Delegates to strategy's lifecycle extraction."""
        return self._strategy.extract(data)

    def set_strategy(self, new_strategy: ExtractionStrategy) -> None:
        """Dynamic strategy switching at runtime."""
        self._strategy = new_strategy

    def __str__(self) -> str:
        return "Extractor()"

    def __repr__(self) -> str:
        return "Extractor()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Extractor)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Test Suite
# ============================================================

class TestStrategyPattern:
    """Test advanced strategy pattern implementation."""

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

    def test_simple_strategy(self) -> None:
        logger = StrategyLogger()
        strategy = SimpleStrategy(logger)
        extractor = Extractor(strategy)

        result = extractor.process("test")

        assert result == ["test"]
        assert "SimpleStrategy: extracting" in logger.messages

    def test_complex_strategy(self) -> None:
        logger = StrategyLogger()
        strategy = ComplexStrategy(logger)
        extractor = Extractor(strategy)

        result = extractor.process("test")

        assert result == ["test", "test"]
        assert "ComplexStrategy: extracting" in logger.messages

    def test_strategy_switching(self) -> None:
        logger = StrategyLogger()
        extractor = Extractor(SimpleStrategy(logger))

        r1 = extractor.process("data")
        assert r1 == ["data"]

        extractor.set_strategy(ComplexStrategy(logger))
        r2 = extractor.process("data")
        assert r2 == ["data", "data"]

        # Verify lifecycle events appear for both strategies
        assert "SimpleStrategy: extracting" in logger.messages
        assert "ComplexStrategy: extracting" in logger.messages

    def __str__(self) -> str:
        return "TestStrategyPattern()"

    def __repr__(self) -> str:
        return "TestStrategyPattern()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TestStrategyPattern)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
