"""
Enterprise OOP Base configuration classes with advanced
Encapsulation, Abstraction, Polymorphism, and Overloading.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, TypeVar, Union

from .constants import ParserMode

if TYPE_CHECKING:
    from typing import TypeVar
    ConfigType = TypeVar("ConfigType", bound="BaseConfig")


# ==========================================================
# Decorator for Encapsulation
# ==========================================================

T = TypeVar('T')

def protected_access(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator indicating this method is protected/internal."""
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
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
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def mode_behavior(self) -> str:
        raise NotImplementedError

    # Polymorphism
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True


# ==========================================================
# BASE CONFIG CLASS (Encapsulation + Polymorphism)
# ==========================================================

class BaseConfig(BaseConfigInterface):
    """
    Base configuration with full OOP improvements.

    - Encapsulation: private attributes + property getters/setters
    - Abstraction: inherited abstract interface
    - Polymorphism: mode_behavior(), summary(), validation
    """

    def __init__(self, input_path: Path, output_dir: Path, mode: ParserMode = ParserMode.FULL, verbose: bool = False) -> None:
        self.__input_path = input_path
        self.__output_dir = output_dir
        self.__mode = mode
        self.__verbose = verbose

    # -------------------------------
    # PROPERTY DECORATORS
    # -------------------------------

    @property
    def input_path(self) -> Path:
        return self.__input_path

    @input_path.setter
    def input_path(self, value: Path) -> None:
        self.__input_path = value

    @property
    def output_dir(self) -> Path:
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, value: Path) -> None:
        self.__output_dir = value

    @property
    def mode(self) -> ParserMode:
        return self.__mode

    @mode.setter
    def mode(self, value: ParserMode) -> None:
        self.__mode = value

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self.__verbose = value

    # ==========================================================
    # VALIDATION (Polymorphism + Encapsulation)
    # ==========================================================

    @protected_access
    def _validate_paths(self) -> None:
        if not self.__input_path.exists():
            raise FileNotFoundError(f"Input does not exist: {self.__input_path}")
        if not self.__output_dir.exists():
            raise FileNotFoundError(f"Output directory does not exist: {self.__output_dir}")

    def validate(self) -> None:
        self._validate_paths()

    # ==========================================================
    # MODE-SPECIFIC CONFIG CREATOR (Polymorphism + Overloading)
    # ==========================================================

    def with_mode(self, mode: Union[str, ParserMode]) -> Union['FullConfig', 'TOCConfig', 'ContentConfig']:
        """Create a new config object for a different mode (polymorphic)."""
        from src.core.config.base_config import FullConfig, TOCConfig, ContentConfig

        mode_enum = mode if isinstance(mode, ParserMode) else ParserMode(mode)

        if mode_enum == ParserMode.FULL:
            return FullConfig(self.__input_path, self.__output_dir, verbose=self.__verbose)

        if mode_enum == ParserMode.TOC:
            return TOCConfig(self.__input_path, self.__output_dir, verbose=self.__verbose)

        if mode_enum == ParserMode.CONTENT:
            return ContentConfig(self.__input_path, self.__output_dir, verbose=self.__verbose)

        raise ValueError(f"Unsupported mode: {mode}")

    # ==========================================================
    # POLYMORPHISM: Summary + Behavior
    # ==========================================================

    def summary(self) -> str:
        return (
            f"Config Summary:\n"
            f"  Input: {self.__input_path}\n"
            f"  Output: {self.__output_dir}\n"
            f"  Mode: {self.__mode.value}\n"
            f"  Verbose: {self.__verbose}\n"
            f"  Behavior: {self.mode_behavior()}\n"
        )

    def mode_behavior(self) -> str:
        return "General parsing behavior"

    # ==========================================================
    # ADDITIONAL POLYMORPHISM (Magic Methods)
    # ==========================================================

    def __str__(self) -> str:
        return f"BaseConfig(input={self.__input_path.name}, mode={self.__mode.value})"

    def __len__(self) -> int:
        return 4  # number of config fields

    def __bool__(self) -> bool:
        return self.__input_path.exists()

    def __int__(self) -> int:
        return len(str(self.__input_path))

    def __float__(self) -> float:
        return float(len(self.summary()))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseConfig):
            return NotImplemented
        return len(self.summary()) < len(other.summary())

    def __contains__(self, text: str) -> bool:
        return text in self.summary()


# ==========================================================
# MODE-SPECIFIC CONFIG CLASSES
# ==========================================================

class FullConfig(BaseConfig):
    """Configuration for FULL parsing mode."""

    def mode_behavior(self) -> str:
        return "Parses full PDF including TOC and content"

    def validate(self) -> None:
        super().validate()


class TOCConfig(BaseConfig):
    """Configuration for TOC-only mode."""

    def mode_behavior(self) -> str:
        return "Extracts only Table of Contents"

    def validate(self) -> None:
        super().validate()


class ContentConfig(BaseConfig):
    """Configuration for CONTENT-only mode."""

    def mode_behavior(self) -> str:
        return "Extracts only main content blocks"

    def validate(self) -> None:
        super().validate()
