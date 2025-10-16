# USB PD Specification Parser - Configuration Module
"""Configuration loader with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import yaml


class BaseConfig(ABC):
    """Abstract config loader (Abstraction, Encapsulation)."""

    def __init__(self, config_path: str):
        self.__config_path = self._validate_path(config_path)  # Private
        self.__config = self._load_config()  # Private

    def _validate_path(self, config_path: str) -> Path:  # Protected
        """Validate config path securely against traversal attacks."""
        try:
            input_path = Path(config_path)
            resolved_path = input_path.resolve(strict=False)
            working_dir = Path.cwd().resolve()

            # Prevent path traversal attacks
            if not resolved_path.is_relative_to(working_dir):
                raise ValueError(f"Path traversal detected: {config_path}")
            return resolved_path
        except (OSError, ValueError) as e:
            raise ValueError(f"Invalid path: {config_path} - {e}") from e

    @abstractmethod  # Protected abstract method
    def _load_config(self) -> dict[str, Any]:
        pass

    @abstractmethod  # Protected abstract method
    def _get_defaults(self) -> dict[str, Any]:
        pass

    # Public interface methods
    def get_config_path(self) -> Path:
        """Public method to get config path."""
        return self.__config_path

    def get_config_data(self) -> dict[str, Any]:
        """Public method to get config data."""
        return self.__config.copy()  # Return copy to prevent modification


class Config(BaseConfig):  # Inheritance
    """YAML config loader (Inheritance, Polymorphism)."""

    from .constants import DEFAULT_PDF_PATH

    __DEFAULT_PDF = DEFAULT_PDF_PATH  # Private class attribute

    def __str__(self) -> str:  # Magic Method
        pdf_name = self.pdf_input_file.name
        output_name = self.output_directory.name
        return f"Config(pdf={pdf_name}, output={output_name})"

    def __getitem__(self, key: str) -> Any:  # Magic Method
        return self.get_config_data()[key]

    def __contains__(self, key: str) -> bool:  # Magic Method
        return key in self.get_config_data()

    def _load_config(self) -> dict[str, Any]:  # Protected method
        """Load config with defaults (Abstraction)."""
        config_path = self.get_config_path()
        if not config_path.exists():
            return self._get_defaults()

        try:
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}") from e
        except OSError as e:
            raise ValueError(f"Cannot read config file: {e}") from e

    def _get_defaults(self) -> dict[str, Any]:  # Protected method
        """Default configuration (Abstraction)."""
        return {
            "pdf_input_file": self.__DEFAULT_PDF,
            "output_directory": "outputs",
            "max_pages": None,
        }

    @property  # Public property
    def pdf_input_file(self) -> Path:
        """Get PDF input file path."""
        try:
            config_data = self.get_config_data()
            pdf_path = config_data.get("pdf_input_file", self.__DEFAULT_PDF)
            path = Path(pdf_path)
            return self._validate_path(str(path))
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid PDF input file path: {e}") from e

    @property  # Public property
    def output_directory(self) -> Path:
        """Get output directory path."""
        config_data = self.get_config_data()
        path = Path(config_data.get("output_directory", "outputs"))
        return self._validate_path(str(path))

    @property  # Public property
    def max_pages(self) -> Optional[int]:
        """Get max pages setting."""
        return self.get_config_data().get("max_pages")

    def get(self, key: str, default: Any = None) -> Any:  # Public method
        """Get config value with default."""
        return self.get_config_data().get(key, default)
