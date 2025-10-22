# USB PD Specification Parser - Content Analyzer Module
"""Enhanced content analyzer with polymorphism."""

import re
from abc import ABC, abstractmethod
from typing import Protocol, Type, Dict


class BaseAnalyzer(ABC):
    """Abstract base analyzer."""

    @abstractmethod
    def analyze(self, text: str) -> str:
        """Analyze text and return content type."""
    
    def __call__(self, text: str) -> str:  # Magic method polymorphism
        """Make analyzer callable."""
        return self.analyze(text)
    
    def __str__(self) -> str:  # Magic method polymorphism
        """String representation."""
        return f"{self.__class__.__name__}()"


class AnalyzerProtocol(Protocol):  # Protocol for polymorphism
    """Protocol for analyzer implementations."""
    
    def analyze(self, text: str) -> str:
        """Analyze text and return type."""
        ...


class AnalyzerFactory:  # Factory for polymorphism
    """Factory to create analyzer instances."""
    
    @staticmethod
    def create(analyzer_type: str) -> BaseAnalyzer:
        """Create analyzer - runtime polymorphism."""
        types: Dict[str, Type[BaseAnalyzer]] = {
            "pattern": PatternAnalyzer,
            "length": LengthAnalyzer,
            "hybrid": HybridAnalyzer
        }
        if analyzer_type not in types:
            raise ValueError(f"Unknown type: {analyzer_type}")
        return types[analyzer_type]()


class PatternAnalyzer(BaseAnalyzer):  # Inheritance
    """Pattern-based content analyzer."""

    def __init__(self) -> None:
        patterns = {  # Encapsulation
            "major_section": r"\b(Overview|References|Terms|Definitions)\b",
            "section_header": r"^\d+\.\d+",
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


class LengthAnalyzer(BaseAnalyzer):  # Polymorphism
    """Length-based content analyzer."""

    def analyze(self, text: str) -> str:  # Polymorphism
        length = len(text.strip())
        if length < 20:
            return "short_text"
        elif length > 200:
            return "long_content"
        return "medium_text"


class HybridAnalyzer(BaseAnalyzer):  # Polymorphism
    """Combines multiple analyzers."""

    def __init__(self):
        self._pattern = PatternAnalyzer()
        self._length = LengthAnalyzer()

    def analyze(self, text: str) -> str:  # Polymorphism
        pattern_result = self._pattern.analyze(text)
        if pattern_result != "paragraph":
            return pattern_result
        return self._length.analyze(text)
