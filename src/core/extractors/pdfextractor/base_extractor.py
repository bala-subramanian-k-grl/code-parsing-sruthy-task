"""Base PDF extractor modules."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractor(ABC):  # Abstraction
    """Abstract PDF extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path) -> None:
        self.__pdf_path = pdf_path  # Private encapsulation
        class_name = self.__class__.__name__
        self.__logger = logging.getLogger(class_name)  # Private
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    @property
    def _pdf_path(self) -> Path:  # Protected property for subclasses
        """Get PDF path for subclasses."""
        return self.__pdf_path

    @property
    def _logger(self) -> Any:  # Protected property for subclasses
        """Get logger for subclasses."""
        return self.__logger

    @abstractmethod  # Abstraction
    def extract(self) -> Any:
        """Extract content from PDF."""

    def _get_fitz(self) -> Any:  # Encapsulation
        """Get fitz module."""
        import fitz

        return fitz


class FastExtractor(BaseExtractor):  # Inheritance + Polymorphism
    """Fast extraction variant."""

    def extract(self) -> Any:  # Method override
        """Fast extraction implementation."""
        return []


class DetailedExtractor(BaseExtractor):  # Inheritance + Polymorphism
    """Detailed extraction variant."""

    def extract(self) -> Any:  # Method override
        """Detailed extraction implementation."""
        return []
