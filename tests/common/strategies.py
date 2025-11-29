"""Enterprise-grade test strategies (Strategy Pattern)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

# ==========================================================
# Base Strategy (Abstraction + Polymorphism)
# ==========================================================

class TestStrategy(ABC):
    """Abstract base class for test strategies."""

    def __init__(self) -> None:
        self.__execution_count = 0

    @property
    def execution_count(self) -> int:
        return self.__execution_count

    def _increment_execution(self) -> None:
        self.__execution_count += 1

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the strategy using supplied arguments."""
        raise NotImplementedError

    def name(self) -> str:
        """Return human-friendly strategy name."""
        return self.__class__.__name__

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return self.__execution_count


# ==========================================================
# Attribute Setter Strategy
# ==========================================================

class AttributeSetterStrategy(TestStrategy):
    """
    Strategy for dynamically setting attributes on objects.

    Example:
        strategy = AttributeSetterStrategy()
        strategy.execute(obj, "name", "value")
    """

    def execute(self, obj: Any, attr: str, value: Any) -> None:
        """Set attribute on an object safely."""
        self._increment_execution()
        try:
            setattr(obj, attr, value)
        except Exception as e:
            raise AttributeError(
                f"Cannot set attribute '{attr}' on {type(obj).__name__}: {e}"
            ) from e

    def __str__(self) -> str:
        return "AttributeSetterStrategy()"

    def __repr__(self) -> str:
        return "AttributeSetterStrategy()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AttributeSetterStrategy)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ==========================================================
# Validation Strategy
# ==========================================================

class ValidationStrategy(TestStrategy):
    """
    Strategy for simple validation based on a dict schema.

    Schema Format:
        {
            "required": ["field1", "field2"],
            "types": {"field1": str, "field2": int}
        }
    """

    def execute(self, data: Any, schema: dict[str, Any]) -> bool:
        """Validate data against a schema."""
        self._increment_execution()
        if not isinstance(data, dict):
            return False

        # Required fields
        required = schema.get("required", [])
        if not all(field in data for field in required):
            return False

        # Type validation
        types = schema.get("types", {})
        for field, expected_type in types.items():
            if field in data and not isinstance(data[field], expected_type):
                return False

        return True

    def __str__(self) -> str:
        return "ValidationStrategy()"

    def __repr__(self) -> str:
        return "ValidationStrategy()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidationStrategy)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ==========================================================
# Backward compatibility alias
# ==========================================================

mock_strategy = AttributeSetterStrategy
