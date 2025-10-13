"""Content analyzer implementation."""
# USB PD Specification Parser - Content Analyzer Module

from collections.abc import Iterator
from typing import Any
from .base_analyzer import PatternAnalyzer



class ContentAnalyzer:  # Composition
    """Content analyzer using pattern matching."""
    def __init__(self) -> None:
        self._analyzer = PatternAnalyzer()  # Encapsulation

    def classify(self, text: str) -> str:  # Abstraction
        """Classify text content type."""
        return str(self._analyzer.analyze(text))  # Polymorphism

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
