"""Base PDF extractor module."""
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractor(ABC):  # Abstraction
    """Abstract PDF extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path) -> None:
        self._pdf_path = pdf_path  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    @abstractmethod  # Abstraction
    def extract(self) -> Any:
        """Extract content from PDF."""
        pass

    def _get_fitz(self) -> Any:  # Encapsulation
        """Get fitz module."""
        import fitz

        return fitz
