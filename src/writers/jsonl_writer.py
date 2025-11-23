"""JSONL writer implementation (OOP enhanced)."""

import json
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar, Union, cast

from src.core.config.models import ContentItem, TOCEntry
from src.writers.writer_interface import WriterInterface

T = TypeVar("T", TOCEntry, ContentItem)


class JSONLWriter(WriterInterface):
    """Writes TOC and Content to JSONL files with improved OOP principles."""

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    def __init__(self, doc_title: str) -> None:
        self.__doc_title = doc_title

    # -------------------------------------------------------------------------
    # Encapsulated Properties
    # -------------------------------------------------------------------------
    @property
    def doc_title(self) -> str:
        return self.__doc_title

    @property
    def title_length(self) -> int:
        return len(self.__doc_title)

    @property
    def has_title(self) -> bool:
        return bool(self.__doc_title)

    @property
    def title_words(self) -> int:
        return len(self.__doc_title.split())

    @property
    def title_chars(self) -> int:
        return len(self.__doc_title)

    @property
    def title_upper(self) -> str:
        return self.__doc_title.upper()

    # -------------------------------------------------------------------------
    # High-level Writer (Abstraction)
    # -------------------------------------------------------------------------
    def write(
        self, data: list[Union[TOCEntry, ContentItem]], path: Path
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
        self._write_jsonl(entries, path, self._serialize_toc)

    def write_content(self, items: list[ContentItem], path: Path) -> None:
        self._write_jsonl(items, path, self._serialize_content)

    # -------------------------------------------------------------------------
    # Core Writer Logic (Encapsulation + Template Method)
    # -------------------------------------------------------------------------
    def _write_jsonl(
        self,
        data: Iterable[T],
        path: Path,
        serializer: Callable[[T], dict[str, Any]]
    ) -> None:
        """Write serialized JSON lines to file."""

        # Prepare directory (Encapsulation)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(serializer(item)) + "\n")

    # -------------------------------------------------------------------------
    # Hooks (Polymorphic extension points)
    # -------------------------------------------------------------------------
    def _before_write(self, path: Path) -> None:
        """Hook before writing. Subclasses can override."""
        pass

    def _after_write(self, path: Path) -> None:
        """Hook after writing. Subclasses can override."""
        pass

    # -------------------------------------------------------------------------
    # Serialization Layer
    # -------------------------------------------------------------------------
    def _serialize_toc(self, entry: TOCEntry) -> dict[str, Any]:
        return {
            "doc_title": self.__doc_title,
            "section_id": entry.section_id,
            "title": entry.title,
            "full_path": entry.title,
            "page": entry.page,
            "level": entry.level,
            "parent_id": entry.parent_id,
            "tags": [],
        }

    def _serialize_content(self, item: ContentItem) -> dict[str, Any]:
        return {
            "doc_title": item.doc_title,
            "section_id": item.section_id,
            "title": item.title,
            "content": item.content,
            "page": item.page,
            "level": item.level,
            "parent_id": item.parent_id,
            "full_path": item.full_path,
            "type": item.content_type,
            "block_id": item.block_id,
            "bbox": item.bbox,
        }

    # -------------------------------------------------------------------------
    # Magic / Dunder Methods (Your same logic kept)
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"JSONLWriter(doc_title={self.__doc_title})"

    def __repr__(self) -> str:
        return f"JSONLWriter(doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, JSONLWriter) and self.__doc_title == other.__doc_title

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__doc_title))

    def __len__(self) -> int:
        return len(self.__doc_title)

    def __bool__(self) -> bool:
        return bool(self.__doc_title)

    def __lt__(self, other: object) -> bool:
        return isinstance(other, JSONLWriter) and self.__doc_title < other.__doc_title

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __getitem__(self, index: int) -> str:
        return self.__doc_title[index]

    def __contains__(self, text: str) -> bool:
        return text.lower() in self.__doc_title.lower()

    def __enter__(self) -> "JSONLWriter":
        return self


    def __int__(self) -> int:
        return len(self.__doc_title)

    def __float__(self) -> float:
        return float(len(self.__doc_title))
