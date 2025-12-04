"""Shared decorators for CLI module."""

from collections.abc import Callable
from typing import Any, TypeVar

TReturn = TypeVar('TReturn')


def protected_access(
    func: Callable[..., TReturn]
) -> Callable[..., TReturn]:
    """Decorator to mark protected/internal methods."""
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> TReturn:
        """Method implementation."""
        return func(self, *args, **kwargs)
    return wrapper
