"""Basic OOP principles tests."""

from abc import ABC, abstractmethod


class AbstractExtractor(ABC):
    """Abstract extractor for testing."""

    @abstractmethod
    def extract(self) -> list[str]:
        """Extract data."""


class ConcreteExtractor(AbstractExtractor):
    """Concrete extractor implementation."""

    def extract(self) -> list[str]:
        """Extract data."""
        return ["item1", "item2"]


class TestOOPPrinciples:
    """Test OOP principles."""

    def test_abstraction(self) -> None:
        """Test abstraction principle."""
        extractor = ConcreteExtractor()
        assert isinstance(extractor, AbstractExtractor)
        assert hasattr(extractor, "extract")

    def test_polymorphism(self) -> None:
        """Test polymorphism principle."""
        extractors: list[AbstractExtractor] = [ConcreteExtractor()]
        results = [e.extract() for e in extractors]
        assert len(results) == 1
        assert results[0] == ["item1", "item2"]

    def test_encapsulation(self) -> None:
        """Test encapsulation principle."""

        class EncapsulatedClass:
            def __init__(self) -> None:
                self.__private = "secret"

            def get_private(self) -> str:
                return self.__private

        obj = EncapsulatedClass()
        assert obj.get_private() == "secret"
        assert not hasattr(obj, "__private")
