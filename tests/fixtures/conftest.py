"""
Pytest fixtures and factories with improved OOP design.

Enhancements:
- BaseFactory abstraction (Abstraction)
- Polymorphic factory implementation (Polymorphism)
- Registry protection (Encapsulation)
- Factory composition storing fixture classes (Composition)
- Stable, readable fixture providers
- Consistent type hints and documentation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from ..helpers.file_utils import TempFileManager
from .small_test import MockConfigFixture, MockContentFixture, MockTOCFixture


# =========================================================
# Base Abstract Factory (Abstraction + Encapsulation)
# =========================================================

class BaseFixtureFactory(ABC):
    """
    Abstract base class for fixture factories.

    Provides:
    - protected internal registry
    - controlled registration
    - polymorphic create() method
    """

    def __init__(self) -> None:
        self.__registry: dict[str, Any] = {}  # Encapsulated registry
        self.__creation_count = 0

    @property
    def registry(self) -> dict[str, Any]:
        return dict(self.__registry)

    @property
    def creation_count(self) -> int:
        return self.__creation_count

    @abstractmethod
    def create(self, fixture_type: str) -> Any:
        """Polymorphic fixture creation."""
        raise NotImplementedError

    def register(self, name: str, fixture_obj: Any) -> None:
        """Register a fixture class inside the registry."""
        self.__registry[name] = fixture_obj

    def get_registered_types(self) -> list[str]:
        """Return available registered fixture types."""
        return list(self.__registry.keys())

    def __contains__(self, key: str) -> bool:
        """Check if a fixture type exists in registry."""
        return key in self.__registry

    def __len__(self) -> int:
        """Return number of registered fixture types."""
        return len(self.__registry)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(types={len(self)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> bool:
        return len(self.__registry) > 0


# =========================================================
# Concrete Fixture Factory (Inheritance + Polymorphism)
# =========================================================

class FixtureFactory(BaseFixtureFactory):
    """
    Factory for creating mock fixtures for pytest.

    Demonstrates:
    - inheritance from BaseFixtureFactory
    - polymorphic fixture creation
    - composition by storing fixture constructors
    """

    def __init__(self) -> None:
        super().__init__()

        # Composition: store fixture constructors inside registry
        self.register("toc", MockTOCFixture)
        self.register("content", MockContentFixture)
        self.register("config", MockConfigFixture)
        self.__instance_id = id(self)
        self.__created = True

    def create(self, fixture_type: str) -> Any:
        """Return fixture instance by type name."""
        reg = self.registry
        fixture_class = reg.get(fixture_type)

        if fixture_class is None:
            types = ', '.join(reg.keys())
            raise ValueError(
                f"Unknown fixture type: {fixture_type}. "
                f"Available types: {types}"
            )

        return fixture_class()

    def __str__(self) -> str:
        return f"FixtureFactory(registered={self.get_registered_types()})"

    def __repr__(self) -> str:
        return "FixtureFactory()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FixtureFactory)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# =========================================================
# Pytest Fixtures (Context-managed Data Providers)
# =========================================================

@pytest.fixture
def mock_toc() -> Generator[list[dict[str, Any]], None, None]:
    """Provide mock Table of Contents data through context manager."""
    fixture = MockTOCFixture()
    fixture.setup()
    yield fixture.data
    fixture.teardown()


@pytest.fixture
def mock_content() -> Generator[list[dict[str, Any]], None, None]:
    """Provide mock content data through context manager."""
    fixture = MockContentFixture()
    fixture.setup()
    yield fixture.data
    fixture.teardown()


@pytest.fixture
def mock_config() -> Generator[dict[str, Any], None, None]:
    """Provide mock config data through context manager."""
    fixture = MockConfigFixture()
    fixture.setup()
    yield fixture.data
    fixture.teardown()


@pytest.fixture
def temp_file_manager() -> Generator[TempFileManager, None, None]:
    """Provide a temporary file manager."""
    manager_instance = TempFileManager()
    with manager_instance as manager:
        yield manager  # type: ignore[misc]


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for test outputs."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(exist_ok=True)
    return output_dir


# =========================================================
# Factory Fixture (Convenience Wrapper)
# =========================================================

@pytest.fixture
def fixture_factory() -> FixtureFactory:
    """
    Provide the fixture factory.

    Usage:
        factory.create("toc")
        factory.create("content")
        factory.create("config")
    """
    return FixtureFactory()
