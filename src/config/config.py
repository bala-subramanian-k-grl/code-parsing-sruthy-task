# USB PD Specification Parser - Configuration Module
"""Configuration loader with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import yaml


class BaseConfig(ABC):
    """Abstract config loader."""

    def __init__(self, config_path: str):
        self.__config_path = self._validate_path(config_path)
        self.__config = self._load_config()

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
        return self.__config.copy()


class Config(BaseConfig):  # Inheritance
    """YAML config loader."""

    from .constants import DEFAULT_PDF_PATH

    __DEFAULT_PDF = DEFAULT_PDF_PATH
    
    def __init__(self, config_path: str):
        super().__init__(config_path)
        self.__pdf_cache = None  # Private cache
        self.__output_cache = None  # Private cache

    def __str__(self) -> str:  # Magic Method
        pdf_name = self.pdf_input_file.name
        output_name = self.output_directory.name
        return f"Config(pdf={pdf_name}, output={output_name})"

    def __getitem__(self, key: str) -> Any:  # Magic Method
        return self.get_config_data()[key]

    def __contains__(self, key: str) -> bool:  # Magic Method
        return key in self.get_config_data()

    def _load_config(self) -> dict[str, Any]:
        """Load config with defaults."""
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

    def _get_defaults(self) -> dict[str, Any]:
        """Default configuration."""
        return {
            "pdf_input_file": self.__DEFAULT_PDF,
            "output_directory": "outputs",
            "max_pages": None,
        }

    @property
    def pdf_input_file(self) -> Path:
        """Get PDF input file path."""
        try:
            config_data = self.get_config_data()
            default_pdf = self.__DEFAULT_PDF
            pdf_path = config_data.get("pdf_input_file", default_pdf)
            path = Path(pdf_path)
            return self._validate_path(str(path))
        except (ValueError, OSError) as e:
            msg = f"Invalid PDF input file path: {e}"
            raise ValueError(msg) from e

    @property
    def output_directory(self) -> Path:
        """Get output directory path."""
        config_data = self.get_config_data()
        default_dir = "outputs"
        path = Path(config_data.get("output_directory", default_dir))
        return self._validate_path(str(path))

    @property
    def max_pages(self) -> Optional[int]:
        """Get max pages setting."""
        return self.get_config_data().get("max_pages")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with default."""
        return self.get_config_data().get(key, default)
