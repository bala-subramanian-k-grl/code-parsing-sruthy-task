"""Execution timer with improved OOP design."""

from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from src.utils.logger import Logger


class Timer:
    """Context manager for timing operations with extendable behaviors."""

    def __init__(self, name: str, logger: Logger | None = None) -> None:
        self.__name = name
        self.__logger = logger or Logger()
        self.__start_time: float = 0.0
        self.__elapsed: float = 0.0
        self.__run_count = 0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def start_time(self) -> float:
        return self.__start_time

    @property
    def elapsed(self) -> float:
        return self.__elapsed

    @property
    def run_count(self) -> int:
        return self.__run_count

    # -------------------------------------------------------------------------
    # Context manager hooks
    # -------------------------------------------------------------------------
    def __enter__(self) -> "Timer":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()
        if exc_type is None:
            self._on_success()
        else:
            self._on_failure(exc_val)

    # -------------------------------------------------------------------------
    # Encapsulated operations
    # -------------------------------------------------------------------------
    def start(self) -> None:
        """Start the timer."""
        self.__start_time = time.time()
        self.__run_count += 1

    def stop(self) -> None:
        """Stop the timer and calculate elapsed time."""
        self.__elapsed = time.time() - self.__start_time

    # -------------------------------------------------------------------------
    # Polymorphic extension hooks
    # -------------------------------------------------------------------------
    def _on_success(self) -> None:
        """Hook: Called when block finishes successfully."""
        self.__logger.info(f"'{self.__name}' took {self.__elapsed:.2f} sec")

    def _on_failure(self, error: Exception) -> None:
        """Hook: Called when block raises an exception."""
        self.__logger.error(
            f"'{self.__name}' failed after {self.__elapsed:.2f} sec: {error}"
        )

    # -------------------------------------------------------------------------
    # Utility: convert to string
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"Timer(name='{self.__name}', elapsed={self.__elapsed:.2f}s)"

    def __repr__(self) -> str:
        return f"Timer(name={self.__name!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Timer):
            return NotImplemented
        return self.__name == other.__name

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__name))

    def __len__(self) -> int:
        return self.__run_count

    def __bool__(self) -> bool:
        return self.__elapsed > 0

    def __int__(self) -> int:
        return int(self.__elapsed)

    def __float__(self) -> float:
        return self.__elapsed

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Timer):
            return NotImplemented
        return self.__elapsed < other.elapsed

    # -------------------------------------------------------------------------
    # Decorator wrapper (Polymorphic)
    # -------------------------------------------------------------------------
    @staticmethod
    def decorate(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator to measure execution time."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with Timer(func.__name__):
                return func(*args, **kwargs)

        return wrapper


# Public decorator alias
def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator alias for Timer.decorate."""
    return Timer.decorate(func)
