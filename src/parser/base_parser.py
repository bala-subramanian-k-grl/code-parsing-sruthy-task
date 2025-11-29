"""Base parser abstract class (OOP + Overloading)."""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, overload

from src.core.config.models import ParserResult
from src.core.interfaces.parser_interface import ParserInterface


class BaseParser(ParserInterface, ABC):
    """Abstract base class for all parsers with full OOP support."""

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

        # Use overloaded validate() with raise_on_error=True
        if not self.validate(raise_on_error=True):
            raise FileNotFoundError(
                f"File not found or is not a valid file: {file_path}"
            )

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------

    @property
    def file_path(self) -> Path:
        """Get the file path being parsed."""
        return self.__file_path

    @property
    def file_name(self) -> str:
        """Get filename."""
        return self.__file_path.name

    @property
    def file_suffix(self) -> str:
        """Get file extension."""
        return self.__file_path.suffix.lower()

    @property
    def file_size(self) -> int:
        """Get file size in bytes."""
        return (
            self.__file_path.stat().st_size
            if self.__file_path.exists()
            else 0
        )

    # ---------------------------------------------------------
    # Polymorphism (subclass-specific behavior)
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def parser_type(self) -> str:
        """Polymorphic parser identifier."""
        raise NotImplementedError

    def supports(self, extension: str) -> bool:
        """Polymorphic extension support check."""
        return extension.lower() == self.file_suffix

    # ---------------------------------------------------------
    # Validation (with overloading)
    # ---------------------------------------------------------

    @overload
    def validate(self) -> bool: ...
    
    @overload
    def validate(self, *, raise_on_error: bool) -> bool: ...

    def validate(self, *, raise_on_error: bool = False) -> bool:
        """
        Overloaded validation:
        - validate()                          -> bool
        - validate(raise_on_error=True)       -> bool + raises on failure
        """
        is_valid = self.__file_path.exists() and self.__file_path.is_file()
        if not is_valid and raise_on_error:
            raise FileNotFoundError(
                f"File not found or is not a valid file: {self.__file_path}"
            )
        return is_valid

    # ---------------------------------------------------------
    # Core abstract parse method
    # ---------------------------------------------------------

    @abstractmethod
    def parse(self) -> ParserResult:
        """Parse file and return result - implemented by subclasses."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # ParserInterface implementation
    # ---------------------------------------------------------

    def open(self) -> None:
        """Open parser resources."""
        # Kept minimal; subclasses may override if needed.
        pass

    def close(self) -> None:
        """Close parser resources."""
        # Kept minimal; subclasses may override if needed.
        pass

    def reset(self) -> None:
        """Reset parser state."""
        # Kept minimal; subclasses may override if needed.
        pass

    # ---------------- get_info (Overloaded) -------------------

    @overload
    def get_info(self) -> Dict[str, Any]: ...

    @overload
    def get_info(self, *, extended: bool) -> Dict[str, Any]: ...

    def get_info(self, *, extended: bool = False) -> Dict[str, Any]:
        """
        Overloaded:
        - get_info()                   -> basic info
        - get_info(extended=True)      -> basic + extra info
        """
        info: Dict[str, Any] = {
            "type": self.parser_type,
            "file": self.file_name,
            "suffix": self.file_suffix,
        }
        if extended:
            info.update(
                {
                    "size_bytes": self.file_size,
                    "path": str(self.file_path),
                }
            )
        return info

    # ---------------- supports_format ------------

    def supports_format(self, *formats: str) -> bool:
        """Check if parser supports one or more formats."""
        suffix = self.file_suffix.lstrip(".")
        return suffix in [fmt.lower().lstrip(".") for fmt in formats]

    # ---------------------------------------------------------
    # Magic Methods (clean and consistent)
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(file={self.file_name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(file_path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path))

    def __bool__(self) -> bool:
        return self.__file_path.exists()

    def __len__(self) -> int:
        return self.file_size

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.file_size < other.file_size

    def __contains__(self, text: str) -> bool:
        return text in str(self.__file_path)

    def __enter__(self) -> "BaseParser":
        self.open()
        return self

    def __exit__(self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        self.close()

    def __int__(self) -> int:
        return self.file_size

    def __float__(self) -> float:
        return float(self.file_size)
