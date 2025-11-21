"""Test mixins for cleanup and timing operations."""

import time
from pathlib import Path
from typing import Any, Callable, TypeVar

type_var_t = TypeVar("type_var_t")


class CleanupMixin:
    """Mixin for cleanup operations in tests."""

    def cleanup_files(self, files: list[Path]) -> None:
        """Clean up test files with error handling.

        Args:
            files: List of file paths to delete
        """
        for f in files:
            if f.exists():
                try:
                    f.unlink()
                except (OSError) as e:
                    print(f"Warning: Could not delete {f}: {e}")


class TimerMixin:
    """Mixin for timing operations in tests."""

    def time_operation(
        self, func: Callable[..., type_var_t], *args: Any, **kwargs: Any
    ) -> tuple[type_var_t, float]:
        """Time a function execution and return result with elapsed time.

        Args:
            func: Function to time
            *args: Positional arguments passed to func
            **kwargs: Keyword arguments passed to func

        Returns:
            Tuple of (function result, elapsed time in seconds)
        """
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            return result, elapsed
        except Exception as e:
            elapsed = time.time() - start
            print(f"Function failed after {elapsed:.2f}s: {e}")
            raise
