"""
Enterprise-level data models.
Clean, minimal, and professionally structured.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

# ======================================================================
# ABSTRACT BASE MODEL
# ======================================================================


class BaseModel(ABC):
    """
    Abstract base class for all models.
    Enforces:
        - validate()
        - summary()
        - item_type()
    """

    @abstractmethod
    def validate(self) -> None:
        """Validate the model's fields."""
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        """Short description of model."""
        raise NotImplementedError

    @abstractmethod
    def item_type(self) -> str:
        """Return identifying model type."""
        raise NotImplementedError

    # -------- Meaningful magic methods --------
    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.item_type()}: {self.summary()}"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(self.__class__.__name__)


# ======================================================================
# TOC ENTRY MODEL
# ======================================================================

@dataclass
class TOCEntry(BaseModel):
    section_id: str
    title: str
    page: int
    level: int = 1
    parent_id: str | None = None
    full_path: str = ""

    # -------- Polymorphic behavior --------
    def validate(self) -> None:
        """Method implementation."""
        if not self.section_id:
            raise ValueError("section_id cannot be empty")
        if self.page < 0:
            raise ValueError("page must be >= 0")

    def summary(self) -> str:
        """Method implementation."""
        return f"{self.title} (page={self.page}, level={self.level})"

    def item_type(self) -> str:
        """Method implementation."""
        return "TOCEntry"

    # -------- Encapsulated helpers --------
    @property
    def is_top_level(self) -> bool:
        """Method implementation."""
        return self.level == 1

    @property
    def has_parent(self) -> bool:
        """Method implementation."""
        return self.parent_id is not None

    # -------- Minimal magic methods --------
    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, TOCEntry):
            return NotImplemented
        return self.page < other.page


# ======================================================================
# CONTENT ITEM MODEL
# ======================================================================

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
    bbox: list[float] = field(default_factory=list)

    # -------- Polymorphic behavior --------
    def validate(self) -> None:
        """Method implementation."""
        if not self.title:
            raise ValueError("title cannot be empty")
        if self.page < 0:
            raise ValueError("page must be >= 0")

    def summary(self) -> str:
        """Method implementation."""
        preview = self.content[:50] + ("..." if len(self.content) > 50 else "")
        return f"{self.title} → {preview}"

    def item_type(self) -> str:
        """Method implementation."""
        return "ContentItem"

    # -------- Encapsulated helpers --------
    @property
    def word_count(self) -> int:
        """Method implementation."""
        return len(self.content.split())

    @property
    def is_empty(self) -> bool:
        """Method implementation."""
        return not self.content.strip()

    @property
    def has_bbox(self) -> bool:
        """Method implementation."""
        return bool(self.bbox)

    # -------- Minimal magic method --------
    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, ContentItem):
            return NotImplemented
        return self.page < other.page


# ======================================================================
# METADATA MODEL
# ======================================================================

@dataclass
class Metadata(BaseModel):
    total_pages: int = 0
    total_toc_entries: int = 0
    total_content_items: int = 0
    toc_levels: dict[str, int] = field(default_factory=dict)
    content_types: dict[str, int] = field(default_factory=dict)

    def validate(self) -> None:
        """Method implementation."""
        if self.total_pages < 0:
            raise ValueError("total_pages must be >= 0")

    def summary(self) -> str:
        """Method implementation."""
        return (
            f"pages={self.total_pages}, "
            f"toc={self.total_toc_entries}, "
            f"content={self.total_content_items}"
        )

    def item_type(self) -> str:
        """Method implementation."""
        return "Metadata"

    @property
    def total_items(self) -> int:
        """Method implementation."""
        return self.total_toc_entries + self.total_content_items

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.total_pages > 0


# ======================================================================
# PARSER RESULT MODEL
# ======================================================================

@dataclass
class ParserResult(BaseModel):
    toc_entries: list[TOCEntry] = field(default_factory=list)
    content_items: list[ContentItem] = field(default_factory=list)
    metadata: Metadata = field(default_factory=Metadata)

    def validate(self) -> None:
        """Method implementation."""
        for e in self.toc_entries:
            e.validate()
        for c in self.content_items:
            c.validate()
        self.metadata.validate()

    def summary(self) -> str:
        """Method implementation."""
        return (
            f"{len(self.toc_entries)} TOC entries, "
            f"{len(self.content_items)} content items"
        )

    def item_type(self) -> str:
        """Method implementation."""
        return "ParserResult"

    @property
    def is_empty(self) -> bool:
        """Method implementation."""
        return not self.toc_entries and not self.content_items

    def __len__(self) -> int:
        """Method implementation."""
        return len(self.toc_entries) + len(self.content_items)

    def __iter__(self) -> Iterator[TOCEntry | ContentItem]:
        """Method implementation."""
        yield from self.toc_entries
        yield from self.content_items

    def __contains__(self, item: Any) -> bool:
        """Method implementation."""
        return item in self.toc_entries or item in self.content_items
