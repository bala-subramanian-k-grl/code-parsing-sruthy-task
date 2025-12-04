"""Extractor interface definition."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ExtractorInterface(ABC):
    """Abstract interface for all extractors."""

    # ---------------- Encapsulation + Polymorphism ----------------

    @property
    @abstractmethod
    def extractor_type(self) -> str:
        """Polymorphic extractor type identifier."""
        raise NotImplementedError

    # ---------------- Required Abstract Method ---------------------

    @abstractmethod
    def extract(self, data: Any) -> Any:
        """Extract data from the source."""
        raise NotImplementedError

    # ---------------- Polymorphic Helper ---------------------------

    def extractor_name(self) -> str:
        """Return extractor class name."""
        return self.__class__.__name__

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.extractor_type}Extractor"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __len__(self) -> int:
        """Method implementation."""
        return 1

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, ExtractorInterface):
            return NotImplemented
        return self.extractor_type < other.extractor_type

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in self.extractor_type

    def __int__(self) -> int:
        """Method implementation."""
        return 1

    def __float__(self) -> float:
        """Method implementation."""
        return 1.0

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return self.extractor_type[index]
