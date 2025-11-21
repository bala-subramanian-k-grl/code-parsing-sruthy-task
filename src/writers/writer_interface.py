"""Abstract writer interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class WriterInterface(ABC):
    """Abstract interface for file writers."""

    @abstractmethod
    def write(self, data: Any, path: Path) -> None:
        """Write data to file at specified path."""
