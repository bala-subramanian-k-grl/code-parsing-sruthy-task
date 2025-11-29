"""File utilities for testing with full OOP design.

"""

from __future__ import annotations

import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List

# ============================================================
# Logger (Composition)
# ============================================================


class BaseFileLogger(ABC):
    """Abstract base logger."""

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError


class FileManagerLogger(BaseFileLogger):
    """Logger used by file managers via composition."""

    def __init__(self) -> None:
        self.__log_count = 0

    def log(self, message: str) -> None:
        self.__log_count += 1
        print(f"[FILE MANAGER LOG] {message}")

    def __str__(self) -> str:
        return f"FileManagerLogger(logs={self.__log_count})"

    def __len__(self) -> int:
        return self.__log_count

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "FileManagerLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FileManagerLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ============================================================
# Abstract Base Class (Abstraction + Encapsulation)
# ============================================================


class BaseFileManager(ABC):
    """Abstract base class for file managers.

    Provides:
    - Encapsulated tracking of created files
    - Encapsulated error list
    - Composition-based logging
    - Context manager protocol for automatic cleanup
    """

    def __init__(self, logger: FileManagerLogger | None = None) -> None:
        self._logger: FileManagerLogger = logger or FileManagerLogger()
        self._files: List[Path] = []    # Encapsulation
        self._errors: List[str] = []    # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    # --------------- Abstract Behavior ----------------

    @abstractmethod
    def create_temp_file(self, *args: Any, **kwargs: Any) -> Path:
        """Create a temporary file and register it for cleanup."""
        raise NotImplementedError

    @abstractmethod
    def _delete_file(self, path: Path) -> None:
        """Delete a single file (polymorphic in subclasses)."""
        raise NotImplementedError

    # --------------- Shared Behavior ------------------

    def _register_file(self, path: Path) -> None:
        """Register a file to be tracked for cleanup."""
        self._logger.log(f"Registering temp file: {path}")
        self._files.append(path)

    def cleanup(self) -> None:
        """Delete all tracked temporary files."""
        self._logger.log("Starting cleanup of temporary files...")
        for f in list(self._files):
            if f.exists():
                try:
                    self._delete_file(f)
                    self._logger.log(f"Deleted temp file: {f}")
                except OSError as e:
                    msg = f"Warning: Could not delete {f}: {e}"
                    self._logger.log(msg)
                    self._errors.append(msg)
                except Exception as e:
                    msg = f"Unexpected error deleting {f}: {e}"
                    self._logger.log(msg)
                    self._errors.append(msg)
        self._files.clear()
        self._logger.log("Cleanup complete.")

    # --------------- Context Manager ------------------

    def __enter__(self) -> BaseFileManager:
        """Context manager entry."""
        self._logger.log(f"Entering context for {self.__class__.__name__}")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - always perform cleanup."""
        if exc_type:
            self._logger.log(
                f"Context exited with exception: "
                f"{exc_type.__name__}: {exc_val}"
            )
        self.cleanup()

    # --------------- Introspection Helpers ------------

    @property
    def files(self) -> List[Path]:
        """Get list of tracked files (read-only usage)."""
        return list(self._files)

    @property
    def errors(self) -> List[str]:
        """Get list of errors encountered during cleanup."""
        return list(self._errors)

    def __str__(self) -> str:
        return "BaseFileManager()"

    def __repr__(self) -> str:
        return "BaseFileManager()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseFileManager)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Concrete Implementation (Inheritance + Polymorphism)
# ============================================================


class TempFileManager(BaseFileManager):
    """Manage temporary test files.

    This class preserves the original API:
    - create_temp_file(...)
    - cleanup()
    - usable as a context manager

    But now benefits from:
    - BaseFileManager abstraction
    - Encapsulated state
    - Composition-based logging
    """

    def create_temp_file(
        self,
        content: str = "",
        suffix: str = ".txt",
        encoding: str = "utf-8",
    ) -> Path:
        """Create a temporary file and register it for cleanup."""
        self._logger.log(f"Creating temp file with suffix '{suffix}'")
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        temp_path = Path(path)

        if content:
            self._logger.log(
                f"Writing initial content to temp file: {temp_path}"
            )
            temp_path.write_text(content, encoding=encoding)

        self._register_file(temp_path)
        return temp_path

    def _delete_file(self, path: Path) -> None:
        """Delete a single file (polymorphic implementation)."""
        path.unlink()

    def __str__(self) -> str:
        return "TempFileManager()"

    def __repr__(self) -> str:
        return "TempFileManager()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TempFileManager)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
