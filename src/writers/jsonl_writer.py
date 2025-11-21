"""JSONL writer implementation."""

import json
from pathlib import Path
from typing import Any, Callable, TypeVar, Union

from src.core.config.models import ContentItem, TOCEntry
from src.writers.writer_interface import WriterInterface

T = TypeVar('T', TOCEntry, ContentItem)


class JSONLWriter(WriterInterface):
    """Writes TOC and Content to JSONL files."""

    def __init__(self, doc_title: str) -> None:
        self.__doc_title = doc_title

    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self.__doc_title

    @property
    def title_length(self) -> int:
        """Get title length."""
        return len(self.__doc_title)

    @property
    def has_title(self) -> bool:
        """Check if has title."""
        return bool(self.__doc_title)

    @property
    def title_words(self) -> int:
        """Get title word count."""
        return len(self.__doc_title.split())

    @property
    def title_chars(self) -> int:
        """Get title character count."""
        return len(self.__doc_title)

    @property
    def title_upper(self) -> str:
        """Get title in uppercase."""
        return self.__doc_title.upper()

    def write_toc(self, entries: list[TOCEntry], path: Path) -> None:
        """Write TOC entries to JSONL file."""
        self._write_jsonl(entries, path, self._serialize_toc)

    def write_content(self, items: list[ContentItem], path: Path) -> None:
        """Write content items to JSONL file."""
        self._write_jsonl(items, path, self._serialize_content)

    def write(
        self, data: list[Union[TOCEntry, ContentItem]], path: Path
    ) -> None:
        """Generic write method (required by interface)."""
        if data and isinstance(data[0], TOCEntry):
            self.write_toc(data, path)
        elif data and isinstance(data[0], ContentItem):
            self.write_content(data, path)

    def _write_jsonl(
        self,
        data: list[T],
        path: Path,
        serializer: Callable[[T], dict[str, Any]]
    ) -> None:
        """Write data to JSONL file using serializer."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for item in data:
                json_data = json.dumps(serializer(item))
                f.write(f"{json_data}\n")

    def _serialize_toc(self, entry: TOCEntry) -> dict[str, Any]:
        """Serialize TOC entry to dict."""
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
        """Serialize content item to dict."""
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

    def __str__(self) -> str:
        return f"JSONLWriter(doc_title={self.__doc_title})"

    def __repr__(self) -> str:
        return f"JSONLWriter(doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, JSONLWriter):
            return NotImplemented
        return self.__doc_title == other.__doc_title

    def __hash__(self) -> int:
        """Hash for sets/dicts."""
        return hash((type(self).__name__, self.__doc_title))

    def __len__(self) -> int:
        """Get title length."""
        return len(self.__doc_title)

    def __bool__(self) -> bool:
        """Check if has doc title."""
        return bool(self.__doc_title)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, JSONLWriter):
            return NotImplemented
        return self.__doc_title < other.__doc_title

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __getitem__(self, index: int) -> str:
        """Get character from doc title."""
        return self.__doc_title[index]

    def __contains__(self, text: str) -> bool:
        """Check if text in doc title."""
        return text.lower() in self.__doc_title.lower()

    def __enter__(self) -> "JSONLWriter":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        pass

    def __int__(self) -> int:
        """Get title length as int."""
        return len(self.__doc_title)

    def __float__(self) -> float:
        """Get title length as float."""
        return float(len(self.__doc_title))
