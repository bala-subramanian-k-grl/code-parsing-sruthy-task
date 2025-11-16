"""Pipeline interface definition."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.config.models import ParserResult


@dataclass
class ValidationResult:
    """Result of pipeline validation."""

    is_valid: bool
    errors: list[str]


class PipelineInterface(ABC):
    """Abstract interface for processing pipelines."""

    @abstractmethod
    def execute(self) -> ParserResult:
        """Execute pipeline and return result."""

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate pipeline configuration."""
