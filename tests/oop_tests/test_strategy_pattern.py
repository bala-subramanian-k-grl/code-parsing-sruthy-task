"""Test strategy pattern."""

from abc import ABC, abstractmethod
from typing import Any


class ExtractionStrategy(ABC):
    """Abstract extraction strategy."""

    @abstractmethod
    def extract(self, data: Any) -> list[Any]:
        """Extract data using strategy."""


class SimpleStrategy(ExtractionStrategy):
    """Simple extraction strategy."""

    def extract(self, data: Any) -> list[Any]:
        """Extract using simple method."""
        return [data]


class ComplexStrategy(ExtractionStrategy):
    """Complex extraction strategy."""

    def extract(self, data: Any) -> list[Any]:
        """Extract using complex method."""
        return [data, data]


class Extractor:
    """Extractor using strategy pattern."""

    def __init__(self, strategy: ExtractionStrategy) -> None:
        """Initialize with strategy."""
        self.__strategy = strategy

    def process(self, data: Any) -> list[Any]:
        """Process data using strategy."""
        return self.__strategy.extract(data)


class TestStrategyPattern:
    """Test strategy pattern."""

    def test_simple_strategy(self) -> None:
        """Test simple extraction strategy."""
        strategy = SimpleStrategy()
        extractor = Extractor(strategy)
        result = extractor.process("test")
        assert result == ["test"]

    def test_complex_strategy(self) -> None:
        """Test complex extraction strategy."""
        strategy = ComplexStrategy()
        extractor = Extractor(strategy)
        result = extractor.process("test")
        assert result == ["test", "test"]

    def test_strategy_switching(self) -> None:
        """Test switching strategies at runtime."""
        extractor = Extractor(SimpleStrategy())
        result1 = extractor.process("data")
        assert len(result1) == 1

        extractor = Extractor(ComplexStrategy())
        result2 = extractor.process("data")
        assert len(result2) == 2
