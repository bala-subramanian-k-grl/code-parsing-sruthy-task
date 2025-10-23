"""Interface definition for enhanced polymorphism."""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class Processable(Protocol):
    """Protocol for processable objects."""

    def process(self) -> Any:
        """Process the object."""
        ...


class Cacheable(ABC):
    """Abstract base class for cacheable objects."""

    @abstractmethod
    def get_cache_key(self) -> str:
        """Get unique cache key."""

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear object cache."""

    def __hash__(self) -> int:  # Magic method
        """Hash based on cache key."""
        return hash(self.get_cache_key())


class Configurable(ABC):
    """Abstract base class for configurable objects."""

    @abstractmethod
    def configure(self, **kwargs: Any) -> None:
        """Configure object with parameters."""

    @abstractmethod
    def get_config(self) -> dict[str, Any]:
        """Get current configuration."""

    @abstractmethod
    def reset_config(self) -> None:
        """Reset to default configuration."""


class Validatable(ABC):
    """Abstract base class for validatable objects."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate object state."""

    @abstractmethod
    def get_validation_errors(self) -> list[str]:
        """Get validation error messages."""

    def is_valid(self) -> bool:
        """Check if object is valid."""
        return self.validate() and not self.get_validation_errors()


class Serializable(ABC):
    """Abstract base class for serializable objects."""

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Serialize object to dictionary."""

    @abstractmethod
    def deserialize(self, data: dict[str, Any]) -> None:
        """Deserialize from dictionary."""

    def to_json(self) -> str:
        """Convert to JSON string."""
        import json

        return json.dumps(self.serialize())


class Observable:
    """Abstract base class for observable objects."""

    def __init__(self) -> None:
        self.__observers: list[Any] = []  # Private observers

    def add_observer(self, observer: Any) -> None:
        """Add observer."""
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer: Any) -> None:
        """Remove observer."""
        if observer in self.__observers:
            self.__observers.remove(observer)

    def _notify_observers(self, event: str, data: Any = None) -> None:
        """Notify all observers."""
        for observer in self.__observers:
            if hasattr(observer, "update"):
                observer.update(event, data)

    @property
    def observer_count(self) -> int:
        """Get number of observers."""
        return len(self.__observers)
