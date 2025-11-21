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
