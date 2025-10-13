# USB PD Specification Parser - Pipeline Orchestrator Module
"""Simple pipeline orchestrator with OOP principles."""

from abc import ABC, abstractmethod
from typing import Any

from src.config.config import Config


class BasePipeline(ABC):  # Abstraction
    def __init__(self, config_path: str):
        import logging

        self._logger = logging.getLogger(self.__class__.__name__)
        try:
            self._config = Config(config_path)  # Encapsulation
            self._logger.info(f"Configuration loaded successfully from {config_path}")
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        try:
            self._config.output_directory.mkdir(parents=True, exist_ok=True)
            self._logger.info(
                f"Output directory prepared: {self._config.output_directory}"
            )
        except OSError as e:
            raise RuntimeError(f"Cannot create output directory: {e}") from e

    @abstractmethod  # Abstraction
    def run(self, mode: int = 1) -> dict[str, Any]:
        pass
