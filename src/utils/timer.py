"""Execution timer."""

import time
from functools import wraps
from typing import Any, Callable, Optional

from src.utils.logger import Logger


class Timer:
    """Context manager for timing operations."""

    def __init__(self, name: str, logger: Optional[Logger] = None) -> None:
        self.name = name
        self.logger = logger or Logger()
        self.start_time: float = 0
        self.elapsed: float = 0

    def __enter__(self) -> "Timer":
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed = time.time() - self.start_time
        if exc_type is None:
            self.logger.info(f"'{self.name}' took {self.elapsed:.2f} sec")
        else:
            self.logger.error(
                f"'{self.name}' failed after {self.elapsed:.2f} sec: {exc_val}"
            )


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to measure execution time."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with Timer(func.__name__):
            return func(*args, **kwargs)

    return wrapper
