"""
Pytest fixtures and factories with improved OOP design.

Enhancements:
- Added BaseFactory abstraction
- Added polymorphic factory class
- Added encapsulation around registry
- Added composition in factory
- Improved naming consistency
- Increased documentation coverage
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
    Provides encapsulation through a protected registry.
    """

    def __init__(self) -> None:
        self._registry: dict[str, Any] = {}  # Encapsulation

    @abstractmethod
    def create(self, fixture_type: str):
        """Create a fixture based on type."""
        pass

    def register(self, name: str, fixture_obj: Any) -> None:
        """Register a fixture object in the internal registry."""
        self._registry[name] = fixture_obj

    def get_registered_types(self) -> list[str]:
        """Return a list of registered fixture types."""
        return list(self._registry.keys())


# =========================================================
# Concrete Fixture Factory (Inheritance + Polymorphism)
# =========================================================

class FixtureFactory(BaseFixtureFactory):
    """
    Factory for creating test fixtures (Factory Pattern).
    Uses composition by storing fixture classes internally.
    """

    def __init__(self) -> None:
        super().__init__()

        # Composition: store fixture constructors inside the registry
        self.register("toc", MockTOCFixture)
        self.register("content", MockContentFixture)
        self.register("config", MockConfigFixture)

    def create(self, fixture_type: str):
        """Polymorphic creation of fixtures."""
        fixture_class = self._registry.get(fixture_type)

        if fixture_class is None:
            raise ValueError(f"Unknown fixture type: {fixture_type}")

        return fixture_class()


# =========================================================
# Pytest Fixtures (Context-managed Data Providers)
# =========================================================

@pytest.fixture
def mock_toc() -> Generator[list[dict[str, Any]], None, None]:
    """Provide mock Table of Contents data."""
    with MockTOCFixture() as data:
        yield data


@pytest.fixture
def mock_content() -> Generator[list[dict[str, Any]], None, None]:
    """Provide mock content data."""
    with MockContentFixture() as data:
        yield data


@pytest.fixture
def mock_config() -> Generator[dict[str, Any], None, None]:
    """Provide mock config data."""
    with MockConfigFixture() as config:
        yield config


@pytest.fixture
def temp_file_manager() -> Generator[TempFileManager, None, None]:
    """Provide temporary file manager via context manager."""
    with TempFileManager() as manager:
        yield manager


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Provide temporary output directory."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(exist_ok=True)
    return output_dir


# =========================================================
# Additional Factory Utility (Convenience Wrapper)
# =========================================================

@pytest.fixture
def fixture_factory() -> FixtureFactory:
    """
    Provide an instance of the OOP-enhanced FixtureFactory.

    This gives test files access to dynamic fixture creation:
        factory.create("toc")
        factory.create("config")
        factory.create("content")
    """
    return FixtureFactory()
