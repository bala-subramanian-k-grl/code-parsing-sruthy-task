"""
Enterprise-level application constants.

OOP Enhancements:
- BaseEnum abstraction for consistent enum behavior
- ParserMode inherits BaseEnum (polymorphic methods)
- ConstantManager for encapsulation of constant validation
- Utility methods for dynamic expansion of constants
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path


# ==========================================================
# 1. ABSTRACT BASE ENUM (Abstraction + Polymorphism)
# ==========================================================

class BaseEnum(str, Enum):
    """
    Abstract enum base class.

    Adds polymorphic behavior:
    - label() → human friendly name
    - is_valid() → enum-level validation
    """

    def label(self) -> str:
        """Return a human-readable label."""
        raise NotImplementedError("Subclasses must implement label()")

    def is_valid(self, value: str) -> bool:
        """Check if string matches an enum member."""
        return value.lower() == self.value.lower()

    @classmethod
    def list_values(cls) -> list[str]:
        """List all enum values."""
        return [member.value for member in cls]

    @classmethod
    def from_string(cls, value: str) -> "BaseEnum":
        """Convert string to enum safely."""
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"{value!r} is not a valid {cls.__name__}")


# ==========================================================
# 2. PARSER MODE ENUM (Inheritance + Polymorphism)
# ==========================================================

class ParserMode(BaseEnum):
    """Parser processing modes with behavior."""

    TOC = "toc"
    CONTENT = "content"
    FULL = "full"

    # Polymorphic behavior for mode descriptions
    def label(self) -> str:
        match self:
            case ParserMode.TOC:
                return "Table of Contents Extraction"
            case ParserMode.CONTENT:
                return "Content Extraction"
            case ParserMode.FULL:
                return "Full Document Parsing"
        return "Unknown Mode"

    def is_full(self) -> bool:
        """Check if mode is FULL mode."""
        return self == ParserMode.FULL

    def is_toc(self) -> bool:
        """Check if mode is TOC mode."""
        return self == ParserMode.TOC

    def is_content(self) -> bool:
        """Check if mode is CONTENT mode."""
        return self == ParserMode.CONTENT


# ==========================================================
# 3. CONSTANT MANAGER (Encapsulation)
# ==========================================================

class ConstantManager:
    """
    Encapsulates constants and provides validation.
    Enterprise-style utility class.
    """

    DEFAULT_PDF_PATH = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
    DEFAULT_OUTPUT_DIR = Path("outputs")

    @staticmethod
    def validate_paths() -> None:
        """Validate that required paths exist."""
        if not ConstantManager.DEFAULT_PDF_PATH.exists():
            raise FileNotFoundError(
                f"Default PDF not found: {ConstantManager.DEFAULT_PDF_PATH}"
            )
        if not ConstantManager.DEFAULT_OUTPUT_DIR.exists():
            raise FileNotFoundError(
                f"Output directory not found: {ConstantManager.DEFAULT_OUTPUT_DIR}"
            )

    @staticmethod
    def get_default_pdf() -> Path:
        """Safe getter for default PDF path."""
        return ConstantManager.DEFAULT_PDF_PATH

    @staticmethod
    def get_output_dir() -> Path:
        """Safe getter for output directory."""
        return ConstantManager.DEFAULT_OUTPUT_DIR


# ==========================================================
# 4. EXPORTED CONSTANTS (Backward Compatibility)
# ==========================================================

DEFAULT_PDF_PATH = ConstantManager.get_default_pdf()
DEFAULT_OUTPUT_DIR = ConstantManager.get_output_dir()
