"""Validator for parsing results."""

from abc import ABC, abstractmethod

from src.core.config.models import ContentItem, ParserResult, TOCEntry
from src.core.interfaces.pipeline_interface import ValidationResult


class BaseValidator(ABC):
    """Abstract base validator for parser results."""

    @abstractmethod
    def validate(self, data: ParserResult) -> ValidationResult:
        """Validate parser result and return detailed validation result."""


class ResultValidator(BaseValidator):
    """Validates parser results have at least TOC or content data."""

    def validate(self, data: ParserResult) -> ValidationResult:
        """Validate parser result has at least TOC entries or content items."""
        errors: list[str] = []
        if not data.toc_entries and not data.content_items:
            errors.append("No TOC entries or content items found")
        return ValidationResult(is_valid=not errors, errors=errors)

    def validate_toc(self, entries: list[TOCEntry]) -> bool:
        """Check if TOC entries list is non-empty."""
        return bool(entries)

    def validate_content(self, items: list[ContentItem]) -> bool:
        """Check if content items list is non-empty."""
        return bool(items)


class StrictValidator(ResultValidator):
    """Strict validator requiring both TOC entries and content items."""

    def validate(self, data: ParserResult) -> ValidationResult:
        """Validate that both TOC entries and content items exist."""
        errors: list[str] = []
        if not data.toc_entries:
            errors.append("No TOC entries found")
        if not data.content_items:
            errors.append("No content items found")
        return ValidationResult(is_valid=not errors, errors=errors)
