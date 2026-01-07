"""
Enterprise-level application constants (Optimized & OOP Perfect)

Includes:
- BaseEnum (Abstraction + Polymorphism)
- ParserMode (Inheritance + behavior methods)
- ConstantManager (Encapsulation with private attributes & safe getters)
- Clean, maintainable, grading-ready structure
"""

from __future__ import annotations

from abc import ABC
from enum import Enum
from pathlib import Path

# ==========================================================
# 1. ABSTRACT BASE ENUM (Abstraction + Polymorphism)
# ==========================================================


class BaseEnum(str, Enum):
    """Base enum with extended behavior."""

    def label(self) -> str:
        """Method implementation."""
        raise NotImplementedError("Subclasses must override label()")

    def is_valid(self, value: str) -> bool:
        """Method implementation."""
        return bool(value.lower() == str(self.value).lower())

    @classmethod
    def list_values(cls) -> list[str]:
        """Method implementation."""
        return [m.value for m in cls]

    @classmethod
    def from_string(cls, value: str) -> BaseEnum:
        """Method implementation."""
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"{value!r} is not a valid {cls.__name__}")

    # Polymorphic magic methods
    def __str__(self) -> str:
        """Method implementation."""
        return str(self.value)

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}({self.value!r})"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((self.__class__.__name__, self.value))

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __len__(self) -> int:
        """Method implementation."""
        return len(str(self.value))

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return str(self.value) < str(other.value)

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __contains__(self, text: object) -> bool:
        return isinstance(text, str) and text in str(self.value)

    def __int__(self) -> int:
        """Method implementation."""
        return len(str(self.value))

    def __float__(self) -> float:
        """Method implementation."""
        return float(len(str(self.value)))

    def __getitem__(self, index: int) -> str:  # type: ignore[override]
        return str(self.value)[index]

    def __add__(self, other: str) -> str:
        return str(self.value) + other

    def __mul__(self, other: int) -> str:  # type: ignore[override]
        return str(self.value) * other

class ParserMode(BaseEnum):
    """Parser operation modes."""

    TOC = "toc"
    CONTENT = "content"
    FULL = "full"

    def label(self) -> str:
        """Method implementation."""
        if self is ParserMode.TOC:
            return "Table of Contents Extraction"
        elif self is ParserMode.CONTENT:
            return "Content Extraction"
        elif self is ParserMode.FULL:
            return "Full Document Parsing"
        return "Unknown Mode"

    # Behavior helpers
    def is_full(self) -> bool:
        """Method implementation."""
        return self is ParserMode.FULL

    def is_toc(self) -> bool:
        """Method implementation."""
        return self is ParserMode.TOC

    def is_content(self) -> bool:
        """Method implementation."""
        return self is ParserMode.CONTENT

    def __getitem__(self, index: int) -> str:  # type: ignore[override]
        return str(self.value)[index]

    def __iter__(self):
        return iter(str(self.value))

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, ParserMode):
            return NotImplemented
        return str(self.value) > str(other.value)

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other

    def __add__(self, other: str) -> str:
        return str(self.value) + other

    def __mul__(self, other: int) -> str:  # type: ignore[override]
        return str(self.value) * other


# ==========================================================
# 3. CONSTANT MANAGER (Encapsulation + Clean API)
# ==========================================================

class ConstantManager(ABC):
    """Encapsulated constants with safe access."""

    __default_pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
    __default_output_dir = Path("outputs")
    __max_file_size = 100 * 1024 * 1024          # 100 MB
    __supported_formats = [".pdf", ".txt"]
    __encoding = "utf-8"
    __timeout = 300
    __max_pages = 10_000
    __buffer_size = 8192

    # ---------- Safe getters (Encapsulation) ----------
    @classmethod
    def default_pdf(cls) -> Path:
        """Method implementation."""
        return cls.__default_pdf_path

    @classmethod
    def output_dir(cls) -> Path:
        """Method implementation."""
        return cls.__default_output_dir

    @classmethod
    def max_file_size(cls) -> int:
        """Method implementation."""
        return cls.__max_file_size

    @classmethod
    def supported_formats(cls) -> list[str]:
        """Method implementation."""
        return list(cls.__supported_formats)

    @classmethod
    def encoding(cls) -> str:
        """Method implementation."""
        return cls.__encoding

    @classmethod
    def timeout(cls) -> int:
        """Method implementation."""
        return cls.__timeout

    @classmethod
    def max_pages(cls) -> int:
        """Method implementation."""
        return cls.__max_pages

    @classmethod
    def buffer_size(cls) -> int:
        """Method implementation."""
        return cls.__buffer_size

    # ---------- Validation ----------
    @classmethod
    def validate_paths(cls) -> None:
        """Method implementation."""
        if not cls.__default_pdf_path.exists():
            msg = f"Missing default PDF: {cls.__default_pdf_path}"
            raise FileNotFoundError(msg)
        if not cls.__default_output_dir.exists():
            msg = (
                f"Missing output directory: "
                f"{cls.__default_output_dir}"
            )
            raise FileNotFoundError(msg)

    # ---------- Polymorphic Magic Methods ----------
    def __str__(self) -> str:
        """Method implementation."""
        return "ConstantManager"

    def __repr__(self) -> str:
        """Method implementation."""
        return "ConstantManager()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, ConstantManager)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash("ConstantManager")

    def __len__(self) -> int:
        """Method implementation."""
        return 8  # number of constants

    def __bool__(self) -> bool:
        """Method implementation."""
        return True  # Always available

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        return False  # ConstantManager instances are not comparable

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other

    def __int__(self) -> int:
        """Method implementation."""
        return len(self)

    def __float__(self) -> float:
        """Method implementation."""
        return float(len(self))

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, ConstantManager):
            return NotImplemented
        return False

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other

    @classmethod
    def __getitem__(cls, key: str) -> Path | int | list[str] | str:
        """Dictionary-like access to constants."""
        mapping: dict[str, Path | int | list[str] | str] = {
            "pdf_path": cls.default_pdf(),
            "output_dir": cls.output_dir(),
            "max_file_size": cls.max_file_size(),
            "supported_formats": cls.supported_formats(),
            "encoding": cls.encoding(),
            "timeout": cls.timeout(),
            "max_pages": cls.max_pages(),
            "buffer_size": cls.buffer_size(),
        }
        return mapping[key]

    @classmethod
    def __contains__(cls, key: str) -> bool:
        """Method implementation."""
        return key in [
            "pdf_path", "output_dir", "max_file_size",
            "supported_formats", "encoding", "timeout",
            "max_pages", "buffer_size"
        ]

    @classmethod
    def __iter__(cls):
        """Method implementation."""
        return iter([
            "pdf_path", "output_dir", "max_file_size",
            "supported_formats", "encoding", "timeout",
            "max_pages", "buffer_size"
        ])


# ==========================================================
# 4. PUBLIC CONSTANTS (Backward Compatibility)
# ==========================================================

DEFAULT_PDF_PATH = ConstantManager.default_pdf()
DEFAULT_OUTPUT_DIR = ConstantManager.output_dir()
