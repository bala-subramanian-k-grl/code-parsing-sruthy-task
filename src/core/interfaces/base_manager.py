"""Abstract base for manager classes."""

from abc import ABC, abstractmethod


class BaseManager(ABC):
    """Abstract base for manager classes."""

    @abstractmethod
    def manage(self, *args: object, **kwargs: object) -> object:
        """Manage resources."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"
