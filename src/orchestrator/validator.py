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

    def __init__(self) -> None:
        self.__validation_count = 0

    @property
    def validation_count(self) -> int:
        """Get validation count."""
        return self.__validation_count

    @property
    def has_validated(self) -> bool:
        """Check if has validated."""
        return self.__validation_count > 0

    def _increment_validation(self) -> None:
        """Increment validation counter."""
        self.__validation_count += 1

    def __str__(self) -> str:
        """String representation."""
        return "ResultValidator(requires_toc_or_content)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return "ResultValidator()"

    def validate(self, data: ParserResult) -> ValidationResult:
        """Validate parser result has at least TOC entries or content items."""
        self._increment_validation()
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

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultValidator)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __len__(self) -> int:
        return self.__validation_count

    def __bool__(self) -> bool:
        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ResultValidator):
            return NotImplemented
        return self.__validation_count < other.__validation_count

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __int__(self) -> int:
        return self.__validation_count

    def __float__(self) -> float:
        return float(self.__validation_count)


class StrictValidator(ResultValidator):
    """Strict validator requiring both TOC entries and content items."""

    def __init__(self) -> None:
        super().__init__()
        self.__strict_mode = True

    @property
    def strict_mode(self) -> bool:
        """Get strict mode."""
        return self.__strict_mode

    def __str__(self) -> str:
        """String representation."""
        return "StrictValidator(requires_both_toc_and_content)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return "StrictValidator()"

    def validate(self, data: ParserResult) -> ValidationResult:
        """Validate that both TOC entries and content items exist."""
        self._increment_validation()
        errors: list[str] = []
        if not data.toc_entries:
            errors.append("No TOC entries found")
        if not data.content_items:
            errors.append("No content items found")
        return ValidationResult(is_valid=not errors, errors=errors)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, StrictValidator)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, StrictValidator):
            return NotImplemented
        return self.validation_count < other.validation_count
