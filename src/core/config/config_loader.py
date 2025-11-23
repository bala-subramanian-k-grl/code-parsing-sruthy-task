"""
Enterprise OOP Configuration Loader Module.

OOP Enhancements:
- BaseConfigLoader (Abstraction)
- YAMLConfigLoader / JSONConfigLoader / EnvConfigLoader (Inheritance)
- Polymorphic load(), source_name(), validate()
- Factory pattern for selecting loader type
- Encapsulation with protected methods
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
import json
import os


# ==========================================================
# 1. ABSTRACT BASE LOADER (Abstraction)
# ==========================================================

class BaseConfigLoader(ABC):
    """
    Abstract interface for configuration loaders.

    Enforces:
    - load()
    - get()
    - source_name()
    """

    def __init__(self, config_path: Optional[Path] = None):
        self._config_path = config_path
        self._config: Dict[str, Any] = {}

    # ------- ABSTRACT POLYMORPHIC METHODS -------
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load configuration from underlying storage."""
        raise NotImplementedError

    @abstractmethod
    def source_name(self) -> str:
        """Human readable name of source (YAML/JSON/ENV)."""
        raise NotImplementedError

    # ------- SHARED UTILITY METHODS (Encapsulation) -------
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve config value safely."""
        return self._config.get(key, default)

    def validate_path(self) -> None:
        """Validate file path existence."""
        if self._config_path and not self._config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self._config_path}")

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @property
    def config_keys(self) -> list[str]:
        return list(self._config.keys())

    @property
    def config_values(self) -> list[Any]:
        return list(self._config.values())

    def __contains__(self, key: str) -> bool:
        return key in self._config

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def __len__(self) -> int:
        return len(self._config)

    def __str__(self) -> str:
        return f"{self.source_name()}Loader(path={self._config_path})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config_path={self._config_path!r})"


# ==========================================================
# 2. YAML CONFIG LOADER (Inheritance + Polymorphism)
# ==========================================================

class YAMLConfigLoader(BaseConfigLoader):
    """Load configuration from YAML file."""

    def load(self) -> Dict[str, Any]:
        self.validate_path()

        if not self._config_path:
            raise ValueError("Config path is not set")

        try:
            with self._config_path.open("r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Malformed YAML in {self._config_path}: {e}")

        return self._config

    def source_name(self) -> str:
        return "YAML"


# ==========================================================
# 3. JSON CONFIG LOADER
# ==========================================================

class JSONConfigLoader(BaseConfigLoader):
    """Load configuration from JSON file."""

    def load(self) -> Dict[str, Any]:
        self.validate_path()

        if not self._config_path:
            raise ValueError("Config path is not set")

        try:
            with self._config_path.open("r", encoding="utf-8") as f:
                self._config = json.load(f) or {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in {self._config_path}: {e}")

        return self._config

    def source_name(self) -> str:
        return "JSON"


# ==========================================================
# 4. ENVIRONMENT CONFIG LOADER
# ==========================================================

class EnvConfigLoader(BaseConfigLoader):
    """
    Load configuration from environment variables.

    Example:
        export PDF_PATH="assets/doc.pdf"
        export OUTPUT_DIR="outputs"
    """

    def load(self) -> Dict[str, Any]:
        self._config = {
            "input": {"pdf_path": os.getenv("PDF_PATH")},
            "output": {"base_dir": os.getenv("OUTPUT_DIR")},
            "metadata": {
                "doc_title": os.getenv("DOC_TITLE", "Document"),
                "keywords": os.getenv("KEYWORDS", "").split(",")
                if os.getenv("KEYWORDS")
                else [],
            },
        }
        return self._config

    def source_name(self) -> str:
        return "ENVIRONMENT"


# ==========================================================
# 5. FACTORY PATTERN — Select Loader Type
# ==========================================================

class ConfigLoaderFactory:
    """Factory class to create appropriate loader based on file extension."""

    @staticmethod
    def create_loader(path: Path) -> BaseConfigLoader:
        ext = path.suffix.lower()

        if ext in [".yml", ".yaml"]:
            return YAMLConfigLoader(path)
        elif ext == ".json":
            return JSONConfigLoader(path)
        else:
            raise ValueError(f"Unsupported config format: {ext}")


# ==========================================================
# 6. HIGH-LEVEL ENTERPRISE WRAPPER (Maintains backward compatibility)
# ==========================================================

class ConfigLoader:
    """
    Backward-compatible wrapper.

    Uses:
    - YAMLConfigLoader
    - ConfigLoaderFactory
    - Polymorphic loader underneath
    """

    def __init__(self, config_path: Path = Path("application.yml")):
        self._config_path = config_path
        self._loader = ConfigLoaderFactory.create_loader(self._config_path)
        self._config = self._loader.load()

    # -------- Existing methods you already had (compatible) --------
    def get_pdf_path(self) -> Path:
        path = self._config.get("input", {}).get("pdf_path")
        if not path:
            raise ValueError(f"pdf_path not found in {self._config_path}")
        return Path(path)

    def get_output_dir(self) -> Path:
        dir_path = self._config.get("output", {}).get("base_dir")
        if not dir_path:
            raise ValueError(f"base_dir not found in {self._config_path}")
        return Path(dir_path)

    def get_doc_title(self) -> str:
        title = self._config.get("metadata", {}).get("doc_title", "Document")
        return str(title)

    def get_keywords(self) -> list[str]:
        keywords = self._config.get("metadata", {}).get("keywords", [])
        return [str(k) for k in keywords] if keywords else []

    # -------- Add transparency for access -------
    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def __str__(self) -> str:
        return f"ConfigLoader(source={self._loader.source_name()}, path={self._config_path})"

    def __repr__(self) -> str:
        return f"ConfigLoader(loader={self._loader!r})"
