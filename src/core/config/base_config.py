"""Base configuration classes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Union

from typing_extensions import Self

from .constants import ParserMode


@dataclass(frozen=True)
class BaseConfig:
    """
    Immutable base configuration object.

    This can be extended by more specific config classes.
    """

    input_path: Path
    output_dir: Path
    mode: ParserMode = ParserMode.FULL
    verbose: bool = False

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

    def with_mode(self, mode: Union[str, ParserMode]) -> Self:
        """Create new config with different mode."""
        mode_enum = mode if isinstance(mode, ParserMode) else ParserMode(mode)
        return type(self)(
            input_path=self.input_path,
            output_dir=self.output_dir,
            mode=mode_enum,
            verbose=self.verbose,
        )

    @property
    def input_exists(self) -> bool:
        """Check if input path exists."""
        return self.input_path.exists()

    @property
    def output_exists(self) -> bool:
        """Check if output directory exists."""
        return self.output_dir.exists()

    @property
    def is_full_mode(self) -> bool:
        """Check if in full mode."""
        return self.mode == ParserMode.FULL

    @property
    def is_verbose(self) -> bool:
        """Check if verbose mode."""
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
