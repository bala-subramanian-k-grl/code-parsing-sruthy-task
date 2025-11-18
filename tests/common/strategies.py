"""Test strategies and patterns for testing utilities."""

from abc import ABC, abstractmethod
from typing import Any


class TestStrategy(ABC):
    """Abstract base class for test strategies."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the strategy with given arguments."""


class AttributeSetterStrategy(TestStrategy):
    """Strategy for setting object attributes in tests.

    Example:
        strategy = AttributeSetterStrategy()
        strategy.execute(my_obj, "name", "test_value")
    """

    def execute(self, obj: Any, attr: str, value: Any) -> None:
        """Set an attribute on an object.

        Args:
            obj: Object to modify
            attr: Attribute name to set
            value: Value to assign

        Raises:
            AttributeError: If attribute cannot be set
        """
        try:
            setattr(obj, attr, value)
        except (AttributeError, TypeError) as e:
            raise AttributeError(
                f"Cannot set attribute '{attr}' on {type(obj).__name__}: {e}"
            ) from e


class ValidationStrategy(TestStrategy):
    """Strategy for basic data validation against a schema.

    Schema format:
        {
            "required": ["field1", "field2"],
            "types": {"field1": str, "field2": int}
        }

    Example:
        schema = {
            "required": ["name", "age"],
            "types": {"name": str, "age": int}
        }
        strategy = ValidationStrategy()
        is_valid = strategy.execute(
            {"name": "John", "age": 30}, schema
        )
    """

    def execute(self, data: Any, schema: dict[str, Any]) -> bool:
        """Validate data against schema.

        Args:
            data: Data to validate (typically a dict)
            schema: Validation schema with 'required' and optional 'types' keys

        Returns:
            True if validation passes, False otherwise
        """
        if not isinstance(data, dict):
            return False

        # Check required fields
        required = schema.get("required", [])
        if not all(k in data for k in required):
            return False

        # Check types if specified
        types = schema.get("types", {})
        for field, expected_type in types.items():
            if field in data and not isinstance(data[field], expected_type):
                return False

        return True


# Backward compatibility alias
mock_strategy = AttributeSetterStrategy
