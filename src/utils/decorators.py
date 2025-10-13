# USB PD Specification Parser - Decorators Module
"""Useful decorators for enhancing functionality."""

import functools
import logging
import time
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


def log_execution(func: F) -> F:
    """Decorator to log function execution."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)
        logger.info(f"Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Completed {func.__name__} successfully")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
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
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
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
                raise FileNotFoundError(f"Path not found: {args[0]}")
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
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                        raise
                    logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}")
            return None
        return wrapper  # type: ignore
    return decorator