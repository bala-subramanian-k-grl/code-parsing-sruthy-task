"""USB PD Specification Parser - Data Extraction Module"""

from typing import Any, Optional

from src.config.config import Config
from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor
from src.core.extractors.strategies.extraction_strategy import (
    ComprehensiveStrategy,
)
from src.core.extractors.tocextractor.toc_extractor import TOCExtractor


class DataExtractor:  # Encapsulation + Interface Implementation
    """Handles all data extraction operations."""

    def __init__(self, config: Config, logger: Any):
        """Initialize data extractor with dependencies."""
        if not config:
            raise ValueError("Config cannot be None")
        if not logger:
            raise ValueError("Logger cannot be None")

        self.__config = config  # Private
        self.__logger = logger  # Private

    def __extract_toc(self) -> list[Any]:  # Private - only used internally
        """Extract Table of Contents."""
        self.__logger.info("Extracting Table of Contents...")
        pdf_file = self.__config.pdf_input_file
        toc = TOCExtractor().extract_toc(pdf_file)
        toc_count = len(toc)
        self.__logger.info("TOC extraction completed: %s entries", toc_count)
        return toc

    def __extract_content(
        self, max_pages: Optional[int] = None
    ) -> list[Any]:  # Private - only used internally
        """Extract content using Strategy Pattern."""
        if max_pages is not None and max_pages < 1:
            raise ValueError("max_pages must be positive")

        pages_info = max_pages or "all"
        self.__logger.info("Extracting content (max pages: %s)...", pages_info)

        pdf_file = self.__config.pdf_input_file
        strategy = ComprehensiveStrategy()
        content = list(strategy.extract_pages(pdf_file, max_pages))
        count = len(content)
        self.__logger.info("Content extraction completed: %s items", count)
        return content

    def extract_data(
        self, max_pages: Optional[int]
    ) -> tuple[list[Any], list[Any]]:
        """Extract both TOC and content data."""
        toc = self.__extract_toc()
        content = self.__extract_content(max_pages)
        return toc, content

    def extract_toc_only(self) -> Any:
        """Extract TOC only for specialized operations."""
        return TOCExtractor().extract_toc(self.__config.pdf_input_file)

    def extract_content_only(self) -> int:
        """Extract content only for specialized operations."""
        extractor = PDFExtractor(self.__config.pdf_input_file)
        return len(extractor.extract_content())

    def extract(self, mode: str = "full") -> Any:  # Polymorphism
        """Extract data based on mode."""
        if mode == "toc":
            return self.extract_toc_only()
        if mode == "content":
            return self.extract_content_only()
        return self.extract_data(None)


class FastDataExtractor(DataExtractor):  # Inheritance + Polymorphism
    """Fast data extractor variant."""

    def extract(self, mode: str = "full") -> Any:  # Method override
        """Fast extraction mode."""
        self.__logger.info("Using fast extraction mode")
        return super().extract(mode)


class DetailedDataExtractor(DataExtractor):  # Inheritance + Polymorphism
    """Detailed data extractor variant."""

    def extract(self, mode: str = "full") -> Any:  # Method override
        """Detailed extraction mode."""
        self.__logger.info("Using detailed extraction mode")
        return super().extract(mode)
