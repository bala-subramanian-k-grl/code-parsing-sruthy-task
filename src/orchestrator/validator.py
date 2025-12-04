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
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, data: ParserResult) -> ValidationResult:
        """Method implementation."""
        raise NotImplementedError

    # ---------- Polymorphic Helper ----------
    def validator_name(self) -> str:
        """Method implementation."""
        return self.__class__.__name__

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.validator_type}"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __len__(self) -> int:
        """Method implementation."""
        return 1

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, BaseValidator):
            return NotImplemented
        return self.validator_type < other.validator_type

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in self.validator_type

    def __int__(self) -> int:
        """Method implementation."""
        return 1

    def __float__(self) -> float:
        """Method implementation."""
        return 1.0


# ================================================================
# RESULT VALIDATOR (INHERITANCE + OVERLOADING + ENCAPSULATION)
# ================================================================

class ResultValidator(BaseValidator, ABC):
    """Abstract validator for parser results with configurable strictness."""

    def __init__(self) -> None:
        """Method implementation."""
        self.__count = 0  # encapsulated counter

    # ---------- Polymorphism ----------
    @property
    def validator_type(self) -> str:
        """Method implementation."""
        return "ResultValidator"

    # ---------- Encapsulated Properties ----------
    @property
    def validation_count(self) -> int:
        """Method implementation."""
        return self.__count

    def _increment(self) -> None:
        """Method implementation."""
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

    def validate(
        self, data: ParserResult, *, strict: bool = False
    ) -> ValidationResult:
        """Validate parser result."""
        self._increment()
        if strict:
            errors = self._check_strict(data)
        else:
            errors = self._check_any(data)
        return ValidationResult(is_valid=(not errors), errors=errors)

    def _check_strict(self, data: ParserResult) -> list[str]:
        """Check strict mode: both TOC and content required."""
        errors: list[str] = []
        if not data.toc_entries:
            errors.append("Missing TOC entries (strict mode)")
        if not data.content_items:
            errors.append("Missing content items (strict mode)")
        return errors

    def _check_any(self, data: ParserResult) -> list[str]:
        """Check any mode: TOC or content required."""
        if not data.toc_entries and not data.content_items:
            return ["No TOC entries or content items found"]
        return []

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
        """Method implementation."""
        return "ResultValidator(requires_toc_or_content)"

    def __repr__(self) -> str:
        """Method implementation."""
        return "ResultValidator()"

    def __len__(self) -> int:
        """Method implementation."""
        return self.__count

    def __bool__(self) -> bool:
        """Method implementation."""
        return True

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, ResultValidator):
            return NotImplemented
        return self.__count < other.__count

    def __int__(self) -> int:
        """Method implementation."""
        return self.__count

    def __float__(self) -> float:
        """Method implementation."""
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

class StrictValidator(ResultValidator, ABC):
    """Strict validator requiring BOTH TOC AND Content."""

    def __init__(self) -> None:
        """Method implementation."""
        super().__init__()
        self.__strict = True

    @property
    def validator_type(self) -> str:
        """Method implementation."""
        return "StrictValidator"

    @property
    def strict_mode(self) -> bool:
        """Method implementation."""
        return self.__strict

    # ------------ Override validate() (Polymorphism) ------------
    @overload
    def validate(self, data: ParserResult) -> ValidationResult: ...

    @overload
    def validate(
        self, data: ParserResult, *, strict: bool
    ) -> ValidationResult: ...

    def validate(
        self, data: ParserResult, *, strict: bool = True
    ) -> ValidationResult:
        """
        Strict override → always strict=True
        """
        return super().validate(data, strict=True)

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        """Method implementation."""
        return "StrictValidator(requires_both_toc_and_content)"

    def __repr__(self) -> str:
        """Method implementation."""
        return "StrictValidator()"

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.__strict

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in "strict"

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return "strict"[index]
