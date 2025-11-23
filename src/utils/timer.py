"""Execution timer with improved OOP design."""

import time
from functools import wraps
from typing import Any, Callable, Optional

from src.utils.logger import Logger


class Timer:
    """Context manager for timing operations with extendable behaviors."""

    def __init__(self, name: str, logger: Optional[Logger] = None) -> None:
        self.name = name
        self.logger = logger or Logger()
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

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
        self.start_time = time.time()

    def stop(self) -> None:
        """Stop the timer and calculate elapsed time."""
        self.elapsed = time.time() - self.start_time

    # -------------------------------------------------------------------------
    # Polymorphic extension hooks
    # -------------------------------------------------------------------------
    def _on_success(self) -> None:
        """Hook: Called when block finishes successfully."""
        self.logger.info(f"'{self.name}' took {self.elapsed:.2f} sec")

    def _on_failure(self, error: Exception) -> None:
        """Hook: Called when block raises an exception."""
        self.logger.error(
            f"'{self.name}' failed after {self.elapsed:.2f} sec: {error}"
        )

    # -------------------------------------------------------------------------
    # Utility: convert to string
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"Timer(name='{self.name}', elapsed={self.elapsed:.2f}s)"

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
