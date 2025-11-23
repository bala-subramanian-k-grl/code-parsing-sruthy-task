"""Validator for parsing results."""

from __future__ import annotations
from abc import ABC, abstractmethod

from src.core.config.models import ContentItem, ParserResult, TOCEntry
from src.core.interfaces.pipeline_interface import ValidationResult


# ==========================================================
# BASE VALIDATOR — Abstraction + Polymorphism
# ==========================================================

class BaseValidator(ABC):
    """Abstract base validator for parser results."""

    @property
    @abstractmethod
    def validator_type(self) -> str:
        """Polymorphic validator identifier."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, data: ParserResult) -> ValidationResult:
        """Validate parser result and return ValidationResult."""
        raise NotImplementedError

    def validator_name(self) -> str:
        """Return class name — polymorphism helper."""
        return self.__class__.__name__


# ==========================================================
# RESULT VALIDATOR — Inheritance + Encapsulation
# ==========================================================

class ResultValidator(BaseValidator):
    """Validates parser results have at least TOC or content data."""

    def __init__(self) -> None:
        self.__validation_count = 0

    # ---------------- Polymorphism ----------------

    @property
    def validator_type(self) -> str:
        return "ResultValidator"

    # ---------------- Encapsulation ---------------

    @property
    def validation_count(self) -> int:
        return self.__validation_count

    @property
    def has_validated(self) -> bool:
        return self.__validation_count > 0

    def _increment_validation(self) -> None:
        self.__validation_count += 1

    # ---------------- Main Validation --------------

    def validate(self, data: ParserResult) -> ValidationResult:
        self._increment_validation()

        errors: list[str] = []
        if not data.toc_entries and not data.content_items:
            errors.append("No TOC entries or content items found")

        return ValidationResult(is_valid=not errors, errors=errors)

    # ---------------- Helper Checks ----------------

    def validate_toc(self, entries: list[TOCEntry]) -> bool:
        return bool(entries)

    def validate_content(self, items: list[ContentItem]) -> bool:
        return bool(items)

    # ---------------- Magic Methods ----------------

    def __str__(self) -> str:
        return "ResultValidator(requires_toc_or_content)"

    def __repr__(self) -> str:
        return "ResultValidator()"

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


# ==========================================================
# STRICT VALIDATOR — Inheritance + Method Override
# ==========================================================

class StrictValidator(ResultValidator):
    """Strict validator requiring both TOC entries and content items."""

    def __init__(self) -> None:
        super().__init__()
        self.__strict_mode = True

    # ---------------- Polymorphism ----------------

    @property
    def validator_type(self) -> str:
        return "StrictValidator"

    @property
    def strict_mode(self) -> bool:
        return self.__strict_mode

    # ---------------- Override Validation ---------

    def validate(self, data: ParserResult) -> ValidationResult:
        self._increment_validation()

        errors: list[str] = []
        if not data.toc_entries:
            errors.append("No TOC entries found")
        if not data.content_items:
            errors.append("No content items found")

        return ValidationResult(is_valid=not errors, errors=errors)

    # ---------------- Magic Methods ---------------

    def __str__(self) -> str:
        return "StrictValidator(requires_both_toc_and_content)"

    def __repr__(self) -> str:
        return "StrictValidator()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, StrictValidator)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, StrictValidator):
            return NotImplemented
        return self.validation_count < other.validation_count
