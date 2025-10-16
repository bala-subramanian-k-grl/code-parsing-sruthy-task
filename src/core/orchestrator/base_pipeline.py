# USB PD Specification Parser - Pipeline Orchestrator Module
"""Base class for pipeline orchestrators."""

from abc import ABC, abstractmethod
from typing import Any

from src.config.config import Config


class BasePipeline(ABC):  # Abstraction
    def __init__(self, config_path: str):
        import logging

        class_name = self.__class__.__name__
        self._logger = logging.getLogger(class_name)
        try:
            self._config = Config(config_path)  # Encapsulation
            msg = f"Configuration loaded successfully from {config_path}"
            self._logger.info(msg)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        try:
            self._config.output_directory.mkdir(parents=True, exist_ok=True)
            output_dir = self._config.output_directory
            self._logger.info(f"Output directory prepared: {output_dir}")
        except OSError as e:
            raise RuntimeError(f"Cannot create output directory: {e}") from e

    @abstractmethod  # Abstraction
    def run(self, mode: int = 1) -> dict[str, Any]:
        pass
