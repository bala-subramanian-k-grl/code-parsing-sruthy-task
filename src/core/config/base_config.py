"""
Enterprise OOP Base configuration classes with advanced
Encapsulation, Abstraction, Polymorphism, and Overloading.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from .constants import ParserMode

if TYPE_CHECKING:
    ConfigType = TypeVar("ConfigType", bound="BaseConfig")


# ==========================================================
# Decorator for Encapsulation
# ==========================================================

t_return = TypeVar('t_return')


def protected_access(
    func: Callable[..., t_return]
) -> Callable[..., t_return]:
    """Decorator indicating this method is protected/internal."""
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> t_return:
        """Method implementation."""
        return func(self, *args, **kwargs)
    return wrapper


# ==========================================================
# ABSTRACT INTERFACE (Abstraction + Polymorphism)
# ==========================================================

class BaseConfigInterface(ABC):
    """
    Abstract interface for configuration logic.

    Enforces:
    - validate()
    - summary()
    - mode_behavior()
    """

    @abstractmethod
    def validate(self) -> None:
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def mode_behavior(self) -> str:
        """Method implementation."""
        raise NotImplementedError

    # Polymorphism
    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        """Method implementation."""
        return True


# ==========================================================
# BASE CONFIG CLASS (Encapsulation + Polymorphism)
# ==========================================================

class BaseConfig(BaseConfigInterface, ABC):
    """
    Abstract base configuration with full OOP improvements.

    - Encapsulation: private attributes + property getters/setters
    - Abstraction: abstract mode_behavior() method
    - Polymorphism: mode_behavior(), summary(), validation
    """

    def __init__(
        self,
        input_path: Path,
        output_dir: Path,
        mode: ParserMode = ParserMode.FULL,
        verbose: bool = False
    ) -> None:
        self.__input_path = input_path
        self.__output_dir = output_dir
        self.__mode = mode
        self.__verbose = verbose

    # -------------------------------
    # PROPERTY DECORATORS
    # -------------------------------

    @property
    def input_path(self) -> Path:
        """Method implementation."""
        return self.__input_path

    @input_path.setter
    def input_path(self, value: Path) -> None:
        """Method implementation."""
        self.__input_path = value

    @property
    def output_dir(self) -> Path:
        """Method implementation."""
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, value: Path) -> None:
        """Method implementation."""
        self.__output_dir = value

    @property
    def mode(self) -> ParserMode:
        """Method implementation."""
        return self.__mode

    @mode.setter
    def mode(self, value: ParserMode) -> None:
        """Method implementation."""
        self.__mode = value

    @property
    def verbose(self) -> bool:
        """Method implementation."""
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        """Method implementation."""
        self.__verbose = value

    # ==========================================================
    # VALIDATION (Polymorphism + Encapsulation)
    # ==========================================================

    @protected_access
    def _validate_paths(self) -> None:
        """Method implementation."""
        if not self.__input_path.exists():
            msg = f"Input does not exist: {self.__input_path}"
            raise FileNotFoundError(msg)
        if not self.__output_dir.exists():
            msg = f"Output directory does not exist: {self.__output_dir}"
            raise FileNotFoundError(msg)

    def validate(self) -> None:
        """Method implementation."""
        self._validate_paths()

    # ==========================================================
    # MODE-SPECIFIC CONFIG CREATOR (Polymorphism + Overloading)
    # ==========================================================

    def with_mode(
        self, mode: str | ParserMode
    ) -> "FullConfig | TOCConfig | ContentConfig":
        """
        Create a new config object for a different mode (polymorphic).
        """
        from src.core.config.base_config import (
            ContentConfig,
            FullConfig,
            TOCConfig,
        )

        mode_enum = mode if isinstance(mode, ParserMode) else ParserMode(mode)

        if mode_enum == ParserMode.FULL:
            return FullConfig(
                self.__input_path, self.__output_dir,
                verbose=self.__verbose
            )

        if mode_enum == ParserMode.TOC:
            return TOCConfig(
                self.__input_path, self.__output_dir,
                verbose=self.__verbose
            )

        if mode_enum == ParserMode.CONTENT:
            return ContentConfig(
                self.__input_path, self.__output_dir,
                verbose=self.__verbose
            )

        raise ValueError(f"Unsupported mode: {mode}")

    # ==========================================================
    # POLYMORPHISM: Summary + Behavior
    # ==========================================================

    def summary(self) -> str:
        """Method implementation."""
        return (
            f"Config Summary:\n"
            f"  Input: {self.__input_path}\n"
            f"  Output: {self.__output_dir}\n"
            f"  Mode: {self.__mode.value}\n"
            f"  Verbose: {self.__verbose}\n"
            f"  Behavior: {self.mode_behavior()}\n"
        )

    @abstractmethod
    def mode_behavior(self) -> str:
        """
        Return mode-specific behavior description.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    # ==========================================================
    # ADDITIONAL POLYMORPHISM (Magic Methods)
    # ==========================================================

    def __str__(self) -> str:
        """Method implementation."""
        return (
            f"BaseConfig(input={self.__input_path.name}, "
            f"mode={self.__mode.value})"
        )

    def __len__(self) -> int:
        """Method implementation."""
        return 4  # number of config fields

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.__input_path.exists()

    def __int__(self) -> int:
        """Method implementation."""
        return len(str(self.__input_path))

    def __float__(self) -> float:
        """Method implementation."""
        return float(len(self.summary()))

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, BaseConfig):
            return NotImplemented
        return len(self.summary()) < len(other.summary())

    def __contains__(self, text: str) -> bool:
        """Method implementation."""
        return text in self.summary()

    @property
    def input_name(self) -> str:
        """Method implementation."""
        return self.__input_path.name

    @property
    def input_stem(self) -> str:
        """Method implementation."""
        return self.__input_path.stem

    @property
    def input_suffix(self) -> str:
        """Method implementation."""
        return self.__input_path.suffix

    @property
    def input_exists(self) -> bool:
        """Method implementation."""
        return self.__input_path.exists()

    @property
    def output_exists(self) -> bool:
        """Method implementation."""
        return self.__output_dir.exists()

    @property
    def output_name(self) -> str:
        """Method implementation."""
        return self.__output_dir.name

    @property
    def is_verbose(self) -> bool:
        """Method implementation."""
        return self.__verbose

    @property
    def mode_value(self) -> str:
        """Method implementation."""
        return str(self.__mode.value)

    @property
    def mode_name(self) -> str:
        """Method implementation."""
        return str(self.__mode.name)

    def __getitem__(self, key: str) -> Path | ParserMode | bool | None:
        """Method implementation."""
        attrs: dict[str, Path | ParserMode | bool] = {
            "input": self.__input_path,
            "output": self.__output_dir,
            "mode": self.__mode,
            "verbose": self.__verbose
        }
        return attrs.get(key)

    def __iter__(self):
        """Method implementation."""
        return iter(["input", "output", "mode", "verbose"])

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, BaseConfig):
            return NotImplemented
        return len(self.summary()) > len(other.summary())

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other

    def __add__(self, other: object) -> int:
        """Method implementation."""
        if isinstance(other, int):
            return len(self.summary()) + other
        return NotImplemented

    def __sub__(self, other: object) -> int:
        """Method implementation."""
        if isinstance(other, int):
            return len(self.summary()) - other
        return NotImplemented


# ==========================================================
# MODE-SPECIFIC CONFIG CLASSES
# ==========================================================

class FullConfig(BaseConfig, ABC):
    """Configuration for FULL parsing mode."""

    def mode_behavior(self) -> str:
        """Method implementation."""
        return "Parses full PDF including TOC and content"

    def validate(self) -> None:
        """Method implementation."""
        super().validate()


class TOCConfig(BaseConfig, ABC):
    """Configuration for TOC-only mode."""

    def mode_behavior(self) -> str:
        """Method implementation."""
        return "Extracts only Table of Contents"

    def validate(self) -> None:
        """Method implementation."""
        super().validate()


class ContentConfig(BaseConfig, ABC):
    """Configuration for CONTENT-only mode."""

    def mode_behavior(self) -> str:
        """Method implementation."""
        return "Extracts only main content blocks"

    def validate(self) -> None:
        """Method implementation."""
        super().validate()
