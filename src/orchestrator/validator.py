"""
Enterprise Validator Module (OOP + Encapsulation + Overloading + Polymorphism)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import overload

from src.core.config.models import ContentItem, ParserResult, TOCEntry
from src.core.interfaces.pipeline_interface import ValidationResult

# ================================================================
# BASE VALIDATOR (ABSTRACTION + POLYMORPHISM)
# ================================================================

class BaseValidator(ABC):
    """Abstract base validator for parser results."""

    @property
    @abstractmethod
    def validator_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def validate(self, data: ParserResult) -> ValidationResult:
        raise NotImplementedError

    # ---------- Polymorphic Helper ----------
    def validator_name(self) -> str:
        return self.__class__.__name__

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        return f"{self.validator_type}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return 1

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseValidator):
            return NotImplemented
        return self.validator_type < other.validator_type

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, item: str) -> bool:
        return item in self.validator_type

    def __int__(self) -> int:
        return 1

    def __float__(self) -> float:
        return 1.0


# ================================================================
# RESULT VALIDATOR (INHERITANCE + OVERLOADING + ENCAPSULATION)
# ================================================================

class ResultValidator(BaseValidator):
    """Validates parser results for TOC OR Content availability."""

    def __init__(self) -> None:
        self.__count = 0  # encapsulated counter

    # ---------- Polymorphism ----------
    @property
    def validator_type(self) -> str:
        return "ResultValidator"

    # ---------- Encapsulated Properties ----------
    @property
    def validation_count(self) -> int:
        return self.__count

    def _increment(self) -> None:
        self.__count += 1

    # ============================================================
    # METHOD OVERLOADING FOR validate()
    # ============================================================

    @overload
    def validate(self, data: ParserResult) -> ValidationResult: ...

    @overload
    def validate(
        self, data: ParserResult, *, strict: bool
    ) -> ValidationResult: ...

    def validate(  # type: ignore[override]
        self, data: ParserResult, *, strict: bool = False
    ) -> ValidationResult:
        """
        validate(result)
        validate(result, strict=True)
        """
        self._increment()
        errors: list[str] = []

        if strict:
            if not data.toc_entries:
                errors.append("Missing TOC entries (strict mode)")
            if not data.content_items:
                errors.append("Missing content items (strict mode)")
        elif not data.toc_entries and not data.content_items:
            errors.append("No TOC entries or content items found")

        return ValidationResult(is_valid=(not errors), errors=errors)

    # ============================================================
    # OVERLOADED TOC VALIDATION
    # ============================================================

    @overload
    def validate_toc(self, entries: list[TOCEntry]) -> bool: ...

    @overload
    def validate_toc(
        self, entries: list[TOCEntry], *, min_items: int
    ) -> bool: ...

    def validate_toc(
        self, entries: list[TOCEntry], *, min_items: int = 1
    ) -> bool:
        return len(entries) >= min_items

    # ============================================================
    # OVERLOADED CONTENT VALIDATION
    # ============================================================

    @overload
    def validate_content(self, items: list[ContentItem]) -> bool: ...

    @overload
    def validate_content(
        self, items: list[ContentItem], *, min_items: int
    ) -> bool: ...

    def validate_content(
        self, items: list[ContentItem], *, min_items: int = 1
    ) -> bool:
        return len(items) >= min_items

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        return "ResultValidator(requires_toc_or_content)"

    def __repr__(self) -> str:
        return "ResultValidator()"

    def __len__(self) -> int:
        return self.__count

    def __bool__(self) -> bool:
        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ResultValidator):
            return NotImplemented
        return self.__count < other.__count

    def __int__(self) -> int:
        return self.__count

    def __float__(self) -> float:
        return float(self.__count)

    def __call__(self, data: ParserResult) -> ValidationResult:
        """Make validator callable."""
        return self.validate(data)

    def __iter__(self):
        """Iterate over validation methods."""
        return iter(["validate", "validate_toc", "validate_content"])


# ================================================================
# STRICT VALIDATOR (OVERRIDING)
# ================================================================

class StrictValidator(ResultValidator):
    """Strict validator requiring BOTH TOC AND Content."""

    def __init__(self) -> None:
        super().__init__()
        self.__strict = True

    @property
    def validator_type(self) -> str:
        return "StrictValidator"

    @property
    def strict_mode(self) -> bool:
        return self.__strict

    # ------------ Override validate() (Polymorphism) ------------
    def validate(self, data: ParserResult) -> ValidationResult:  # type: ignore[override]
        """
        Strict override → always strict=True
        """
        return super().validate(data, strict=True)

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        return "StrictValidator(requires_both_toc_and_content)"

    def __repr__(self) -> str:
        return "StrictValidator()"

    def __bool__(self) -> bool:
        return self.__strict

    def __contains__(self, item: str) -> bool:
        return item in "strict"

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __getitem__(self, index: int) -> str:
        return "strict"[index]
