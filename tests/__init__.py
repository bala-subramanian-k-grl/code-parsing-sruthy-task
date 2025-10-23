"""Test package with OOP principles."""

from abc import ABC, abstractmethod
from typing import Any


class BaseTestCase(ABC):  # Abstraction
    """Abstract base test case (Abstraction, Encapsulation)."""

    def __init__(self):
        self._test_data: dict[str, Any] = {}  # Encapsulation

    @abstractmethod  # Abstraction: must be implemented
    def setup_test_data(self) -> None:
        """Setup test data."""

    def _add_test_data(
        self, key: str, value: Any
    ) -> None:  # Encapsulation: protected
        """Add test data."""
        self._test_data[key] = value

    @property  # Encapsulation: controlled access
    def test_data(self) -> dict[str, Any]:
        """Get test data."""
        return self._test_data.copy()


class MockTestCase(BaseTestCase):  # Inheritance
    """Mock test case (Inheritance, Polymorphism)."""

    def setup_test_data(self) -> None:  # Polymorphism
        """Setup mock test data."""
        self._add_test_data("mock_key", "mock_value")
        self._add_test_data("test_count", 42)


class TestHelper:  # Encapsulation
    """Test helper utilities (Encapsulation, Abstraction)."""

    @staticmethod  # Abstraction: utility method
    def create_mock_data(count: int = 5) -> list[str]:
        """Create mock data."""
        return [f"mock_item_{i}" for i in range(count)]

    @staticmethod  # Abstraction: utility method
    def validate_test_result(result: Any, expected_type: type) -> bool:
        """Validate test result."""
        return isinstance(result, expected_type)


# Factory function (Abstraction)
def create_test_case(test_type: str = "mock") -> BaseTestCase:
    """Factory function for test cases (Polymorphism)."""
    if test_type == "mock":
        return MockTestCase()
    # Default case - could be extended for other test types
    return MockTestCase()


__all__ = ["BaseTestCase", "MockTestCase", "TestHelper", "create_test_case"]
