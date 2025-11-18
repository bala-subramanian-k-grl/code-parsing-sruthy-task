"""TOC extractor with hierarchical section numbering."""

from pathlib import Path
from typing import Union

import fitz  # type: ignore[import-untyped]

from src.core.config.models import TOCEntry


class TOCExtractor:
    """Extract TOC with hierarchical section IDs."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def extract(self) -> list[TOCEntry]:
        """Extract TOC with parent-child relationships."""
        entries: list[TOCEntry] = []
        parent_stack: list[tuple[int, str]] = []

        try:
            with fitz.open(str(self._file_path)) as doc:  # type: ignore
                toc = doc.get_toc()  # type: ignore
                for idx, (level, title, page) in enumerate(toc):
                    title_str = str(title)  # type: ignore
                    sid = self._extract_section_id(title_str, idx)
                    lvl = int(level)  # type: ignore
                    pid = self._get_parent_id(lvl, parent_stack)
                    fpath = self._build_full_path(title_str)

                    entries.append(
                        TOCEntry(
                            section_id=sid,
                            title=title_str,
                            page=int(page),  # type: ignore
                            level=lvl,
                            parent_id=pid,
                            full_path=fpath,
                        )
                    )

                    while parent_stack and parent_stack[-1][0] >= lvl:
                        parent_stack.pop()
                    parent_stack.append((lvl, sid))
        except Exception as e:
            raise ValueError(f"Failed to extract TOC from PDF: {e}") from e

        return entries

    def _extract_section_id(self, title: str, idx: int) -> str:
        """Extract section ID from title."""
        parts = title.split()
        if not parts:
            return f"section_{idx}"

        first = parts[0].rstrip(".")
        if self._is_section_number(first):
            return first

        return f"section_{idx}"

    def _is_section_number(self, text: str) -> bool:
        """Check if text is a section number."""
        parts = text.split(".")
        return all(p.isdigit() for p in parts if p)

    def _get_parent_id(
        self, level: int, stack: list[tuple[int, str]]
    ) -> Union[str, None]:
        """Get parent section ID."""
        for parent_level, parent_id in reversed(stack):
            if parent_level < level:
                return parent_id
        return None

    def _build_full_path(self, title: str) -> str:
        """Build full hierarchical path."""
        return title
