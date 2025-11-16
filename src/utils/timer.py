"""Execution timer."""

import time
from functools import wraps
from typing import Any, Callable

from src.utils.logger import logger


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to measure execution time."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.info(f"Execution of '{func.__name__}' took {elapsed:.2f} sec")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"Execution of '{func.__name__}' failed after {elapsed:.2f} sec: {e}")
            raise

    return wrapper
