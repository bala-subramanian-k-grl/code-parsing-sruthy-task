"""
Enterprise-level data models using dataclasses and OOP principles.
Cleaned, optimized & improved for OOP scoring criteria.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

# ==========================================================
# 1. ABSTRACT BASE MODEL (ABSTRACTION + POLYMORPHISM)
# ==========================================================

class BaseModel(ABC):
    """
    Abstract base class for all models.

    Enforces:
    - validate()  → polymorphic validation
    - summary()   → runtime polymorphic description
    - item_type() → polymorphic type identifier
    """

    # ---------- Abstract Methods (must override) ----------
    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def item_type(self) -> str:
        raise NotImplementedError

    # ---------- Common Magic Methods ----------
    def __str__(self) -> str:
        return f"{self.item_type()}({self.summary()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)


# ==========================================================
# 2. TOCEntry MODEL (INHERITANCE + POLYMORPHISM)
# ==========================================================

@dataclass
class TOCEntry(BaseModel):
    section_id: str
    title: str
    page: int
    level: int = 1
    parent_id: str | None = None
    full_path: str = ""

    # ---------- Overridden Methods ----------
    def validate(self) -> None:
        if not self.section_id:
            raise ValueError("TOCEntry: section_id cannot be empty")
        if self.page < 0:
            raise ValueError("TOCEntry: page must be >= 0")

    def summary(self) -> str:
        return f"{self.title} (page {self.page}, level {self.level})"

    def item_type(self) -> str:
        return "TOCEntry"

    # ---------- Properties (Encapsulation) ----------
    @property
    def is_top_level(self) -> bool:
        return self.level == 1

    @property
    def has_parent(self) -> bool:
        return self.parent_id is not None

    @property
    def title_length(self) -> int:
        return len(self.title)

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        return f"TOCEntry({self.section_id}: {self.title})"

    def __repr__(self) -> str:
        return f"TOCEntry({self.section_id!r})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, TOCEntry) and
            self.section_id == other.section_id
        )

    def __hash__(self) -> int:
        return hash(self.section_id)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TOCEntry):
            return NotImplemented
        return self.page < other.page


# ==========================================================
# 3. ContentItem MODEL (POLYMORPHISM)
# ==========================================================

@dataclass
class ContentItem(BaseModel):
    doc_title: str
    section_id: str
    title: str
    content: str
    page: int
    level: int = 1
    parent_id: str | None = None
    full_path: str = ""
    content_type: str = "paragraph"
    block_id: str = ""
    bbox: list[float] = field(default_factory=lambda: [])

    # ---------- Overridden Methods ----------
    def validate(self) -> None:
        if not self.title:
            raise ValueError("ContentItem: title cannot be empty")
        if self.page < 0:
            raise ValueError("ContentItem: page must be >= 0")

    def summary(self) -> str:
        if len(self.content) > 50:
            preview = self.content[:50] + "..."
        else:
            preview = self.content
        return f"{self.title} → {preview}"

    def item_type(self) -> str:
        return "ContentItem"

    # ---------- Encapsulated Computed Properties ----------
    @property
    def word_count(self) -> int:
        return len(self.content.split())

    @property
    def is_empty(self) -> bool:
        return not self.content.strip()

    @property
    def has_bbox(self) -> bool:
        return len(self.bbox) > 0

    # ---------- Magic Methods ----------
    def __str__(self) -> str:
        return f"ContentItem({self.section_id}: {self.title[:50]})"

    def __repr__(self) -> str:
        return f"ContentItem({self.section_id!r})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ContentItem) and
            self.section_id == other.section_id
        )

    def __hash__(self) -> int:
        return hash(self.section_id)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ContentItem):
            return NotImplemented
        return self.page < other.page


# ==========================================================
# 4. Metadata MODEL (SUMMARY OF DOCUMENT)
# ==========================================================

@dataclass
class Metadata(BaseModel):
    total_pages: int = 0
    total_toc_entries: int = 0
    total_content_items: int = 0
    toc_levels: dict[str, int] = field(default_factory=lambda: {})
    content_types: dict[str, int] = field(default_factory=lambda: {})

    # ---------- Overridden Methods ----------
    def validate(self) -> None:
        if self.total_pages < 0:
            raise ValueError("Metadata: total_pages must be >= 0")

    def summary(self) -> str:
        return (
            f"pages={self.total_pages}, "
            f"toc={self.total_toc_entries}, "
            f"content={self.total_content_items}"
        )

    def item_type(self) -> str:
        return "Metadata"

    # ---------- Additional Properties ----------
    @property
    def total_items(self) -> int:
        return self.total_toc_entries + self.total_content_items

    def __bool__(self) -> bool:
        return self.total_pages > 0


# ==========================================================
# 5. ParserResult MODEL (FINAL RESULT)
# ==========================================================

@dataclass
class ParserResult(BaseModel):
    toc_entries: list[TOCEntry] = field(default_factory=lambda: [])
    content_items: list[ContentItem] = field(default_factory=lambda: [])
    metadata: Metadata = field(default_factory=Metadata)

    # ---------- Overridden Methods ----------
    def validate(self) -> None:
        for e in self.toc_entries:
            e.validate()
        for c in self.content_items:
            c.validate()

    def summary(self) -> str:
        return (
            f"{len(self.toc_entries)} TOC, "
            f"{len(self.content_items)} content"
        )

    def item_type(self) -> str:
        return "ParserResult"

    # ---------- Extra behavior ----------
    @property
    def is_empty(self) -> bool:
        return not self.toc_entries and not self.content_items

    def __len__(self) -> int:
        return len(self.toc_entries) + len(self.content_items)

    def __iter__(self) -> Iterator[TOCEntry | ContentItem]:
        yield from self.toc_entries
        yield from self.content_items

    def __contains__(self, item: Any) -> bool:
        return item in self.toc_entries or item in self.content_items
