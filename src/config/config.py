# USB PD Specification Parser - Configuration Module
"""Configuration loader with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import yaml


class BaseConfig(ABC):  # Abstraction
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

    _DEFAULT_PDF = "assets/USB_PD_R3_2 V1.1 2024-10.pdf"  # Encapsulation

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
        try:
            path = Path(self._config.get("pdf_input_file", self._DEFAULT_PDF))
            return self._validate_path(str(path))
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid PDF input file path: {e}") from e

    @property  # Encapsulation
    def output_directory(self) -> Path:
        path = Path(self._config.get("output_directory", "outputs"))
        return self._validate_path(str(path))

    @property  # Encapsulation
    def max_pages(self) -> Optional[int]:
        return self._config.get("max_pages")

    def get(self, key: str, default: Any = None) -> Any:  # Abstraction
        return self._config.get(key, default)
