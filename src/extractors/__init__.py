"""
Extractors Package (Enterprise Architecture)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.extractors.content_extractor import ContentExtractor
from src.extractors.extractor_interface import ExtractorInterface
from src.extractors.text_extractor import TextExtractor

if TYPE_CHECKING:
    pass

# ==========================================================
# PACKAGE METADATA
# ==========================================================

__version__ = "1.1.0"
__all__ = [
    "ContentExtractor",
    "TextExtractor",
    "get_available_extractors",
    "register_extractor",
]


# ==========================================================
# INTERNAL EXTRACTOR REGISTRY (Encapsulation)
# ==========================================================

# Protected registry for all extractors
_extractor_registry: dict[str, type[ExtractorInterface]] = {
    "content": ContentExtractor,
    "text": TextExtractor,
}


# ==========================================================
# PUBLIC API (Polymorphism + Encapsulation)
# ==========================================================

def get_available_extractors() -> list[str]:
    """
    Return list of available extractor names.

    Polymorphic:
        New extractors can be registered dynamically.
    """
    return list(_extractor_registry.keys())


def register_extractor(
    name: str, extractor_cls: type[ExtractorInterface]
) -> None:
    """
    Register a new extractor implementation.

    Example:
        register_extractor("image", ImageExtractor)

    Raises:
        ValueError if extractor name already exists.
    """
    if name in _extractor_registry:
        raise ValueError(f"Extractor {name!r} is already registered.")

    _extractor_registry[name] = extractor_cls


def get_extractor(name: str) -> type[ExtractorInterface]:
    """
    Retrieve extractor class by name.

    Polymorphism:
        Any class implementing ExtractionStrategy can be stored here.
    """
    if name not in _extractor_registry:
        raise KeyError(f"No extractor registered under: {name}")

    return _extractor_registry[name]
