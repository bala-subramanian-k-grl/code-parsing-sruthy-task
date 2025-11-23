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
