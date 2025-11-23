"""
Parser interface definition (Enhanced with minimal OOP features).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ParserInterface(ABC):
    """Abstract interface for all parser implementations."""

    # -------------------- Encapsulated Properties --------------------

    @property
    @abstractmethod
    def parser_type(self) -> str:
        """Return parser type (encapsulation property)."""
        raise NotImplementedError

    # -------------------- Required Abstract Method --------------------

    @abstractmethod
    def parse(self) -> Any:
        """Parse the input source and return a raw representation."""
        raise NotImplementedError

    # -------------------- Minimal Optional Hook --------------------
    @property  
    def parser_name(self) -> str:
        """Return parser class name (polymorphism)."""
        return self.__class__.__name__
