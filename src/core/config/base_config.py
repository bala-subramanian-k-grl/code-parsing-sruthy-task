"""Enterprise OOP Base configuration classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Union

from typing_extensions import Self

from .constants import ParserMode

if TYPE_CHECKING:
    from typing import TypeVar
    ConfigType = TypeVar('ConfigType', bound='BaseConfig')


# ==========================================================
# 1. ABSTRACTION LAYER (OOP PRINCIPLE)
# ==========================================================

class BaseConfigInterface(ABC):
    """
    Abstract interface for configuration classes.

    Enforces:
    - validate()
    - summary()
    - mode_behavior()
    """

    @abstractmethod
    def validate(self) -> None:
        """Validate config values."""
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        """Return a formatted summary of the config."""
        raise NotImplementedError

    @abstractmethod
    def mode_behavior(self) -> str:
        """
        Polymorphic method:
        Each config mode returns its own behavior description.
        """
        raise NotImplementedError


# ==========================================================
# 2. BASE CLASS IMPLEMENTATION (Inherited by mode classes)
# ==========================================================

@dataclass(frozen=True)
class BaseConfig(BaseConfigInterface):
    """
    Immutable base configuration object.

    OOP Improvements Added:
    - Inherits BaseConfigInterface → Abstraction
    - mode_behavior() → Polymorphism
    - validate() → Polymorphism
    - will be extended by: FullConfig, TOCConfig, ContentConfig
    """

    input_path: Path
    output_dir: Path
    mode: ParserMode = ParserMode.FULL
    verbose: bool = False

    # -------------------------------
    # Class Factory
    # -------------------------------
    @classmethod
    def from_env(
        cls,
        input_path: str,
        output_dir: str,
        mode: str = "full",
        verbose: bool = False,
    ) -> Self:
        """Create config from environment variables."""
        if not input_path:
            raise ValueError("input_path cannot be empty")
        if not output_dir:
            raise ValueError("output_dir cannot be empty")

        return cls(
            input_path=Path(input_path),
            output_dir=Path(output_dir),
            mode=ParserMode(mode),
            verbose=verbose,
        )

    # -------------------------------
    # Polymorphic factory for modes
    # -------------------------------
    def with_mode(
        self,
        mode: Union[str, ParserMode]
    ) -> Union['FullConfig', 'TOCConfig', 'ContentConfig']:
        """Create new config with different mode (polymorphic)."""
        mode_enum = (
            mode if isinstance(mode, ParserMode) else ParserMode(mode)
        )

        if mode_enum == ParserMode.FULL:
            return FullConfig(
                self.input_path, self.output_dir, verbose=self.verbose
            )

        if mode_enum == ParserMode.TOC:
            return TOCConfig(
                self.input_path, self.output_dir, verbose=self.verbose
            )

        if mode_enum == ParserMode.CONTENT:
            return ContentConfig(
                self.input_path, self.output_dir, verbose=self.verbose
            )

        raise ValueError(f"Unsupported mode: {mode_enum}")

    # ==========================================================
    # 3. VALIDATION (Encapsulation + Polymorphism Prepare)
    # ==========================================================
    def validate(self) -> None:
        """Base validation logic."""
        if not self.input_path.exists():
            raise FileNotFoundError(
                f"Input file does not exist: {self.input_path}"
            )
        if not self.output_dir.exists():
            raise FileNotFoundError(
                f"Output directory does not exist: {self.output_dir}"
            )

    # ==========================================================
    # 4. POLYMORPHISM: Summary method
    # ==========================================================
    def summary(self) -> str:
        """Return human-readable config summary."""
        return (
            f"Config Summary:\n"
            f"  Input: {self.input_path}\n"
            f"  Output: {self.output_dir}\n"
            f"  Mode: {self.mode.value}\n"
            f"  Verbose: {self.verbose}\n"
            f"  Behavior: {self.mode_behavior()}\n"
        )

    # ==========================================================
    # 5. POLYMORPHIC METHOD: Each mode gives its own behavior
    # ==========================================================
    def mode_behavior(self) -> str:
        """Default behavior (can be overridden)."""
        return "General parsing behavior"

    # ==========================================================
    # 6. Additional Utility Methods (Encapsulation)
    # ==========================================================
    @property
    def input_exists(self) -> bool:
        return self.input_path.exists()

    @property
    def output_exists(self) -> bool:
        return self.output_dir.exists()

    @property
    def is_full_mode(self) -> bool:
        return self.mode == ParserMode.FULL

    @property
    def is_verbose(self) -> bool:
        return self.verbose

    def __str__(self) -> str:
        return f"BaseConfig(input={self.input_path.name}, mode={self.mode.value})"

    def __len__(self) -> int:
        return 4

    def __bool__(self) -> bool:
        return self.input_path.exists()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseConfig):
            return NotImplemented
        return self.input_path == other.input_path

    def __hash__(self) -> int:
        return hash((self.input_path, self.output_dir, self.mode))

    def __contains__(self, text: str) -> bool:
        return text in str(self.input_path)


# ==========================================================
# 7. MODE-SPECIFIC CONFIG CLASSES (Inheritance + Polymorphism)
# ==========================================================

class FullConfig(BaseConfig):
    """Configuration for FULL parsing mode."""

    def mode_behavior(self) -> str:
        return "Parses full PDF including TOC and content"

    def validate(self) -> None:
        super().validate()
        # add future full-mode specific validation


class TOCConfig(BaseConfig):
    """Configuration for TOC-only mode."""

    def mode_behavior(self) -> str:
        return "Extracts only Table of Contents"

    def validate(self) -> None:
        super().validate()


class ContentConfig(BaseConfig):
    """Configuration for CONTENT parsing mode."""

    def mode_behavior(self) -> str:
        return "Extracts only main content blocks"

    def validate(self) -> None:
        super().validate()
