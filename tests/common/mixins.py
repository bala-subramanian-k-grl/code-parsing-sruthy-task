"""Enhanced test mixins for cleanup and timing operations."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, TypeVar

t_var = TypeVar("t_var")  # PEP8 compliant snake_case


class CleanupMixin:
    """Mixin providing safe file cleanup utilities for tests."""

    def cleanup_files(self, files: list[Path]) -> None:
        """
        Delete the given files safely.

        Args:
            files: List of file paths to delete.
        """
        for file_path in files:
            if not file_path.exists():
                continue

            try:
                file_path.unlink()
            except OSError as e:
                self._on_cleanup_warning(file_path, e)

    # -----------------------------------------
    # Hook for extensibility (OOP improvement)
    # -----------------------------------------
    def _on_cleanup_warning(
        self, file_path: Path, error: Exception
    ) -> None:
        """Hook: allow subclasses to override cleanup-error handling."""
        print(
            f"[Cleanup Warning] Could not delete {file_path}: {error}"
        )

    def __str__(self) -> str:
        return "CleanupMixin()"

    def __repr__(self) -> str:
        return "CleanupMixin()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CleanupMixin)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class TimerMixin:
    """Mixin providing execution timing utilities for tests."""

    def time_operation(
        self,
        func: Callable[..., t_var],
        *args: Any,
        **kwargs: Any
    ) -> tuple[t_var, float]:
        """
        Measure the execution time of a function.

        Returns:
            (function_result, elapsed_time_in_seconds)
        """
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            return result, elapsed

        except Exception as e:
            elapsed = time.time() - start
            self._on_timing_error(func.__name__, elapsed, e)
            raise

    # -----------------------------------------
    # Hook for extensibility (OOP improvement)
    # -----------------------------------------
    def _on_timing_error(
        self, func_name: str, elapsed: float, error: Exception
    ) -> None:
        """Hook: allow subclasses to override timing error behavior."""
        print(
            f"[Timer Error] Function '{func_name}' failed after "
            f"{elapsed:.2f}s: {error}"
        )

    def __str__(self) -> str:
        return "TimerMixin()"

    def __repr__(self) -> str:
        return "TimerMixin()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TimerMixin)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
