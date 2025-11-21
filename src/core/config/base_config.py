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
