"""Abstract writer interface with improved OOP structure."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable


class WriterInterface(ABC):
    """Abstract interface for all file writers."""

    @abstractmethod
    def write(self, data: Iterable[Any], path: Path) -> None:
        """
        Write multiple items to the specified path.
        """
        raise NotImplementedError


    def write_single(self, item: Any, path: Path) -> None:
        """
        Default implementation: write a single item.
        Writers may override for optimization.
        """
        self.write([item], path)

    def prepare_path(self, path: Path) -> Path:
        """
        Prepare filesystem path — ensures the parent folder exists.
        This method supports polymorphic overrides in subclasses.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
