"""Base PDF extractor module."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractor(ABC):  # Abstraction
    """Abstract PDF extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path) -> None:
        self._pdf_path = pdf_path  # Encapsulation
        class_name = self.__class__.__name__
        self._logger = logging.getLogger(class_name)
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
