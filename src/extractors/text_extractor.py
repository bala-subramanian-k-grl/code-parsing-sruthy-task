"""Text extraction from PDF blocks."""

from __future__ import annotations
from typing import Any

from src.extractors.extractor_interface import ExtractorInterface


class TextExtractor(ExtractorInterface):
    """Extract text from PDF blocks and spans."""

    def __init__(self) -> None:
        self.__extraction_count = 0

    # ---------------------------------------------------
    # Encapsulation + Polymorphism (OOP Improvements)
    # ---------------------------------------------------

    @property
    def extractor_type(self) -> str:
        """Polymorphic extractor type."""
        return "TextExtractor"

    def validate(self) -> None:
        """Optional validation (kept minimal)."""
        pass

    # ---------------------------------------------------
    # Main Extraction Logic (unchanged)
    # ---------------------------------------------------

    @property
    def extraction_count(self) -> int:
        """Get extraction count."""
        return self.__extraction_count

    @property
    def has_extractions(self) -> bool:
        """Check if any extractions occurred."""
        return self.__extraction_count > 0

    @property
    def extraction_rate(self) -> float:
        """Return extraction count as float."""
        return float(self.__extraction_count)

    def extract(self, data: dict[str, Any]) -> str:
        """Extract text from block."""
        self.__extraction_count += 1
        lines: list[Any] = data.get("lines", [])
        return "".join(self._extract_from_line(line) for line in lines)

    def _extract_from_line(self, line: dict[str, Any]) -> str:
        """Extract text from line spans."""
        spans: list[Any] = line.get("spans", [])
        return "".join(str(span.get("text", "")) for span in spans)

    # ---------------------------------------------------
    # Magic Methods (kept same)
    # ---------------------------------------------------

    def __str__(self) -> str:
        return "TextExtractor()"

    def __repr__(self) -> str:
        return "TextExtractor()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TextExtractor)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __len__(self) -> int:
        return self.__extraction_count

    def __bool__(self) -> bool:
        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TextExtractor):
            return NotImplemented
        return self.__extraction_count < other.__extraction_count

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __int__(self) -> int:
        """Get extraction count as int."""
        return self.__extraction_count

    def __float__(self) -> float:
        """Get extraction count as float."""
        return float(self.__extraction_count)
