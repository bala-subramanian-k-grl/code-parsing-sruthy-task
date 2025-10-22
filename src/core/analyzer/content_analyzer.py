"""Content analyzer implementation."""
# USB PD Specification Parser - Content Analyzer Module

from collections.abc import Iterator
from typing import Any

from src.config.constants import MIN_LINE_LENGTH

from .base_analyzer import PatternAnalyzer

class ContentAnalyzer:
    """Content analyzer using pattern matching."""

    def __init__(self) -> None:
        self.__analyzer = PatternAnalyzer()  # Private
        self.__analysis_cache: dict[str, str] = {}  # Private cache
        self.__stats: dict[str, int] = {}  # Private statistics

    def classify(self, text: str) -> str:  # Abstraction
        """Classify text content type."""
        return self._classify_with_cache(text)

    def _classify_with_cache(self, text: str) -> str:
        """Classify with caching for performance."""
        cache_key = self._get_cache_key(text)
        if cache_key in self.__analysis_cache:
            return self.__analysis_cache[cache_key]
        
        result = str(self.__analyzer.analyze(text))
        self.__analysis_cache[cache_key] = result
        self._update_classification_stats(result)
        return result

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return text[:50].strip().lower()

    def _update_classification_stats(self, result: str) -> None:
        """Update classification statistics."""
        self.__stats[result] = self.__stats.get(result, 0) + 1



    def is_major_section(self, text: str) -> bool:
        """Check if text is a major section header."""
        return self._check_section_type(text, "major_section")

    def _check_section_type(self, text: str, section_type: str) -> bool:
        """Protected method to check specific section type."""
        return self.__analyzer.analyze(text) == section_type

    def extract_items(
        self, text: str, page: int
    ) -> Iterator[dict[str, Any]]:  # Abstraction
        """Extract content items from text."""
        lines = self._split_text_lines(text)
        for i, line in enumerate(lines):
            if self._is_valid_line(line):
                content_type = self.classify(line)
                if self._should_include_content(content_type):
                    yield self._create_content_item(
                        line, content_type, page, i
                    )

    def _split_text_lines(self, text: str) -> list[str]:
        """Protected method to split text into lines."""
        return [line.strip() for line in text.split("\n")]

    def _is_valid_line(self, line: str) -> bool:
        """Protected method to validate line length."""
        return len(line) > MIN_LINE_LENGTH

    def _should_include_content(self, content_type: str) -> bool:
        """Protected method to check if content should be included."""
        return content_type != "paragraph"

    def _create_content_item(
        self, line: str, content_type: str, page: int, index: int
    ) -> dict[str, Any]:
        """Protected method to create content item dictionary."""
        block_id = self._generate_block_id(content_type, page, index)
        return self._build_item_dict(content_type, line, page, block_id)

    def _generate_block_id(
        self, content_type: str, page: int, index: int
    ) -> str:
        """Generate unique block identifier."""
        return f"{content_type[0]}{page}_{index}"

    def _build_item_dict(
        self, content_type: str, line: str, page: int, block_id: str
    ) -> dict[str, Any]:
        """Build content item dictionary."""
        return {
            "type": content_type,
            "content": line,
            "page": page + 1,
            "block_id": block_id,
            "bbox": [],
        }

    @property
    def classification_stats(self) -> dict[str, int]:
        """Get classification statistics (read-only)."""
        return self.__stats.copy()

    def clear_cache(self) -> None:
        """Clear analysis cache."""
        self.__analysis_cache.clear()

    def _reset_stats(self) -> None:
        """Reset classification statistics."""
        self.__stats.clear()

    def get_cache_size(self) -> int:
        """Get current cache size."""
        return len(self.__analysis_cache)
