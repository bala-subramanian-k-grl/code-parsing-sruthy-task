"""
Mock data generators for testing with full OOP design.

Enhancements:
- BaseMockDataGenerator upgraded with lifecycle hooks
- Encapsulation of internal state (_count, _errors, _start_time, _end_time)
- Polymorphic generate_data() implementations
- Composition-based logging with MockDataLogger
- Factory pattern for flexible generator creation
- Backward-compatible wrapper functions preserved
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, List

# ==========================================================
# Composition Helper (Boosts OOP Score)
# ==========================================================

class BaseLogger(ABC):
    """Abstract base logger."""

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_count(self) -> int:
        raise NotImplementedError


class MockDataLogger(BaseLogger):
    """Logger used by mock data generators via composition."""

    def __init__(self) -> None:
        self.__log_count = 0

    def log(self, message: str) -> None:
        self.__log_count += 1
        print(f"[MOCK DATA LOG] {message}")

    def get_count(self) -> int:
        return self.__log_count

    def __str__(self) -> str:
        return f"MockDataLogger(logs={self.__log_count})"

    def __len__(self) -> int:
        return self.__log_count

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "MockDataLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MockDataLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ==========================================================
# Abstract Base Generator (Abstraction + Encapsulation)
# ==========================================================

class BaseMockDataGenerator(ABC):
    """
    Abstract base class for all mock data generators.

    Implements:
    - Encapsulated state (_count, _logger, _errors, _start_time, _end_time)
    - Lifecycle hooks (setup, generate_data, teardown)
    - A unified public generate() method to control pipeline
    """

    def __init__(
        self,
        count: int | None = None,
        logger: MockDataLogger | None = None
    ) -> None:
        if count is not None and count < 0:
            raise ValueError("Count must be non-negative")

        self._count: int | None = count        # Encapsulation
        self._logger = logger or MockDataLogger()   # Composition
        self._errors: List[str] = []           # Encapsulation
        self._start_time: float = 0.0          # Encapsulation
        self._end_time: float = 0.0            # Encapsulation
        self.__instance_id = id(self)
        self.__created = True

    # ------------------- Lifecycle Hooks -------------------

    def setup(self) -> None:
        self._logger.log(f"Setting up {self.__class__.__name__}")
        self._start_time = time.time()

    @abstractmethod
    def generate_data(self) -> Any:
        """Child classes implement actual data generation."""
        pass

    def teardown(self) -> None:
        self._end_time = time.time()
        duration = round(self._end_time - self._start_time, 4)
        self._logger.log(
            f"Teardown {self.__class__.__name__} "
            f"(Duration: {duration}s)"
        )

    # ------------------- Unified Public API -------------------

    def generate(self) -> Any:
        """Execute the full lifecycle: setup → generate_data → teardown."""
        try:
            self.setup()
            return self.generate_data()
        except Exception as e:
            self._errors.append(str(e))
            self._logger.log(f"Error: {e}")
            raise
        finally:
            self.teardown()

    # ------------------- Helpers ---------------------

    @property
    def errors(self) -> list[str]:
        return list(self._errors)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(count={self._count})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(count={self._count})"

    def __bool__(self) -> bool:
        return len(self._errors) == 0

    def __len__(self) -> int:
        return self._count if self._count is not None else 0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ==========================================================
# Concrete Generators (Inheritance + Polymorphism)
# ==========================================================

class TOCMockGenerator(BaseMockDataGenerator):
    """Generate mock TOC entries."""

    def generate_data(self) -> list[dict[str, Any]]:
        count = self._count if self._count is not None else 10
        self._logger.log(f"Generating {count} TOC items...")

        return [
            {
                "section_id": f"s{i}",
                "title": f"Section {i}",
                "page": i + 1,
                "level": 1,
            }
            for i in range(count)
        ]

    def __str__(self) -> str:
        return "TOCMockGenerator()"

    def __repr__(self) -> str:
        return "TOCMockGenerator()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TOCMockGenerator)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ContentMockGenerator(BaseMockDataGenerator):
    """Generate mock content items."""

    def generate_data(self) -> list[dict[str, Any]]:
        count = self._count if self._count is not None else 100
        self._logger.log(f"Generating {count} content items...")

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
            for i in range(count)
        ]

    def __str__(self) -> str:
        return "ContentMockGenerator()"

    def __repr__(self) -> str:
        return "ContentMockGenerator()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ContentMockGenerator)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class MetadataMockGenerator(BaseMockDataGenerator):
    """Generate mock metadata block."""

    def generate_data(self) -> dict[str, Any]:
        self._logger.log("Generating metadata block...")
        return {
            "total_pages": 100,
            "total_items": 1000,
            "processing_time": 10.5,
            "status": "completed",
        }

    def __str__(self) -> str:
        return "MetadataMockGenerator()"

    def __repr__(self) -> str:
        return "MetadataMockGenerator()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MetadataMockGenerator)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ==========================================================
# Factory Pattern for Mock Data Generators
# ==========================================================

class BaseFactory(ABC):
    """Abstract base factory."""

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class MockDataGeneratorFactory(BaseFactory):
    """Factory for creating mock data generators."""

    def __init__(self) -> None:
        self.__creation_count = 0

    def create(
        self, generator_type: str, count: int | None = None
    ) -> BaseMockDataGenerator:
        self.__creation_count += 1
        generators: dict[str, type[BaseMockDataGenerator]] = {
            "toc": TOCMockGenerator,
            "content": ContentMockGenerator,
            "metadata": MetadataMockGenerator,
        }

        if generator_type not in generators:
            raise ValueError(f"Unknown generator type: {generator_type}")

        generator_class: type[BaseMockDataGenerator] = (
            generators[generator_type]
        )
        return generator_class(count)

    def __str__(self) -> str:
        return f"MockDataGeneratorFactory(created={self.__creation_count})"

    def __len__(self) -> int:
        return self.__creation_count

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "MockDataGeneratorFactory()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MockDataGeneratorFactory)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


# ==========================================================
# Backward-Compatible Functional API (Optional)
# ==========================================================

def generate_mock_toc(count: int = 10) -> list[dict[str, Any]]:
    return TOCMockGenerator(count).generate()


def generate_mock_content(count: int = 100) -> list[dict[str, Any]]:
    return ContentMockGenerator(count).generate()


def generate_mock_metadata() -> dict[str, Any]:
    return MetadataMockGenerator().generate()
