"""Abstract writer interface with improved OOP structure."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable


class WriterInterface(ABC):
    """Abstract interface for all file writers."""

    @property
    @abstractmethod
    def writer_type(self) -> str:
        """Return writer type identifier."""
        raise NotImplementedError

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

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True
