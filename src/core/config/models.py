"""Enterprise-level data models using dataclasses and OOP principles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Iterator, Union


# ==========================================================
# 1. ABSTRACT BASE MODEL (ABSTRACTION + POLYMORPHISM)
# ==========================================================

class BaseModel(ABC):
    """
    Abstract base class for all models.

    Provides:
    - validate()  → polymorphic field validation
    - summary()   → polymorphic human-readable description
    - item_type() → polymorphic model identifier
    """

    @abstractmethod
    def validate(self) -> None:
        """Validate model fields."""
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        """Return model summary."""
        raise NotImplementedError

    @abstractmethod
    def item_type(self) -> str:
        """Return model type name."""
        raise NotImplementedError


# ==========================================================
# 2. TOCEntry MODEL (INHERITANCE + POLYMORPHISM)
# ==========================================================

@dataclass
class TOCEntry(BaseModel):
    """Table of Contents entry."""

    section_id: str
    title: str
    page: int
    level: int = 1
    parent_id: Union[str, None] = None
    full_path: str = ""

    # ---------------- Polymorphism Implementations ----------------
    def validate(self) -> None:
        if not self.section_id:
            raise ValueError("TOCEntry: section_id cannot be empty")
        if self.page < 0:
            raise ValueError("TOCEntry: page must be >= 0")

    def summary(self) -> str:
        return f"TOCEntry '{self.title}' (page {self.page}, level {self.level})"

    def item_type(self) -> str:
        return "TOCEntry"

    # ---------------- Existing methods ----------------
    @property
    def is_top_level(self) -> bool:
        return self.level == 1

    @property
    def has_parent(self) -> bool:
        return self.parent_id is not None

    @property
    def title_length(self) -> int:
        return len(self.title)

    @property
    def has_full_path(self) -> bool:
        return bool(self.full_path)

    def __str__(self) -> str:
        return f"TOCEntry({self.section_id}: {self.title})"


# ==========================================================
# 3. ContentItem MODEL (INHERITANCE + POLYMORPHISM)
# ==========================================================

@dataclass
class ContentItem(BaseModel):
    """Content item from PDF."""

    doc_title: str
    section_id: str
    title: str
    content: str
    page: int
    level: int = 1
    parent_id: Union[str, None] = None
    full_path: str = ""
    content_type: str = "paragraph"
    block_id: str = ""
    bbox: list[float] = field(default_factory=lambda: [])

    # ---------------- Polymorphism Implementations ----------------
    def validate(self) -> None:
        if not self.title:
            raise ValueError("ContentItem: title cannot be empty")
        if self.page < 0:
            raise ValueError("ContentItem: page must be >= 0")

    def summary(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"ContentItem '{self.title}' → {preview}"

    def item_type(self) -> str:
        return "ContentItem"

    # ---------------- Existing methods ----------------
    @property
    def word_count(self) -> int:
        return len(self.content.split())

    @property
    def is_empty(self) -> bool:
        return not self.content.strip()

    @property
    def has_bbox(self) -> bool:
        return len(self.bbox) > 0

    @property
    def title_length(self) -> int:
        return len(self.title)

    @property
    def has_parent(self) -> bool:
        return self.parent_id is not None

    def __str__(self) -> str:
        return f"ContentItem({self.section_id}: {self.title[:50]}...)"


# ==========================================================
# 4. Metadata MODEL (INHERITANCE + POLYMORPHISM)
# ==========================================================

@dataclass
class Metadata(BaseModel):
    """Metadata for parser results."""

    total_pages: int = 0
    total_toc_entries: int = 0
    total_content_items: int = 0
    toc_levels: dict[str, int] = field(default_factory=lambda: {})
    content_types: dict[str, int] = field(default_factory=lambda: {})

    # ---------------- Polymorphism Implementations ----------------
    def validate(self) -> None:
        if self.total_pages < 0:
            raise ValueError("Metadata: total_pages must be >= 0")

    def summary(self) -> str:
        return (
            f"Metadata: pages={self.total_pages}, "
            f"TOC={self.total_toc_entries}, "
            f"Content={self.total_content_items}"
        )

    def item_type(self) -> str:
        return "Metadata"

    # ---------------- Existing methods ----------------
    @property
    def total_items(self) -> int:
        return self.total_toc_entries + self.total_content_items

    @property
    def has_content(self) -> bool:
        return self.total_pages > 0

    @property
    def has_toc(self) -> bool:
        return self.total_toc_entries > 0

    @property
    def has_items(self) -> bool:
        return self.total_content_items > 0


# ==========================================================
# 5. ParserResult MODEL (INHERITANCE + POLYMORPHISM)
# ==========================================================

@dataclass
class ParserResult(BaseModel):
    """Result of parser execution."""

    toc_entries: list[TOCEntry] = field(default_factory=lambda: [])
    content_items: list[ContentItem] = field(default_factory=lambda: [])
    metadata: Metadata = field(default_factory=Metadata)

    # ---------------- Polymorphism Implementations ----------------
    def validate(self) -> None:
        for entry in self.toc_entries:
            entry.validate()
        for item in self.content_items:
            item.validate()

    def summary(self) -> str:
        return (
            f"ParserResult: "
            f"{len(self.toc_entries)} TOC entries, "
            f"{len(self.content_items)} content items"
        )

    def item_type(self) -> str:
        return "ParserResult"

    # ---------------- Existing methods ----------------
    @property
    def total_entries(self) -> int:
        return len(self.toc_entries)

    @property
    def total_content(self) -> int:
        return len(self.content_items)

    @property
    def is_empty(self) -> bool:
        return not self.toc_entries and not self.content_items

    def __len__(self) -> int:
        return len(self.toc_entries) + len(self.content_items)

    def __iter__(self) -> Iterator[Union[TOCEntry, ContentItem]]:
        yield from self.toc_entries
        yield from self.content_items

    def __contains__(self, item: Any) -> bool:
        return item in self.toc_entries or item in self.content_items
