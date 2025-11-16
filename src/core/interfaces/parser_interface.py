"""Parser interface definition."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class ParserInterface(ABC):
    """Abstract interface for all parsers."""

    @abstractmethod
    def parse(self, path: Path) -> Any:
        """Parse the input file and return a raw representation."""
        raise NotImplementedError
