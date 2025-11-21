"""Configuration loader."""

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {"input": {}, "output": {}}


class ConfigLoader:
    """Load configuration from YAML file."""

    def __init__(self, config_path: Path = Path("application.yml")):
        """Initialize config loader with path."""
        self.__config_path = config_path
        self.__config = self._load()

    @property
    def config_path(self) -> Path:
        """Get configuration file path."""
        return self.__config_path

    @property
    def config(self) -> dict[str, Any]:
        """Get configuration dictionary."""
        return self.__config

    @property
    def config_size(self) -> int:
        """Get config size."""
        return len(self.__config)

    @property
    def has_config(self) -> bool:
        """Check if has config."""
        return bool(self.__config)

    @property
    def path_exists(self) -> bool:
        """Check if config path exists."""
        return self.__config_path.exists()

    @property
    def path_name(self) -> str:
        """Get config path name."""
        return self.__config_path.name

    @property
    def is_empty(self) -> bool:
        """Check if config is empty."""
        return len(self.__config) == 0

    @property
    def config_keys(self) -> list[str]:
        """Get config keys."""
        return list(self.__config.keys())

    @property
    def config_values(self) -> list[Any]:
        """Get config values."""
        return list(self.__config.values())

    def _load(self) -> dict[str, Any]:
        """Load configuration from file."""
        if not self.__config_path.exists():
            return self._default_config()

        try:
            with self.__config_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(
                f"Malformed YAML in {self.__config_path}: {e}"
            ) from e

    def _default_config(self) -> dict[str, Any]:
        """Return default configuration."""
        return DEFAULT_CONFIG

    def get_pdf_path(self) -> Path:
        """Get PDF path from config."""
        path = self.__config.get("input", {}).get("pdf_path")
        if not path:
            raise ValueError(
                f"pdf_path not found in {self.__config_path}"
            )
        return Path(path)

    def get_output_dir(self) -> Path:
        """Get output directory from config."""
        dir_path = self.__config.get("output", {}).get("base_dir")
        if not dir_path:
            raise ValueError(
                f"base_dir not found in {self.__config_path}"
            )
        return Path(dir_path)

    def get_doc_title(self) -> str:
        """Get document title from config."""
        title = self.__config.get("metadata", {}).get("doc_title", "Document")
        return str(title)

    def get_keywords(self) -> list[str]:
        """Get keywords from config."""
        keywords = self.__config.get("metadata", {}).get("keywords", [])
        return [str(k) for k in keywords] if keywords else []

    def __str__(self) -> str:
        """String representation."""
        return f"ConfigLoader(path={self.__config_path})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"ConfigLoader(config_path={self.__config_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfigLoader):
            return NotImplemented
        return self.__config_path == other.__config_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__config_path))

    def __len__(self) -> int:
        return len(self.__config)

    def __bool__(self) -> bool:
        return bool(self.__config)

    def __contains__(self, key: str) -> bool:
        return key in self.__config

    def __getitem__(self, key: str) -> Any:
        return self.__config.get(key)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ConfigLoader):
            return NotImplemented
        return str(self.__config_path) < str(other.__config_path)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __iter__(self):
        """Iterate over config keys."""
        return iter(self.__config)
