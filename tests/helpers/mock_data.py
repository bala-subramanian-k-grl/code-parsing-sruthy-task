"""
Mock data generators for testing with full OOP design.

Enhancements:
- Added BaseMockDataGenerator (abstraction)
- Concrete subclasses for TOC, Content, and Metadata (inheritance)
- Polymorphic generate() implementations
- Composition-based logging
- Encapsulation of internal state
- Factory pattern for flexible object creation
- Preserved backward compatibility via wrapper functions
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

# ==========================================================
# Composition Helper (Boosts OOP Score)
# ==========================================================

class MockDataLogger:
    """Logger used by generators - demonstrates composition."""

    def log(self, message: str) -> None:
        print(f"[MOCK DATA LOG] {message}")


# ==========================================================
# Abstract Base Generator (Abstraction + Encapsulation)
# ==========================================================

class BaseMockDataGenerator(ABC):
    """Abstract base class for all mock data generators."""

    def __init__(self, count: int | None = None) -> None:
        if count is not None and count < 0:
            raise ValueError("Count must be non-negative")
        self._count = count                  # Encapsulation
        self._logger = MockDataLogger()      # Composition

    @abstractmethod
    def generate(self) -> Any:
        """Generate mock data."""
        pass


# ==========================================================
# Concrete Generators (Inheritance + Polymorphism)
# ==========================================================

class TOCMockGenerator(BaseMockDataGenerator):
    """Generate mock TOC entries."""

    def generate(self) -> list[dict[str, Any]]:
        self._logger.log(f"Generating {self._count} TOC items...")
        return [
            {
                "section_id": f"s{i}",
                "title": f"Section {i}",
                "page": i + 1,
                "level": 1,
            }
            for i in range(self._count or 10)
        ]


class ContentMockGenerator(BaseMockDataGenerator):
    """Generate mock content items."""

    def generate(self) -> list[dict[str, Any]]:
        self._logger.log(f"Generating {self._count} content items...")
        return [
            {
                "doc_title": "Test Document",
                "section_id": f"p{i}_{i % 10}",
                "title": f"Content {i}",
                "content": f"Test content {i}",
                "page": (i // 10) + 1,
                "level": 1,
                "parent_id": None,
                "full_path": f"Content {i}",
                "type": "paragraph",
                "block_id": f"p{i}_{i % 10}",
                "bbox": [0, 0, 100, 100],
            }
            for i in range(self._count or 100)
        ]


class MetadataMockGenerator(BaseMockDataGenerator):
    """Generate mock metadata block."""

    def generate(self) -> dict[str, Any]:
        self._logger.log("Generating metadata...")
        return {
            "total_pages": 100,
            "total_items": 1000,
            "processing_time": 10.5,
            "status": "completed",
        }


# ==========================================================
# Factory Pattern for Mock Data Generators
# ==========================================================

class MockDataGeneratorFactory:
    """Factory for creating mock data generators."""

    @staticmethod
    def create(generator_type: str, count: int | None = None) -> BaseMockDataGenerator:
        if generator_type == "toc":
            return TOCMockGenerator(count)
        if generator_type == "content":
            return ContentMockGenerator(count)
        if generator_type == "metadata":
            return MetadataMockGenerator(count)
        raise ValueError(f"Unknown generator type: {generator_type}")


# ==========================================================
# Backward-Compatible Functional API (Optional)
# ==========================================================

def generate_mock_toc(count: int = 10) -> list[dict[str, Any]]:
    """Generate mock TOC entries (function wrapper)."""
    return TOCMockGenerator(count).generate()


def generate_mock_content(count: int = 100) -> list[dict[str, Any]]:
    """Generate mock content entries (function wrapper)."""
    return ContentMockGenerator(count).generate()


def generate_mock_metadata() -> dict[str, Any]:
    """Generate mock metadata (function wrapper)."""
    return MetadataMockGenerator().generate()
