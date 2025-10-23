"""USB PD Specification Parser - Pipeline Coordinator Module"""

import logging
from typing import Any, Optional

from src.config.config import Config
from src.core.orchestrator.base_pipeline import BasePipeline
from src.core.orchestrator.data_extractor import DataExtractor
from src.core.orchestrator.file_manager import FileManager
from src.core.orchestrator.interfaces import PipelineInterface
from src.core.orchestrator.report_manager import ReportManager
from src.utils.decorators import log_execution, timing


class PipelineCoordinator(BasePipeline, PipelineInterface):
    """Coordinates pipeline execution with proper separation of concerns."""

    def __init__(self, config_path: str):
        """Initialize pipeline coordinator with configuration."""
        if not config_path:
            raise ValueError("Config path must be a non-empty string")

        class_name = self.__class__.__name__
        self.__logger = logging.getLogger(class_name)  # Private
        try:
            self.__config = Config(config_path)  # Private
            self.__logger.info("Configuration loaded from %s", config_path)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e

        # Initialize components with dependency injection
        self.__data_extractor = DataExtractor(self.__config, self.__logger)
        self.__file_manager = FileManager(self.__config, self.__logger)
        self.__report_manager = ReportManager(self.__config, self.__logger)

    @property
    def config(self) -> Config:  # Encapsulation
        """Get configuration (read-only access)."""
        return self.__config

    @property
    def logger(self) -> Any:  # Encapsulation
        """Get logger (read-only access)."""
        return self.__logger

    def __get_max_pages(self) -> Optional[int]:  # Private method
        """Get max pages for processing."""
        return None  # Process all pages

    def __get_mode_name(self) -> str:  # Private method
        """Get mode name for logging."""
        return "Full Document Processing"

    @timing
    @log_execution
    def run(self) -> dict[str, Any]:  # Polymorphism
        """Execute the complete pipeline."""
        mode_name = self.__get_mode_name()
        self.__logger.info("Starting pipeline execution - %s", mode_name)

        max_pages = self.__get_max_pages()
        toc, content = self.__data_extractor.extract_data(max_pages)
        self.__file_manager.write_files(toc, content)
        counts = self.__report_manager.generate_reports(toc, content)

        self.__logger.info("Pipeline execution completed successfully")
        return {"toc_entries": len(toc), "spec_counts": counts}

    def run_toc_only(self) -> Any:  # Polymorphism
        """Extract TOC only."""
        return self.__data_extractor.extract_toc_only()

    def run_content_only(self) -> int:  # Polymorphism
        """Extract content only."""
        return self.__data_extractor.extract_content_only()

    def run_full_pipeline(self) -> dict[str, Any]:
        """Run full pipeline - Polymorphism."""
        return self.run()
