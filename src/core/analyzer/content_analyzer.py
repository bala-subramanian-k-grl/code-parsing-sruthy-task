"""Content analyzer implementation."""
# USB PD Specification Parser - Content Analyzer Module

from collections.abc import Iterator
from typing import Any

from .base_analyzer import PatternAnalyzer


class ContentAnalyzer:
    """Content analyzer using pattern matching."""

    def __init__(self) -> None:
        self._analyzer = PatternAnalyzer()  # Encapsulation
        self._key_terms = {
            "USB",
            "PD",
            "Power Delivery",
            "VBUS",
            "CC",
            "VCONN",
            "Source",
            "Sink",
            "DFP",
            "UFP",
            "DRP",
            "Cable",
            "Connector",
            "Voltage",
            "Current",
            "Watt",
            "Protocol",
            "Message",
            "Negotiation",
            "Contract",
            "Capability",
            "PDO",
            "RDO",
            "Fast Role Swap",
            "FRS",
            "BIST",
            "VDM",
            "SVID",
            "Alternate Mode",
            "Billboard",
            "Authentication",
            "Security",
        }

    def classify(self, text: str) -> str:  # Abstraction
        """Classify text content type."""
        return str(self._analyzer.analyze(text))  # Polymorphism

    def count_key_terms(self, text: str) -> int:
        """Count USB PD key terms in text."""
        text_upper = text.upper()
        count = sum(1 for term in self._key_terms if term.upper() in text_upper)
        return count

    def is_major_section(self, text: str) -> bool:
        """Check if text is a major section header."""
        return self._analyzer.analyze(text) == "major_section"

    def extract_items(
        self, text: str, page: int
    ) -> Iterator[dict[str, Any]]:  # Abstraction
        """Extract content items from text."""
        for i, line in enumerate(text.split("\n")):
            line = line.strip()
            if len(line) > 10:
                content_type = self.classify(line)
                if content_type != "paragraph":
                    yield {
                        "type": content_type,
                        "content": line,
                        "page": page + 1,
                        "block_id": f"{content_type[0]}{page}_{i}",
                        "bbox": [],
                    }
