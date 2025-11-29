"""
Abstract Factory Interface for Framework-Level Object Creation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, overload

# Type variable for factory output type
t_product = TypeVar("t_product")


class FactoryInterface(ABC, Generic[t_product]):
    """Abstract base class for all factory implementations."""

    VERSION = "1.0.0"

    # ------------------------------------------------------
    # POLYMORPHIC CREATION METHODS
    # ------------------------------------------------------

    @overload
    @abstractmethod
    def create(self) -> t_product:
        """Create without parameters."""
        ...

    @overload
    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> t_product:
        """Create with flexible parameters."""
        ...

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> t_product:
        """Main abstract creation method."""
        raise NotImplementedError

    # ------------------------------------------------------
    # ENCAPSULATION (Protected Helpers)
    # ------------------------------------------------------

    def _validate_args(self, *args: Any, **kwargs: Any) -> None:
        """
        Protected method for validating creation parameters.
        Subclasses can override.
        """
        # Default: always valid (can be extended per factory)
        return

    # ------------------------------------------------------
    # INFO METHODS
    # ------------------------------------------------------

    @property
    def factory_type(self) -> str:
        """Return factory type identifier."""
        return self.__class__.__name__

    def description(self) -> str:
        """Optional descriptive text — polymorphic."""
        return f"{self.factory_type} (Factory Version {self.VERSION})"

    # ------------------------------------------------------
    # DUNDER METHODS (Polymorphism + Debugging)
    # ------------------------------------------------------

    def __str__(self) -> str:
        return self.description()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(version={self.VERSION})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        """Length may represent complexity or creation count (0 for base)."""
        return 0

    def __int__(self) -> int:
        return len(self)

    def __float__(self) -> float:
        return float(len(self))
