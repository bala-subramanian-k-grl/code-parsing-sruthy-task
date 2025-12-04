"""
Enterprise OOP Configuration Loader Module (Optimized & Compact)

Implements:
- Abstraction (BaseConfigLoader)
- Inheritance (YAMLConfigLoader, JSONConfigLoader, EnvConfigLoader)
- Factory Pattern (ConfigLoaderFactory)
- Polymorphism (load(), source_name(), magic methods)
- Encapsulation (private/protected methods, property access)
- Overloading (create(), get())
"""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar, overload

import yaml

from src.core.interfaces.factory_interface import FactoryInterface

# ======================================================
# Helper Decorator — Protected Access
# ======================================================

t_config = TypeVar('t_config')


def protected_access(
    func: Callable[..., t_config]
) -> Callable[..., t_config]:
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> t_config:
        return func(self, *args, **kwargs)
    return wrapper


# ======================================================
# ABSTRACT BASE LOADER (Abstraction + Encapsulation)
# ======================================================


class BaseConfigLoader(ABC):
    """Abstract loader interface."""

    def __init__(self, config_path: Path | None = None):
        self.__config_path = config_path
        self._config: dict[str, Any] = {}

    # ---------- Abstract Methods ----------
    @abstractmethod
    def load(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def source_name(self) -> str:
        raise NotImplementedError

    # ---------- Shared Protected Methods ----------
    @protected_access
    def _validate_path(self) -> None:
        if self.__config_path and not self.__config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.__config_path}")

    @protected_access
    def _read_file(self) -> str:
        if not self.__config_path:
            raise ValueError("Config path is not set")
        with self.__config_path.open("r", encoding="utf-8") as f:
            return f.read()

    # ---------- Public Accessors ----------
    @property
    def config_path(self) -> Path | None:
        return self.__config_path

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    # ---------- Overloaded Getters ----------
    @overload
    def get(self, key: str) -> Any: ...
    @overload
    def get(self, key: str, default: Any) -> Any: ...

    def get(self, key: str, default: Any = None) -> Any:
        # Handle nested keys like "input.pdf_path"
        if "." in key:
            keys = key.split(".")
            value: dict[str, Any] | Any = self._config
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, default)
                    if value is None:
                        return default
                else:
                    return default
            return value
        return self._config.get(key, default)

    # ---------- Magic Methods (Polymorphism) ----------
    def __len__(self) -> int:
        return len(self._config)

    def __str__(self) -> str:
        return f"{self.source_name()}Loader(path={self.__config_path})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self.__config_path!r})"

    def __bool__(self) -> bool:
        return bool(self._config)

    def __contains__(self, item: str) -> bool:
        return item in self._config

    def __call__(self, key: str, default: Any = None) -> Any:
        """Make loader callable for getting values."""
        result: Any = self.get(key, default)
        return result

    def __iter__(self):
        """Iterate over config keys."""
        return iter(self._config.keys())

    def __getitem__(self, key: str):
        """Dictionary-like access."""
        return self._config[key]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseConfigLoader):
            return NotImplemented
        return len(self) < len(other)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __int__(self) -> int:
        return len(self._config)

    def __float__(self) -> float:
        return float(len(self._config))

    def __setitem__(self, key: str, value: Any) -> None:
        self._config[key] = value

    def __delitem__(self, key: str) -> None:
        del self._config[key]


# ======================================================
# YAML LOADER
# ======================================================

class YAMLConfigLoader(BaseConfigLoader):
    def load(self) -> dict[str, Any]:
        self._validate_path()
        data: Any = yaml.safe_load(self._read_file())
        self._config = data if isinstance(data, dict) else {}
        return self._config

    def source_name(self) -> str:
        return "YAML"


# ======================================================
# JSON LOADER
# ======================================================

class JSONConfigLoader(BaseConfigLoader):
    def load(self) -> dict[str, Any]:
        self._validate_path()
        try:
            self._config = json.loads(self._read_file()) or {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON: {e}") from e
        return self._config

    def source_name(self) -> str:
        return "JSON"


# ======================================================
# ENVIRONMENT LOADER
# ======================================================

class EnvConfigLoader(BaseConfigLoader):
    def load(self) -> dict[str, Any]:
        self._config = {
            "input": {"pdf_path": os.getenv("PDF_PATH")},
            "output": {"base_dir": os.getenv("OUTPUT_DIR")},
            "metadata": {
                "doc_title": os.getenv("DOC_TITLE", "Document"),
                "keywords": os.getenv("KEYWORDS", "").split(",")
                if os.getenv("KEYWORDS") else []
            },
        }
        return self._config

    def source_name(self) -> str:
        return "ENVIRONMENT"


# ======================================================
# FACTORY PATTERN (Polymorphism + Overloading)
# ======================================================

class ConfigLoaderFactory(FactoryInterface[BaseConfigLoader]):
    """Create appropriate config loader based on file extension."""

    def create(  # type: ignore[override]
        self, path: Path, *args: Any, **kwargs: Any
    ) -> BaseConfigLoader:
        ext = path.suffix.lower()

        if ext in (".yml", ".yaml"):
            return YAMLConfigLoader(path)
        if ext == ".json":
            return JSONConfigLoader(path)

        raise ValueError(f"Unsupported config format: {ext}")

    def __str__(self) -> str:
        return "ConfigLoaderFactory"

    def __repr__(self) -> str:
        return "ConfigLoaderFactory()"

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return 3

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ConfigLoaderFactory)

    def __hash__(self) -> int:
        return hash("ConfigLoaderFactory")

    def __int__(self) -> int:
        return 3

    def __float__(self) -> float:
        return 3.0


# ======================================================
# HIGH-LEVEL WRAPPER (Simple Public API)
# ======================================================

class ConfigLoader(BaseConfigLoader):
    """User-facing loader (default = YAML)."""

    def __init__(self, config_path: Path = Path("application.yml")):
        super().__init__(config_path)
        self.__factory = ConfigLoaderFactory()
        self.__loader = self.__factory.create(config_path)
        self._config = self.__loader.load()

    def load(self) -> dict[str, Any]:
        return self.__loader.load()

    def source_name(self) -> str:
        return self.__loader.source_name()
