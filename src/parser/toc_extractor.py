"""TOC extractor with hierarchical section numbering."""

from __future__ import annotations
from pathlib import Path
from typing import Any, Union

import fitz  # type: ignore[import-untyped]

from src.core.config.models import TOCEntry
from src.extractors.extractor_interface import ExtractorInterface


class TOCExtractor(ExtractorInterface):
    """Extract TOC with hierarchical section IDs."""

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

    # ---------------------------------------------------------
    # Encapsulation
    # ---------------------------------------------------------
    @property
    def file_path(self) -> Path:
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        return self.__file_path.exists()

    @property
    def file_name(self) -> str:
        return self.__file_path.name

    @property
    def file_size(self) -> int:
        return self.__file_path.stat().st_size if self.file_exists else 0

    @property
    def file_suffix(self) -> str:
        return self.__file_path.suffix.lower()

    # ---------------------------------------------------------
    # Polymorphism
    # ---------------------------------------------------------
    @property
    def extractor_type(self) -> str:
        """Type of extractor."""
        return "TOC"

    def supports(self, extension: str) -> bool:
        """TOC extractor only supports PDF."""
        return extension.lower() == ".pdf"

    def validate(self) -> bool:
        """Basic validation for extractor usage."""
        return self.file_exists and self.file_suffix == ".pdf"

    # ---------------------------------------------------------
    # Main Extraction Logic
    # ---------------------------------------------------------
    def extract(self, data: object = None) -> list[TOCEntry]:
        """Extract TOC with parent-child relationships."""
        if not self.validate():
            raise ValueError(f"Invalid file for TOC extraction: {self.file_path}")

        entries: list[TOCEntry] = []
        parent_stack: list[tuple[int, str]] = []

        try:
            with fitz.open(str(self.__file_path)) as doc:  # type: ignore
                toc: list[Any] = doc.get_toc()  # type: ignore
                for idx, entry in enumerate(toc):
                    level: int = int(entry[0])
                    title: str = str(entry[1])
                    page: int = int(entry[2])

                    sid = self._extract_section_id(title, idx)
                    lvl = level
                    pid = self._get_parent_id(lvl, parent_stack)
                    fpath = self._build_full_path(title)

                    entries.append(
                        TOCEntry(
                            section_id=sid,
                            title=title,
                            page=page,
                            level=lvl,
                            parent_id=pid,
                            full_path=fpath,
                        )
                    )

                    # Maintain hierarchical stack
                    while parent_stack and parent_stack[-1][0] >= lvl:
                        parent_stack.pop()
                    parent_stack.append((lvl, sid))

        except Exception as e:
            raise ValueError(f"Failed to extract TOC from PDF: {e}") from e

        return entries

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------
    def _extract_section_id(self, title: str, idx: int) -> str:
        parts = title.split()
        if not parts:
            return f"section_{idx}"

        first = parts[0].rstrip(".")
        if self._is_section_number(first):
            return first

        return f"section_{idx}"

    def _is_section_number(self, text: str) -> bool:
        parts = text.split(".")
        return all(p.isdigit() for p in parts if p)

    def _get_parent_id(self, level: int, stack: list[tuple[int, str]]) -> Union[str, None]:
        for parent_level, parent_id in reversed(stack):
            if parent_level < level:
                return parent_id
        return None

    def _build_full_path(self, title: str) -> str:
        return title

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"TOCExtractor(file={self.file_path.name})"

    def __repr__(self) -> str:
        return f"TOCExtractor(file_path={self.file_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.file_path == other.file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.file_path))

    def __len__(self) -> int:
        return len(str(self.file_path))

    def __bool__(self) -> bool:
        return self.file_exists

    def __contains__(self, text: str) -> bool:
        return text in str(self.file_path)
