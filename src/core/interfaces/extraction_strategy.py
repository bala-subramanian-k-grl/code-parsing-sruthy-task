"""Extraction strategy interface."""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class Document(Protocol):
    """Protocol defining document interface."""

    def __len__(self) -> int:
        """Return number of pages."""
        ...


class ExtractionStrategy(ABC):
    """Abstract strategy for content extraction."""

    @abstractmethod
    def extract(self, document: Document) -> list[dict[str, Any]]:
        """Extract content using specific strategy."""

    @abstractmethod
    def supports(self, mode: str) -> bool:
        """Check if strategy supports given mode."""
