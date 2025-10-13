"""Security utilities with OOP principles."""

from pathlib import Path
from typing import Union


class PathValidator:  # Encapsulation
    """Secure path validation utility."""

    @staticmethod  # Abstraction
    def validate_path(path: Union[str, Path], base_dir: Path) -> Path:
        """Validate path is within base directory."""
        safe_path = Path(path).resolve()
        try:
            safe_path.relative_to(base_dir.resolve())
        except ValueError:
            raise ValueError(f"Path outside allowed directory: {path}") from None
        return safe_path

    @staticmethod  # Abstraction
    def validate_assets_path(path: Union[str, Path]) -> Path:
        """Validate path is within assets directory."""
        assets_dir = Path.cwd().resolve() / "assets"
        return PathValidator.validate_path(path, assets_dir)

    @staticmethod  # Abstraction
    def validate_output_path(path: Union[str, Path]) -> Path:
        """Validate path is within outputs directory."""
        outputs_dir = Path.cwd().resolve() / "outputs"
        return PathValidator.validate_path(path, outputs_dir)
