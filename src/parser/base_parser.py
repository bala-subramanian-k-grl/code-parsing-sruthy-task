"""Base parser abstract class (OOP + Overloading)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, overload

from src.core.config.models import ParserResult
from src.core.interfaces.parser_interface import ParserInterface


class BaseParser(ParserInterface, ABC):
    """Abstract base class for all parsers with full OOP support."""

    def __init__(self, file_path: Path) -> None:
        """Method implementation."""
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

    @property
    def file_size_kb(self) -> float:
        """Method implementation."""
        return self.file_size / 1024

    @property
    def file_size_mb(self) -> float:
        """Method implementation."""
        return self.file_size / (1024 * 1024)

    @property
    def file_exists(self) -> bool:
        """Method implementation."""
        return self.__file_path.exists()

    @property
    def file_is_file(self) -> bool:
        """Method implementation."""
        return self.__file_path.is_file()

    @property
    def file_stem(self) -> str:
        """Method implementation."""
        return self.__file_path.stem

    @property
    def file_parent(self) -> str:
        """Method implementation."""
        return str(self.__file_path.parent)

    @property
    def file_absolute(self) -> str:
        """Method implementation."""
        return str(self.__file_path.absolute())

    @property
    def is_pdf(self) -> bool:
        """Method implementation."""
        return self.file_suffix == ".pdf"

    @property
    def is_txt(self) -> bool:
        """Method implementation."""
        return self.file_suffix == ".txt"

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

    # ---------------- get_info (Overloaded) -------------------

    @overload
    def get_info(self) -> dict[str, Any]: ...

    @overload
    def get_info(self, *, extended: bool) -> dict[str, Any]: ...

    def get_info(self, *, extended: bool = False) -> dict[str, Any]:
        """
        Overloaded:
        - get_info()                   -> basic info
        - get_info(extended=True)      -> basic + extra info
        """
        info: dict[str, Any] = {
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

    # ---------------- _supports_format (protected) ------------

    def _supports_format(self, format_type: str, *formats: str) -> bool:
        """Check if parser supports one or more formats."""
        all_formats = (format_type,) + formats
        suffix = self.file_suffix.lstrip(".")
        return suffix in [fmt.lower().lstrip(".") for fmt in all_formats]

    # ---------------------------------------------------------
    # Magic Methods (clean and consistent)
    # ---------------------------------------------------------

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}(file={self.file_name})"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}(file_path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((type(self).__name__, self.__file_path))

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.__file_path.exists()

    def __len__(self) -> int:
        """Method implementation."""
        return self.file_size

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.file_size < other.file_size

    def __contains__(self, text: str) -> bool:
        """Method implementation."""
        return text in str(self.__file_path)

    def __enter__(self) -> "BaseParser":
        """Method implementation."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None
    ) -> None:
        self.close()

    def __int__(self) -> int:
        """Method implementation."""
        return self.file_size

    def __float__(self) -> float:
        """Method implementation."""
        return float(self.file_size)

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, BaseParser):
            return NotImplemented
        return self.file_size > other.file_size

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other

    def __add__(self, other: object) -> int:
        """Method implementation."""
        if isinstance(other, int):
            return self.file_size + other
        return NotImplemented

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return str(self.__file_path)[index]
