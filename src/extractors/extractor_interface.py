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
        return f"{self.extractor_type}Extractor"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True
