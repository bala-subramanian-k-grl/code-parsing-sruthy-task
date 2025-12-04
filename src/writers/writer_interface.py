"""Abstract writer interface with improved OOP structure."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from typing import Any


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
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __len__(self) -> int:
        """Method implementation."""
        return 1

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, WriterInterface):
            return NotImplemented
        return self.writer_type < other.writer_type

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in self.writer_type

    def __int__(self) -> int:
        """Method implementation."""
        return 1

    def __float__(self) -> float:
        """Method implementation."""
        return 1.0

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return self.writer_type[index]
