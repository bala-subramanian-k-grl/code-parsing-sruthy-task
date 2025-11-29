"""Shared decorators for CLI module."""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar('T')


def protected_access(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to mark protected/internal methods."""
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
        return func(self, *args, **kwargs)
    return wrapper
