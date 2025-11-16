"""Base fixture abstraction."""

from abc import ABC, abstractmethod
from typing import Any


class BaseFixture(ABC):
    """Abstract base class for test fixtures with context manager support.
    Usage:
        with MyFixture() as fixture:
            # fixture is the fixture instance itself
            # setup() is called automatically
            ...
        # teardown() is called automatically
    """

    @abstractmethod
    def setup(self) -> None:
        """Setup fixture resources."""

    @abstractmethod
    def teardown(self) -> None:
        """Teardown fixture resources."""

    def __enter__(self) -> "BaseFixture":
        """Context manager entry - calls setup and returns fixture instance."""
        self.setup()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - calls teardown with error handling."""
        try:
            self.teardown()
        except Exception as e:
            if exc_type is None:
                raise
            # Log teardown error but preserve original exception
            print(f"Warning: Error during teardown: {e}")
