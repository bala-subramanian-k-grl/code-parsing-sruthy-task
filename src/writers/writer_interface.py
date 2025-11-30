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
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return 1

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, WriterInterface):
            return NotImplemented
        return self.writer_type < other.writer_type

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, item: str) -> bool:
        return item in self.writer_type

    def __int__(self) -> int:
        return 1

    def __float__(self) -> float:
        return 1.0

    def __getitem__(self, index: int) -> str:
        return self.writer_type[index]
