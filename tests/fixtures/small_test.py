# USB PD Specification Parser - Small Test Fixtures
"""Small test fixtures for USB PD Specification Parser."""

from abc import ABC, abstractmethod
from typing import Any


class BaseFixture(ABC):  # Abstraction
    """Abstract test fixture (Abstraction, Encapsulation)."""

    def __init__(self, name: str):
        self._name = name  # Encapsulation
        self._data: dict[str, Any] = {}  # Encapsulation

    @abstractmethod  # Abstraction
    def generate_data(self) -> dict[str, Any]:
        pass

    @property  # Encapsulation
    def name(self) -> str:
        return self._name


class MockTOCFixture(BaseFixture):  # Inheritance
    """Mock TOC fixture (Inheritance, Polymorphism)."""

    def generate_data(self) -> dict[str, Any]:  # Polymorphism
        return {
            "toc_entries": [
                {"section_id": "1", "title": "Introduction", "page": 1},
                {"section_id": "2", "title": "Overview", "page": 5},
                {"section_id": "3", "title": "Details", "page": 10},
            ],
            "total_entries": 3,
        }


class MockContentFixture(BaseFixture):  # Inheritance
    """Mock content fixture (Inheritance, Polymorphism)."""

    def generate_data(self) -> dict[str, Any]:  # Polymorphism
        return {
            "content_items": [
                {"type": "paragraph", "content": "Test paragraph 1", "page": 1},
                {"type": "paragraph", "content": "Test paragraph 2", "page": 2},
                {"type": "image", "content": "[Image 100x50]", "page": 3},
            ],
            "total_items": 3,
        }


class FixtureFactory:  # Abstraction
    """Fixture factory (Abstraction, Encapsulation)."""

    @staticmethod  # Encapsulation
    def create_fixture(fixture_type: str) -> BaseFixture:
        if fixture_type == "toc":
            return MockTOCFixture("Mock TOC")  # Polymorphism
        elif fixture_type == "content":
            return MockContentFixture("Mock Content")  # Polymorphism
        else:
            return MockTOCFixture("Default")  # Default


# Test data generators
def get_small_toc_data() -> list[dict[str, Any]]:
    """Generate small TOC test data."""
    fixture = FixtureFactory.create_fixture("toc")
    return fixture.generate_data()["toc_entries"]


def get_small_content_data() -> list[dict[str, Any]]:
    """Generate small content test data."""
    fixture = FixtureFactory.create_fixture("content")
    return fixture.generate_data()["content_items"]


def get_test_config() -> dict[str, Any]:
    """Generate test configuration."""
    return {
        "pdf_input_file": "test.pdf",
        "output_directory": "test_outputs",
        "max_pages": 10,
    }
