"""Data models using dataclasses."""

from dataclasses import dataclass, field
from typing import Union


@dataclass
class TOCEntry:
    """Table of Contents entry."""

    section_id: str
    title: str
    page: int
    level: int = 1
    parent_id: Union[str, None] = None
    full_path: str = ""

    @property
    def is_top_level(self) -> bool:
        """Check if top-level entry."""
        return self.level == 1

    @property
    def has_parent(self) -> bool:
        """Check if has parent."""
        return self.parent_id is not None

    @property
    def title_length(self) -> int:
        """Get title length."""
        return len(self.title)

    @property
    def has_full_path(self) -> bool:
        """Check if has full path."""
        return bool(self.full_path)

    def __str__(self) -> str:
        return f"TOCEntry({self.section_id}: {self.title})"

    def __repr__(self) -> str:
        return f"TOCEntry(section_id={self.section_id!r}, title={self.title!r}, page={self.page})"

    def __bool__(self) -> bool:
        return bool(self.section_id and self.title)

    def __len__(self) -> int:
        return len(self.title)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TOCEntry):
            return NotImplemented
        return self.section_id == other.section_id and self.page == other.page

    def __hash__(self) -> int:
        return hash((self.section_id, self.page))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TOCEntry):
            return NotImplemented
        return (self.page, self.section_id) < (other.page, other.section_id)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __int__(self) -> int:
        return self.page

    def __float__(self) -> float:
        return float(self.page)


@dataclass
class ContentItem:
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
    bbox: list[float] = field(default_factory=lambda: [])  # [x1, y1, x2, y2]

    @property
    def word_count(self) -> int:
        """Get word count."""
        return len(self.content.split())

    @property
    def is_empty(self) -> bool:
        """Check if content is empty."""
        return not self.content.strip()

    @property
    def has_bbox(self) -> bool:
        """Check if has bounding box."""
        return len(self.bbox) > 0

    @property
    def title_length(self) -> int:
        """Get title length."""
        return len(self.title)

    @property
    def has_parent(self) -> bool:
        """Check if has parent."""
        return self.parent_id is not None

    def __str__(self) -> str:
        return f"ContentItem({self.section_id}: {self.title[:50]}...)"

    def __repr__(self) -> str:
        return f"ContentItem(section_id={self.section_id!r}, page={self.page})"

    def __bool__(self) -> bool:
        return bool(self.content)

    def __len__(self) -> int:
        return len(self.content)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContentItem):
            return NotImplemented
        return self.block_id == other.block_id and self.page == other.page

    def __hash__(self) -> int:
        return hash((self.block_id, self.page))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ContentItem):
            return NotImplemented
        return (self.page, self.block_id) < (other.page, other.block_id)

    def __contains__(self, text: str) -> bool:
        return text.lower() in self.content.lower()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, ContentItem):
            return NotImplemented
        return self == other or self < other

    def __int__(self) -> int:
        return self.page

    def __float__(self) -> float:
        return float(self.page)


@dataclass
class Metadata:
    """Metadata for parsing results."""

    total_pages: int = 0
    total_toc_entries: int = 0
    total_content_items: int = 0
    toc_levels: dict[str, int] = field(default_factory=lambda: {})
    content_types: dict[str, int] = field(default_factory=lambda: {})

    @property
    def total_items(self) -> int:
        """Get total items."""
        return self.total_toc_entries + self.total_content_items

    @property
    def has_content(self) -> bool:
        """Check if has content."""
        return self.total_pages > 0

    @property
    def has_toc(self) -> bool:
        """Check if has TOC entries."""
        return self.total_toc_entries > 0

    @property
    def has_items(self) -> bool:
        """Check if has content items."""
        return self.total_content_items > 0

    def __str__(self) -> str:
        return f"Metadata(pages={self.total_pages}, toc={self.total_toc_entries}, content={self.total_content_items})"

    def __repr__(self) -> str:
        return f"Metadata(total_pages={self.total_pages}, total_toc_entries={self.total_toc_entries}, total_content_items={self.total_content_items})"

    def __len__(self) -> int:
        return self.total_toc_entries + self.total_content_items

    def __bool__(self) -> bool:
        return self.total_pages > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Metadata):
            return NotImplemented
        return self.total_pages == other.total_pages

    def __hash__(self) -> int:
        return hash((self.total_pages, self.total_toc_entries, self.total_content_items))

    def __int__(self) -> int:
        return self.total_pages

    def __float__(self) -> float:
        return float(self.total_pages)


@dataclass
class ParserResult:
    """Result from parser execution."""

    toc_entries: list[TOCEntry] = field(default_factory=lambda: [])
    content_items: list[ContentItem] = field(default_factory=lambda: [])
    metadata: Metadata = field(default_factory=Metadata)

    @property
    def total_entries(self) -> int:
        """Get total entries."""
        return len(self.toc_entries)

    @property
    def total_content(self) -> int:
        """Get total content items."""
        return len(self.content_items)

    @property
    def is_empty(self) -> bool:
        """Check if result is empty."""
        return not self.toc_entries and not self.content_items

    @property
    def has_toc(self) -> bool:
        """Check if has TOC."""
        return bool(self.toc_entries)

    @property
    def has_content(self) -> bool:
        """Check if has content."""
        return bool(self.content_items)

    def __len__(self) -> int:
        """Return total number of items (TOC + content)."""
        return len(self.toc_entries) + len(self.content_items)

    def __str__(self) -> str:
        return f"ParserResult(toc={len(self.toc_entries)}, content={len(self.content_items)})"

    def __repr__(self) -> str:
        return f"ParserResult(toc_entries={len(self.toc_entries)}, content_items={len(self.content_items)})"

    def __bool__(self) -> bool:
        return bool(self.toc_entries or self.content_items)

    def __iter__(self):
        """Iterate over all entries."""
        yield from self.toc_entries
        yield from self.content_items

    def __contains__(self, item) -> bool:
        """Check if item in results."""
        return item in self.toc_entries or item in self.content_items

    def __getitem__(self, index: int):
        """Get item by index."""
        total = len(self.toc_entries)
        if index < total:
            return self.toc_entries[index]
        return self.content_items[index - total]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParserResult):
            return NotImplemented
        return len(self) == len(other)

    def __hash__(self) -> int:
        return hash((len(self.toc_entries), len(self.content_items)))

    def __int__(self) -> int:
        return len(self)

    def __float__(self) -> float:
        return float(len(self))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ParserResult):
            return NotImplemented
        return len(self) < len(other)
