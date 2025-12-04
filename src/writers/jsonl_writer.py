"""JSONL writer implementation (OOP enhanced)."""

from __future__ import annotations

import json
from abc import ABC
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, TypeVar, cast

from src.core.config.models import ContentItem, TOCEntry
from src.writers.writer_interface import WriterInterface

T = TypeVar("T", TOCEntry, ContentItem)


class JSONLWriter(WriterInterface, ABC):
    """Writes TOC and Content to JSONL files with improved OOP principles."""

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    def __init__(self, doc_title: str) -> None:
        """Method implementation."""
        self.__doc_title = doc_title

    # -------------------------------------------------------------------------
    # Encapsulated Properties
    # -------------------------------------------------------------------------
    @property
    def writer_type(self) -> str:
        """Method implementation."""
        return "JSONL"

    @property
    def doc_title(self) -> str:
        """Method implementation."""
        return self.__doc_title

    @property
    def title_length(self) -> int:
        """Method implementation."""
        return len(self.__doc_title)

    @property
    def has_title(self) -> bool:
        """Method implementation."""
        return bool(self.__doc_title)

    @property
    def title_words(self) -> int:
        """Method implementation."""
        return len(self.__doc_title.split())

    @property
    def title_chars(self) -> int:
        """Method implementation."""
        return len(self.__doc_title)

    @property
    def title_upper(self) -> str:
        """Method implementation."""
        return self.__doc_title.upper()

    @property
    def title_lower(self) -> str:
        """Method implementation."""
        return self.__doc_title.lower()

    @property
    def title_capitalized(self) -> str:
        """Method implementation."""
        return self.__doc_title.capitalize()

    @property
    def title_stripped(self) -> str:
        """Method implementation."""
        return self.__doc_title.strip()

    @property
    def title_is_empty(self) -> bool:
        """Method implementation."""
        return not self.__doc_title.strip()

    @property
    def title_first_char(self) -> str:
        """Method implementation."""
        return self.__doc_title[0] if self.__doc_title else ""

    @property
    def title_last_char(self) -> str:
        """Method implementation."""
        return self.__doc_title[-1] if self.__doc_title else ""

    # -------------------------------------------------------------------------
    # High-level Writer (Abstraction)
    # -------------------------------------------------------------------------
    def write(  # type: ignore[override]
        self, data: list[TOCEntry | ContentItem], path: Path
    ) -> None:
        """Generic write orchestrator."""
        if not data:
            raise ValueError("Cannot write empty data.")

        self._before_write(path)

        if isinstance(data[0], TOCEntry):
            self.write_toc(cast(list[TOCEntry], data), path)
        else:
            self.write_content(cast(list[ContentItem], data), path)

        self._after_write(path)

    # -------------------------------------------------------------------------
    # Template Methods (Polymorphism)
    # -------------------------------------------------------------------------
    def write_toc(self, entries: list[TOCEntry], path: Path) -> None:
        """Method implementation."""
        self._write_jsonl(entries, path, self._serialize_toc)

    def write_content(self, items: list[ContentItem], path: Path) -> None:
        """Method implementation."""
        self._write_jsonl(items, path, self._serialize_content)

    # -------------------------------------------------------------------------
    # Core Writer Logic (Encapsulation)
    # -------------------------------------------------------------------------
    def _write_jsonl(
        self,
        data: Iterable[T],
        path: Path,
        serializer: Callable[[T], dict[str, Any]]
    ) -> None:
        """Write serialized JSON lines to file."""
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(serializer(item)) + "\n")

    # -------------------------------------------------------------------------
    # Hooks (Polymorphic extension points)
    # -------------------------------------------------------------------------
    def _before_write(self, path: Path) -> None:
        """Method implementation."""
        pass

    def _after_write(self, path: Path) -> None:
        """Method implementation."""
        pass

    # -------------------------------------------------------------------------
    # Serialization Layer — FINAL & CORRECT VERSION
    # -------------------------------------------------------------------------
    def _serialize_toc(self, entry: TOCEntry) -> dict[str, Any]:
        """Method implementation."""
        return {
            "doc_title": self.__doc_title,
            "section_id": entry.section_id,
            "title": entry.title,
            "full_path": entry.full_path or entry.title,
            "page": entry.page,
            "level": entry.level,
            "parent_id": entry.parent_id,
            "tags": [],
        }

    def _serialize_content(self, item: ContentItem) -> dict[str, Any]:
        """Serialize ContentItem into JSON-safe dict. (MATCHED WITH MODEL)"""
        return {
            "doc_title": item.doc_title,
            "section_id": item.section_id,
            "title": item.title,
            "content": item.content,
            "page": item.page,
            "level": item.level,
            "parent_id": item.parent_id,
            "full_path": item.full_path,
            "content_type": item.content_type,   # CORRECT FIELD
            "block_id": item.block_id,
            "bbox": item.bbox,
        }

    # -------------------------------------------------------------------------
    # Magic / Dunder Methods
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """Method implementation."""
        return f"JSONLWriter(doc_title={self.__doc_title})"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"JSONLWriter(doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return (
            isinstance(other, JSONLWriter)
            and self.__doc_title == other.__doc_title
        )

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((type(self).__name__, self.__doc_title))

    def __len__(self) -> int:
        """Method implementation."""
        return len(self.__doc_title)

    def __bool__(self) -> bool:
        """Method implementation."""
        return bool(self.__doc_title)

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        return (
            isinstance(other, JSONLWriter)
            and self.__doc_title < other.__doc_title
        )

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return self.__doc_title[index]

    def __contains__(self, text: str) -> bool:
        """Method implementation."""
        return text.lower() in self.__doc_title.lower()

    def __enter__(self) -> "JSONLWriter":
        """Method implementation."""
        return self

    def __int__(self) -> int:
        """Method implementation."""
        return len(self.__doc_title)

    def __float__(self) -> float:
        """Method implementation."""
        return float(len(self.__doc_title))

    def __call__(self, data: list[TOCEntry | ContentItem], path: Path) -> None:
        """Make writer callable."""
        return self.write(data, path)

    def __iter__(self):
        """Iterate over doc_title characters."""
        return iter(self.__doc_title)

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, JSONLWriter):
            return NotImplemented
        return self.__doc_title > other.__doc_title

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other

    def __add__(self, other: str) -> str:
        """Method implementation."""
        return self.__doc_title + other

    def __mul__(self, other: int) -> str:
        """Method implementation."""
        return self.__doc_title * other

    def __mod__(self, other: str) -> str:
        """Method implementation."""
        return self.__doc_title % other

    def __pow__(self, other: int) -> int:
        """Method implementation."""
        return int(len(self.__doc_title) ** other)
