"""
Enterprise Pipeline Interface Definition.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.config.models import ParserResult


# ==========================================================
# VALIDATION RESULT
# ==========================================================

@dataclass
class ValidationResult:
    """Result of pipeline validation."""

    is_valid: bool
    errors: list[str]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValidationResult):
            return False
        return self.is_valid == other.is_valid and self.errors == other.errors

    def __str__(self) -> str:
        status = "Valid" if self.is_valid else "Invalid"
        return f"ValidationResult(status={status}, errors={self.errors})"


# ==========================================================
# PIPELINE INTERFACE (Minimal Clean OOP)
# ==========================================================

class PipelineInterface(ABC):
    """
    Abstract interface for data processing pipelines.

    Lifecycle:
        prepare()   → setup
        validate()  → configuration check
        execute()   → run pipeline
        cleanup()   → teardown

    Added OOP:
        - pipeline_type (property)
        - is_async (property)
    """

    # -------------------- Encapsulated Properties --------------------

    @property
    @abstractmethod
    def pipeline_type(self) -> str:
        """Return pipeline type name."""
        raise NotImplementedError

    @property
    def is_async(self) -> bool:
        """Whether the pipeline runs asynchronously (default: False)."""
        return False

    # -------------------- Required Lifecycle Methods --------------------

    @abstractmethod
    def prepare(self) -> None:
        """Prepare pipeline resources before execution."""
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> ParserResult:
        """Execute pipeline and return parsed result."""
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources after execution."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate pipeline configuration."""
        raise NotImplementedError

    # -------------------- Optional Polymorphic Helper --------------------

    def get_errors(self) -> list[str]:
        """Optional error accessor (default empty)."""
        return []

    def pipeline_name(self) -> str:
        """Return pipeline identifier (polymorphic)."""
        return self.__class__.__name__
