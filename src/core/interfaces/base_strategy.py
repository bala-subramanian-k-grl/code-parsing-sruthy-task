"""Abstract base for strategy pattern implementations."""

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """Abstract base for all strategy implementations."""

    @abstractmethod
    def execute(self, *args: object, **kwargs: object) -> object:
        """Execute strategy."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"
