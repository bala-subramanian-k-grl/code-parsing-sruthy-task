"""Base processor classes for enhanced polymorphism."""

from abc import ABC, abstractmethod
from typing import Any

from src.utils.interfaces import Cacheable, Configurable, Validatable


class BaseProcessor(Cacheable, Configurable, Validatable, ABC):
    """Abstract base processor with multiple inheritance."""

    def __init__(self, name: str) -> None:
        self.__name = name  # Private
        self.__config: dict[str, Any] = {}  # Private
        self.__cache: dict[str, Any] = {}  # Private
        self.__errors: list[str] = []  # Private

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process input data."""

    @abstractmethod
    def get_processor_type(self) -> str:
        """Get processor type name."""

    # Cacheable interface methods
    def get_cache_key(self) -> str:
        """Get unique cache key."""
        return f"{self.__name}_{self.get_processor_type()}"

    def clear_cache(self) -> None:
        """Clear processor cache."""
        self.__cache.clear()

    # Configurable interface methods
    def configure(self, **kwargs: Any) -> None:
        """Configure processor with parameters."""
        config_dict: dict[str, Any] = dict(kwargs)
        self.__config.update(config_dict)

    def get_config(self) -> dict[str, Any]:
        """Get current configuration."""
        return self.__config.copy()

    def reset_config(self) -> None:
        """Reset to default configuration."""
        self.__config.clear()
        self.__errors.clear()

    # Validatable interface methods
    def validate(self) -> bool:
        """Validate processor state."""
        self.__errors.clear()
        if not self.__name:
            self.__errors.append("Processor name cannot be empty")
        return len(self.__errors) == 0

    def get_validation_errors(self) -> list[str]:
        """Get validation error messages."""
        return self.__errors.copy()

    @property
    def name(self) -> str:
        """Get processor name."""
        return self.__name

    def __str__(self) -> str:  # Magic method
        """String representation."""
        return f"{self.__class__.__name__}({self.__name})"

    def __call__(self, data: Any) -> Any:  # Magic method
        """Make processor callable."""
        return self.process(data)


class TextProcessor(BaseProcessor):
    """Text processing implementation."""

    def get_processor_type(self) -> str:
        """Get processor type name."""
        return "text"

    def process(self, data: Any) -> str:
        """Process text data."""
        if not isinstance(data, str):
            return str(data)
        return data.strip().replace("\n", " ")


class DataProcessor(BaseProcessor):
    """Data processing implementation."""

    def get_processor_type(self) -> str:
        """Get processor type name."""
        return "data"

    def process(self, data: Any) -> dict[str, Any]:
        """Process data structures."""
        if isinstance(data, dict):
            data_dict: dict[str, Any] = data
            keys_list: list[str] = list(data_dict.keys())
            return {
                "original": data_dict,
                "keys": keys_list,
                "size": len(data_dict),
            }
        if isinstance(data, list):
            data_list: list[Any] = data
            return {"items": data_list, "count": len(data_list)}
        return {"value": data, "type": type(data).__name__}


class ProcessorFactory:
    """Factory for creating processors."""

    __PROCESSORS: dict[str, type[BaseProcessor]] = {
        "text": TextProcessor,
        "data": DataProcessor,
    }

    @classmethod
    def create(cls, processor_type: str, name: str) -> BaseProcessor:
        """Create processor instance."""
        processors: dict[str, type[BaseProcessor]] = cls.__PROCESSORS
        if processor_type not in processors:
            raise ValueError(f"Unknown processor type: {processor_type}")
        processor_class: type[BaseProcessor] = processors[processor_type]
        return processor_class(name)

    @classmethod
    def get_available_types(cls) -> list[str]:
        """Get available processor types."""
        processors: dict[str, type[BaseProcessor]] = cls.__PROCESSORS
        return list(processors.keys())
