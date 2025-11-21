"""Pipeline interface definition."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.config.models import ParserResult


@dataclass
class ValidationResult:
    """Result of pipeline validation."""

    is_valid: bool
    errors: list[str]

    def __eq__(self, other: object) -> bool:
        """Check equality based on validation state."""
        if not isinstance(other, ValidationResult):
            return False
        return self.is_valid == other.is_valid and self.errors == other.errors

    def __str__(self) -> str:
        """String representation."""
        status = "Valid" if self.is_valid else "Invalid"
        return f"ValidationResult(status={status}, errors={len(self.errors)})"


class PipelineInterface(ABC):
    """Abstract interface for processing pipelines."""

    @abstractmethod
    def execute(self) -> ParserResult:
        """Execute pipeline and return result."""

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate pipeline configuration."""
