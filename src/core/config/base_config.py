"""Base configuration classes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Union

from typing_extensions import Self


class ConfigMode(str, Enum):
    """Valid configuration modes."""

    FULL = "full"
    TOC = "toc"
    CONTENT = "content"


@dataclass(frozen=True)
class BaseConfig:
    """
    Immutable base configuration object.

    This can be extended by more specific config classes.
    """

    input_path: Path
    output_dir: Path
    mode: ConfigMode = ConfigMode.FULL
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
            mode=ConfigMode(mode),
            verbose=verbose,
        )

    def with_mode(self, mode: Union[str, ConfigMode]) -> Self:
        """Create new config with different mode."""
        mode_enum = mode if isinstance(mode, ConfigMode) else ConfigMode(mode)
        return type(self)(
            input_path=self.input_path,
            output_dir=self.output_dir,
            mode=mode_enum,
            verbose=self.verbose,
        )
