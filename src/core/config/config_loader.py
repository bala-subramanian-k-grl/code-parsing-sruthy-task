"""Configuration loader."""

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {"input": {}, "output": {}}


class ConfigLoader:
    """Load configuration from YAML file."""

    def __init__(self, config_path: Path = Path("application.yml")):
        """Initialize config loader with path."""
        self._config_path = config_path
        self._config = self._load()

    def _load(self) -> dict[str, Any]:
        """Load configuration from file."""
        if not self._config_path.exists():
            return self._default_config()

        try:
            with self._config_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(
                f"Malformed YAML in {self._config_path}: {e}"
            ) from e

    def _default_config(self) -> dict[str, Any]:
        """Return default configuration."""
        return DEFAULT_CONFIG

    def get_pdf_path(self) -> Path:
        """Get PDF path from config."""
        path = self._config.get("input", {}).get("pdf_path")
        if not path:
            raise ValueError(
                f"pdf_path not found in {self._config_path}"
            )
        return Path(path)

    def get_output_dir(self) -> Path:
        """Get output directory from config."""
        dir_path = self._config.get("output", {}).get("base_dir")
        if not dir_path:
            raise ValueError(
                f"base_dir not found in {self._config_path}"
            )
        return Path(dir_path)

    def get_doc_title(self) -> str:
        """Get document title from config."""
        return self._config.get("metadata", {}).get(
            "doc_title", "Document"
        )

    def get_keywords(self) -> list[str]:
        """Get keywords from config."""
        return self._config.get("metadata", {}).get("keywords", [])
