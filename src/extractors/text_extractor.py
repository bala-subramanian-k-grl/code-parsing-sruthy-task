"""Text extraction from PDF blocks."""

from typing import Any


class TextExtractor:
    """Extract text from PDF blocks and spans."""

    def extract(self, block: dict[str, Any]) -> str:
        """Extract text from block."""
        lines: list[Any] = block.get("lines", [])
        return "".join(self._extract_from_line(line) for line in lines)

    def _extract_from_line(self, line: dict[str, Any]) -> str:
        """Extract text from line spans."""
        spans: list[Any] = line.get("spans", [])
        return "".join(str(span.get("text", "")) for span in spans)

    def __str__(self) -> str:
        return "TextExtractor()"

    def __repr__(self) -> str:
        return "TextExtractor()"
