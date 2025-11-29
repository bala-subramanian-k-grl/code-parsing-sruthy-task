"""Shared decorators for CLI module."""

from collections.abc import Callable
from typing import Any, TypeVar

t_return = TypeVar('t_return')


def protected_access(
    func: Callable[..., t_return]
) -> Callable[..., t_return]:
    """Decorator to mark protected/internal methods."""
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> t_return:
        return func(self, *args, **kwargs)
    return wrapper
