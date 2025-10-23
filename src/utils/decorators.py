"""Useful decorators for enhancing functionality."""

import functools
import logging
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def log_execution(func: F) -> F:
    """Decorator to log function execution."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)
        logger.info("Executing %s", func.__name__)
        try:
            result = func(*args, **kwargs)
            logger.info("Completed %s successfully", func.__name__)
            return result
        except Exception as e:
            logger.error("Error in %s: %s", func.__name__, e)
            raise

    return wrapper  # type: ignore


def timing(func: F) -> F:
    """Decorator to measure execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger = logging.getLogger(func.__module__)
        duration = end_time - start_time
        msg = f"{func.__name__} took {duration:.2f} seconds"
        logger.info(msg)
        return result

    return wrapper  # type: ignore


def validate_path(func: F) -> F:
    """Decorator to validate path arguments."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from pathlib import Path

        # Validate first Path argument if exists
        if args and isinstance(args[0], Path):
            if not args[0].exists():
                msg = f"Path not found: {args[0]}"
                raise FileNotFoundError(msg)
        return func(*args, **kwargs)

    return wrapper  # type: ignore


def retry(max_attempts: int = 3) -> Callable[[F], F]:
    """Decorator to retry function on failure."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__module__)
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        msg = (
                            f"{func.__name__} failed after "
                            f"{max_attempts} attempts"
                        )
                        logger.error(msg)
                        raise
                    msg = f"{func.__name__} attempt {attempt + 1} failed: {e}"
                    logger.warning(msg)
            return None

        return wrapper  # type: ignore

    return decorator
