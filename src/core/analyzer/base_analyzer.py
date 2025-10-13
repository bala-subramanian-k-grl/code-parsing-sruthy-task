# USB PD Specification Parser - Content Analyzer Module
"""Minimal content analyzer with OOP principles."""

import re
from abc import ABC, abstractmethod



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

