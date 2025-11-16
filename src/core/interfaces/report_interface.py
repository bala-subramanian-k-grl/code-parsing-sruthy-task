"""Report generator interface."""

from abc import ABC, abstractmethod
from pathlib import Path

from src.core.config.models import ParserResult


class IReportGenerator(ABC):
    """Interface for all report generators."""

    @abstractmethod
    def generate(self, result: ParserResult, path: Path) -> None:
        """Generate report from parser result."""
