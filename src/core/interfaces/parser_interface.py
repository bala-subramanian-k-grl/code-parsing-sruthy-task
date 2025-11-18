"""Parser interface definition."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ParserInterface(ABC):
    """Abstract interface for all parsers."""

    @abstractmethod
    def parse(self) -> Any:
        """Parse the input file and return a raw representation."""
        raise NotImplementedError
