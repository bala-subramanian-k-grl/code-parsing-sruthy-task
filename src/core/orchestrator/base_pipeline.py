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
            self._logger.info("Configuration loaded from %s", config_path)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        try:
            output_dir = self._config.output_directory
            output_dir.mkdir(parents=True, exist_ok=True)
            self._logger.info("Output directory prepared: %s", output_dir)
        except OSError as e:
            raise RuntimeError(f"Cannot create output directory: {e}") from e

    @abstractmethod  # Abstraction
    def run(self) -> dict[str, Any]:
        pass
