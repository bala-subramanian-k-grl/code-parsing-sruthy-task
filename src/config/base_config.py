"""Base config"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseConfig(ABC):
    """Abstract config loader."""

    def __init__(self, config_path: str):
        self.__config_path = self._validate_path(config_path)
        self.__config: dict[str, Any] = self._load_config()

    def _validate_path(self, config_path: str) -> Path:
        """Validate config path against traversal attacks."""
        try:
            input_path = Path(config_path)
            resolved_path = input_path.resolve(strict=False)
            working_dir = Path.cwd().resolve()

            # Prevent path traversal attacks
            if not resolved_path.is_relative_to(working_dir):
                msg = f"Path traversal detected: {config_path}"
                raise ValueError(msg)
            return resolved_path
        except (OSError, ValueError) as e:
            msg = f"Invalid path: {config_path} - {e}"
            raise ValueError(msg) from e

    @abstractmethod  # Protected abstract method
    def load_config(self) -> dict[str, Any]:
        pass

    def _load_config(self) -> dict[str, Any]:
        """Load config using the abstract method."""
        return self.load_config()

    @abstractmethod  # Protected abstract method
    def get_defaults(self) -> dict[str, Any]:
        pass

    # Public interface methods
    def get_config_path(self) -> Path:
        """Public method to get config path."""
        return self.__config_path

    def get_config_data(self) -> dict[str, Any]:
        """Public method to get config data."""
        return self.__config.copy()
