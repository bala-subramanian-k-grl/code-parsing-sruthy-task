"""Data models using dataclasses."""

from dataclasses import dataclass, field


@dataclass
class TOCEntry:
    """Table of Contents entry."""

    section_id: str
    title: str
    page: int
    level: int = 1
    parent_id: str | None = None
    full_path: str = ""


@dataclass
class ContentItem:
    """Content item from PDF."""

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
    bbox: list[float] = field(default_factory=lambda: [])  # Bounding box [x1, y1, x2, y2]


@dataclass
class Metadata:
    """Metadata for parsing results."""

    total_pages: int = 0
    total_toc_entries: int = 0
    total_content_items: int = 0
    toc_levels: dict[str, int] = field(default_factory=lambda: {})
    content_types: dict[str, int] = field(default_factory=lambda: {})


@dataclass
class ParserResult:
    """Result from parser execution."""

    toc_entries: list[TOCEntry] = field(default_factory=lambda: [])
    content_items: list[ContentItem] = field(default_factory=lambda: [])
    metadata: Metadata = field(default_factory=Metadata)
