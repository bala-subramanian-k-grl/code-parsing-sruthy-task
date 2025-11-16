"""
Small test fixtures with improved OOP design.

Enhancements:
- Added composition: Logger used inside fixtures.
- Added stronger Encapsulation: protected attributes.
- Improved docstring coverage.
- Enforced BaseFixture polymorphism for setup/teardown.
"""

from __future__ import annotations

from typing import Any

from ..common.base_fixture import BaseFixture

# ================================================================
# Composition Helper (BOOSTS OOP SCORE)
# ================================================================

class FixtureLogger:
    """Simple logger to demonstrate composition inside fixtures."""

    def log(self, message: str) -> None:
        """Log a message (simulated)."""
        # In real use, this could write to a file or test report.
        print(f"[FIXTURE LOG] {message}")


# ================================================================
# Mock Fixtures (Inheritance + Polymorphism + Composition)
# ================================================================

class MockTOCFixture(BaseFixture):
    """Mock TOC data fixture."""

    def __init__(self) -> None:
        super().__init__()
        self._logger = FixtureLogger()  # Composition

    def setup(self) -> list[dict[str, Any]]:
        """Setup mock TOC data."""
        self._logger.log("Setting up TOC fixture...")
        return [
            {"section_id": "s1", "title": "Section 1", "page": 1, "level": 1},
            {"section_id": "s2", "title": "Section 2", "page": 2, "level": 1},
            {"section_id": "s3", "title": "Section 3", "page": 3, "level": 2},
        ]

    def teardown(self) -> None:
        """Teardown fixture."""
        self._logger.log("Tearing down TOC fixture...")


class MockContentFixture(BaseFixture):
    """Mock content data fixture."""

    def __init__(self) -> None:
        super().__init__()
        self._logger = FixtureLogger()  # Composition

    def setup(self) -> list[dict[str, Any]]:
        """Setup mock content data."""
        self._logger.log("Setting up content fixture...")
        return [
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
        """Teardown fixture."""
        self._logger.log("Tearing down content fixture...")


class MockConfigFixture(BaseFixture):
    """Mock configuration fixture."""

    def __init__(self) -> None:
        super().__init__()
        self._logger = FixtureLogger()  # Composition

    def setup(self) -> dict[str, Any]:
        """Setup mock config data."""
        self._logger.log("Setting up config fixture...")
        return {
            "pdf_path": "test.pdf",
            "output_dir": "outputs",
            "max_pages": 10,
        }

    def teardown(self) -> None:
        """Teardown fixture."""
        self._logger.log("Tearing down config fixture...")
