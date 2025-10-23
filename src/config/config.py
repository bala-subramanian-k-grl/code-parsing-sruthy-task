"""Configuration loader with OOP principles."""

from pathlib import Path
from typing import Any, Optional

import yaml

from src.config.base_config import BaseConfig


class Config(BaseConfig):  # Inheritance
    """YAML config loader."""

    from .constants import DEFAULT_PDF_PATH

    __DEFAULT_PDF = DEFAULT_PDF_PATH  # Private class attribute

    def __init__(self, config_path: str):
        super().__init__(config_path)

    def __str__(self) -> str:  # Magic Method
        pdf_name = self.pdf_input_file.name
        output_name = self.output_directory.name
        return f"Config(pdf={pdf_name}, output={output_name})"

    def __getitem__(self, key: str) -> Any:  # Magic Method
        return self.get_config_data()[key]

    def __contains__(self, key: str) -> bool:  # Magic Method
        return key in self.get_config_data()

    def load_config(self) -> dict[str, Any]:
        """Load config with defaults."""
        config_path = self.get_config_path()
        if not config_path.exists():
            return self.get_defaults()

        try:
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}") from e
        except OSError as e:
            raise ValueError(f"Cannot read config file: {e}") from e

    def get_defaults(self) -> dict[str, Any]:
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

    @property
    def config_data(self) -> dict[str, Any]:
        """Get configuration data (read-only)."""
        return self.get_config_data().copy()
