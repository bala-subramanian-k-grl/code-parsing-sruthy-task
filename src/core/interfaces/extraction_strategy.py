"""
Enterprise extraction strategy interface (Strategy Pattern).

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Protocol

from src.core.config.constants import ParserMode


class Document(Protocol):
    """Protocol defining the required structure of a document."""

    def __len__(self) -> int:
        """Return number of pages in the document."""
        ...

    def __getitem__(self, index: int) -> Any:
        """Return a specific page by index."""
        ...


class ExtractionStrategy(ABC):
    """Abstract Strategy for content extraction."""


    @abstractmethod
    def extract(self, document: Document) -> list[dict[str, Any]]:
        """
        Extract content from the document.

        Every strategy has a different algorithm.
        This is where polymorphism happens.
        """
        raise NotImplementedError

    @abstractmethod
    def supports(self, mode: ParserMode) -> bool:
        """
        Check if the strategy supports the given parser mode.

        Example:
            return mode == ParserMode.TOC
        """
        raise NotImplementedError

    @abstractmethod
    def strategy_name(self) -> str:
        """
        Human-readable strategy name.

        Example:
            return "TOCExtractionStrategy"
        """
        raise NotImplementedError


    def validate_strategy(self) -> None:
        """
        Optional validation method.

        Subclasses may override to validate internal state or config.
        """
        pass

    def priority(self) -> int:
        """
        Optional priority system.
        Higher value = higher priority strategy.

        Useful if multiple strategies support same ParserMode.
        """
        return 10
