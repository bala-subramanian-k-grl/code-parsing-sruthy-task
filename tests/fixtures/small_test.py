"""
Small test fixtures with enhanced OOP design.

Enhancements:
- Composition through FixtureLogger inside each fixture
- Stronger encapsulation using protected attributes
- Clearer docstring coverage
- Strict adherence to BaseFixture polymorphism
"""

from __future__ import annotations

from typing import Any

from ..common.base_fixture import BaseFixture

# ================================================================
# Composition Helper (HAS-A Relationship)
# ================================================================


class FixtureLogger:
    """Simple logger to demonstrate composition within fixtures."""

    def __init__(self) -> None:
        self.__log_count = 0

    @property
    def log_count(self) -> int:
        return self.__log_count

    def log(self, message: str) -> None:
        """
        Simulate log output.
        """
        self.__log_count += 1
        print(f"[FIXTURE LOG] {message}")

    def __str__(self) -> str:
        return f"FixtureLogger(logs={self.__log_count})"

    def __len__(self) -> int:
        return self.__log_count

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "FixtureLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FixtureLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ================================================================
# Base Mock Fixture (Optional helper – improves DRY and consistency)
# ================================================================

class BaseMockFixture(BaseFixture):
    """
    Optional intermediate base class to avoid repeating logger initialization.

    Demonstrates:
    - Inheritance reuse
    - Polymorphic setup/teardown
    """

    def __init__(self) -> None:
        super().__init__()
        self.__logger = FixtureLogger()   # Composition
        self.__setup_count = 0
        self._data: Any = None

    @property
    def logger(self) -> FixtureLogger:
        return self.__logger

    @property
    def setup_count(self) -> int:
        return self.__setup_count

    @property
    def data(self) -> Any:
        return self._data

    def _log(self, msg: str) -> None:
        """Internal consistent logging helper."""
        self.__logger.log(msg)

    def _increment_setup_count(self) -> None:
        """Increment setup count."""
        self.__setup_count += 1

    def __str__(self) -> str:
        return "BaseMockFixture()"

    def __repr__(self) -> str:
        return "BaseMockFixture()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseMockFixture)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ================================================================
# Mock Fixtures (Inheritance + Polymorphism + Composition)
# ================================================================

class MockTOCFixture(BaseMockFixture):
    """Mock TOC data fixture."""

    def setup(self) -> None:
        """Setup mock TOC entries."""
        self._increment_setup_count()
        self._log("Setting up TOC fixture...")
        self._data = [
            {"section_id": "s1", "title": "Section 1", "page": 1, "level": 1},
            {"section_id": "s2", "title": "Section 2", "page": 2, "level": 1},
            {"section_id": "s3", "title": "Section 3", "page": 3, "level": 2},
        ]

    def teardown(self) -> None:
        """Clean up TOC fixture."""
        self._log("Tearing down TOC fixture...")

    def __str__(self) -> str:
        return "MockTOCFixture()"

    def __repr__(self) -> str:
        return "MockTOCFixture()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MockTOCFixture)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class MockContentFixture(BaseMockFixture):
    """Mock content data fixture."""

    def setup(self) -> None:
        """Setup mock content entries."""
        self._increment_setup_count()
        self._log("Setting up content fixture...")
        self._data = [
            {
                "doc_title": "Test Doc",
                "section_id": "p1_0",
                "title": "Content 1",
                "content": "Test content 1",
                "page": 1,
                "level": 1,
                "parent_id": None,
                "full_path": "Content 1",
                "type": "paragraph",
                "block_id": "p1_0",
                "bbox": [0, 0, 100, 100],
            }
        ]

    def teardown(self) -> None:
        """Clean up content fixture."""
        self._log("Tearing down content fixture...")

    def __str__(self) -> str:
        return "MockContentFixture()"

    def __repr__(self) -> str:
        return "MockContentFixture()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MockContentFixture)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class MockConfigFixture(BaseMockFixture):
    """Mock configuration fixture."""

    def setup(self) -> None:
        """Setup mock configuration data."""
        self._increment_setup_count()
        self._log("Setting up config fixture...")
        self._data = {
            "pdf_path": "test.pdf",
            "output_dir": "outputs",
            "max_pages": 10,
        }

    def teardown(self) -> None:
        """Clean up configuration fixture."""
        self._log("Tearing down config fixture...")

    def __str__(self) -> str:
        return "MockConfigFixture()"

    def __repr__(self) -> str:
        return "MockConfigFixture()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MockConfigFixture)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
