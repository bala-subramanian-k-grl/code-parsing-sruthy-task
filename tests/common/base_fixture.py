"""Base fixture abstraction with improved OOP structure."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseFixture(ABC):
    """
    Abstract base class for test fixtures with context manager support.

    Usage:
        class MyFixture(BaseFixture):
            def setup(self):
                ...

            def teardown(self):
                ...

        with MyFixture() as fx:
            # setup executed automatically
            ...

        # teardown executed automatically
    """

    def __init__(self) -> None:
        self._is_active: bool = False
        self.__instance_id = id(self)
        self.__created = True

    @abstractmethod
    def setup(self) -> None:
        """Setup fixture resources."""

    @abstractmethod
    def teardown(self) -> None:
        """Teardown fixture resources."""

    def _on_setup_error(self, error: Exception) -> None:
        """Hook for logging setup failures."""
        print(f"[Fixture Setup Error] {error}")

    def _on_teardown_error(self, error: Exception) -> None:
        """Hook for logging teardown failures."""
        print(f"[Fixture Teardown Warning] {error}")

    def __enter__(self) -> BaseFixture:
        """Context entry: calls setup()."""
        try:
            self.setup()
            self._is_active = True
        except Exception as e:
            self._on_setup_error(e)
            raise
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: Any | None
    ) -> None:
        """
        Context exit: safely executes teardown().
        """
        try:
            self.teardown()
        except Exception as e:
            # Teardown failed
            self._on_teardown_error(e)

            # If no original exception, raise the teardown error
            if exc_type is None:
                raise

        self._is_active = False

    @property
    def is_active(self) -> bool:
        """Return True if fixture is currently active inside a context."""
        return self._is_active

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(active={self._is_active})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> bool:
        return self._is_active

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)
