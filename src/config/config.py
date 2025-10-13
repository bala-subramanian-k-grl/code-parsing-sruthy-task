# USB PD Specification Parser - Configuration Module
"""Configuration loader with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import yaml


class BaseConfig(ABC):
    """Abstract config loader (Abstraction, Encapsulation)."""

    def __init__(self, config_path: str):
        self._config_path = self._validate_path(config_path)
        self._config = self._load_config()

    def _validate_path(self, config_path: str) -> Path:  # Encapsulation
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

    @abstractmethod  # Abstraction
    def _load_config(self) -> dict[str, Any]:
        pass

    @abstractmethod  # Abstraction
    def _get_defaults(self) -> dict[str, Any]:
        pass


class Config(BaseConfig):  # Inheritance
    """YAML config loader (Inheritance, Polymorphism)."""

    from .constants import DEFAULT_PDF_PATH

    _DEFAULT_PDF = DEFAULT_PDF_PATH

    def __str__(self) -> str:  # Magic Method
        return f"Config(pdf={self.pdf_input_file.name}, output={self.output_directory.name})"

    def __getitem__(self, key: str) -> Any:  # Magic Method
        return self._config[key]

    def __contains__(self, key: str) -> bool:  # Magic Method
        return key in self._config

    def _load_config(self) -> dict[str, Any]:  # Polymorphism
        """Load config with defaults (Abstraction)."""
        if not self._config_path.exists():
            return self._get_defaults()

        try:
            with open(self._config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}") from e
        except OSError as e:
            raise ValueError(f"Cannot read config file: {e}") from e

    def _get_defaults(self) -> dict[str, Any]:  # Polymorphism
        """Default configuration (Abstraction)."""
        return {
            "pdf_input_file": self._DEFAULT_PDF,
            "output_directory": "outputs",
            "max_pages": None,
        }

    @property  # Encapsulation
    def pdf_input_file(self) -> Path:
        """Get PDF input file path."""
        try:
            path = Path(self._config.get("pdf_input_file", self._DEFAULT_PDF))
            return self._validate_path(str(path))
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid PDF input file path: {e}") from e

    @property  # Encapsulation
    def output_directory(self) -> Path:
        """Get output directory path."""
        path = Path(self._config.get("output_directory", "outputs"))
        return self._validate_path(str(path))

    @property  # Encapsulation
    def max_pages(self) -> Optional[int]:
        """Get max pages setting."""
        return self._config.get("max_pages")

    def get(self, key: str, default: Any = None) -> Any:  # Abstraction
        """Get config value with default."""
        return self._config.get(key, default)
