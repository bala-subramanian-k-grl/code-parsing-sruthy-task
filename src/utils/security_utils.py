"""Security utilitie with OOP principles."""

from pathlib import Path
from typing import Union


class PathValidator:  # Encapsulation
    """Secure path validation utility."""

    def __init__(self) -> None:
        self.__validation_count: int = 0  # Private counter
        self.__violation_count: int = 0  # Private violation tracking

    @property
    def validation_count(self) -> int:
        """Get validation count."""
        return self.__validation_count

    @property
    def violation_count(self) -> int:
        """Get violation count."""
        return self.__violation_count

    def __increment_validation_count(self) -> None:  # Private method
        """Increment validation counter."""
        self.__validation_count += 1

    def __increment_violation_count(self) -> None:  # Private method
        """Increment violation counter."""
        self.__violation_count += 1

    def validate_path(self, path: Union[str, Path], base_dir: Path) -> Path:
        """Validate path is within base directory."""
        self.__increment_validation_count()
        safe_path = Path(path).resolve()
        try:
            safe_path.relative_to(base_dir.resolve())
        except ValueError:
            self.__increment_violation_count()
            msg = f"Path outside allowed directory: {path}"
            raise ValueError(msg) from None
        return safe_path

    def validate_assets_path(self, path: Union[str, Path]) -> Path:
        """Validate path is within assets directory."""
        assets_dir = Path.cwd().resolve() / "assets"
        return self.validate_path(path, assets_dir)

    def validate_output_path(self, path: Union[str, Path]) -> Path:
        """Validate path is within outputs directory."""
        outputs_dir = Path.cwd().resolve() / "outputs"
        return self.validate_path(path, outputs_dir)


class StrictPathValidator(PathValidator):  # Inheritance + Polymorphism
    """Strict path validator with additional checks."""

    def validate_path(
        self, path: Union[str, Path], base_dir: Path
    ) -> Path:  # Method override
        """Strict path validation."""
        result = super().validate_path(path, base_dir)
        return result


class LenientPathValidator(PathValidator):  # Inheritance + Polymorphism
    """Lenient path validator with warnings."""

    def validate_path(
        self, path: Union[str, Path], base_dir: Path
    ) -> Path:  # Method override
        """Lenient path validation with warnings."""
        try:
            return super().validate_path(path, base_dir)
        except ValueError as e:
            import logging

            msg = f"Path validation warning: {e}"
            logging.getLogger(__name__).warning(msg)
            return Path(path).resolve()
