"""
Enterprise Extraction Strategy Interface (Strategy Pattern).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol

from src.core.config.constants import ParserMode

# ==========================================================
# DOCUMENT PROTOCOL (Duck-Typed Interface)
# ==========================================================


class Document(Protocol):
    """Protocol defining the expected behavior of a document."""

    def __len__(self) -> int:
        """Return number of pages in the document."""
        ...

    def __getitem__(self, index: int) -> Any:
        """Return a specific page by index."""
        ...


# ==========================================================
# EXTRACTION STRATEGY (ABSTRACT STRATEGY PATTERN)
# ==========================================================

class ExtractionStrategy(ABC):
    """Abstract Strategy for PDF content extraction."""

    VERSION = "1.0.0"

    # ------------------------------------------------------
    # ABSTRACT POLYMORPHIC METHODS
    # ------------------------------------------------------

    @abstractmethod
    def extract(self, document: Document) -> list[dict[str, Any]]:
        """
        Extract content from the document.

        Each strategy implements its own algorithm (Polymorphism).
        """
        raise NotImplementedError

    @abstractmethod
    def supports(self, mode: ParserMode) -> bool:
        """Whether strategy supports the given parser mode."""
        raise NotImplementedError

    @abstractmethod
    def strategy_name(self) -> str:
        """Human-readable strategy name."""
        raise NotImplementedError

    @abstractmethod
    def prepare(self) -> None:
        """Prepare strategy before extraction."""
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup after extraction."""
        raise NotImplementedError

    @abstractmethod
    def can_handle(self, document: Document) -> bool:
        """Check if strategy can process the document."""
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> dict[str, Any]:
        """Return metadata describing strategy behavior."""
        raise NotImplementedError

    @abstractmethod
    def estimate_time(self, document: Document) -> float:
        """Estimate extraction time (seconds)."""
        raise NotImplementedError

    # ------------------------------------------------------
    # OPTIONAL POLYMORPHIC METHODS
    # ------------------------------------------------------

    @abstractmethod
    def validate_strategy(self) -> None:
        """Optional validation (subclasses may override)."""

    def priority(self) -> int:
        """
        Strategy priority for conflict resolution.
        Higher = preferred.
        """
        return 10

    # ------------------------------------------------------
    # INTERNAL VALIDATION (ENCAPSULATION)
    # ------------------------------------------------------

    def _ensure_document(self, document: Document) -> None:
        """Protected helper to validate document before extraction."""
        has_len = hasattr(document, "__len__")
        has_getitem = hasattr(document, "__getitem__")
        if not has_len or not has_getitem:
            raise TypeError(
                f"{self.strategy_name()} received invalid document type"
            )
        if len(document) == 0:
            raise ValueError("Document is empty; cannot extract content")

    # ------------------------------------------------------
    # DUNDER METHODS (POLYMORPHIC + READABILITY)
    # ------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.strategy_name()}Strategy"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(priority={self.priority()})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True

    def __lt__(self, other: object) -> bool:
        """Sort strategies by priority."""
        if not isinstance(other, ExtractionStrategy):
            return NotImplemented
        return self.priority() < other.priority()

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __int__(self) -> int:
        return self.priority()

    def __float__(self) -> float:
        return float(self.priority())
