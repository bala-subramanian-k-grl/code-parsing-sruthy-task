# USB PD Specification Parser - Content Analyzer Module
"""Minimal content analyzer with OOP principles."""

import re
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any


class BaseAnalyzer(ABC):  # Abstraction
    @abstractmethod  # Abstraction
    def analyze(self, text: str) -> str:
        pass


class PatternAnalyzer(BaseAnalyzer):  # Inheritance
    def __init__(self):
        patterns = {  # Encapsulation
            "requirement": r"\b(shall|must|required)\b",
            "definition": r":",
            "numbered_item": r"^\d+\.",
            "bullet_point": r"^[•\-]",
            "table_data": r"[\|\t]{2,}",
        }
        self._compiled = {
            k: re.compile(v, re.I) for k, v in patterns.items()
        }  # Encapsulation

    def analyze(self, text: str) -> str:  # Polymorphism
        text = text.strip()
        for content_type, pattern in self._compiled.items():
            if pattern.search(text):
                return str(content_type)
        return "paragraph"


class ContentAnalyzer:  # Composition
    def __init__(self):
        self._analyzer = PatternAnalyzer()  # Encapsulation

    def classify(self, text: str) -> str:  # Abstraction
        return str(self._analyzer.analyze(text))  # Polymorphism

    def extract_items(
        self, text: str, page: int
    ) -> Iterator[dict[str, Any]]:  # Abstraction
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
