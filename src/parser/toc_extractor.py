"""TOC extractor with hierarchical section numbering."""

from pathlib import Path
from typing import Union

import fitz  # type: ignore[import-untyped]

from src.core.config.models import TOCEntry


class TOCExtractor:
    """Extract TOC with hierarchical section IDs."""

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

    @property
    def file_path(self) -> Path:
        """Get file path."""
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self.__file_path.exists()

    @property
    def file_name(self) -> str:
        """Get file name."""
        return self.__file_path.name

    @property
    def file_size(self) -> int:
        """Get file size."""
        return self.__file_path.stat().st_size if self.__file_path.exists() else 0

    @property
    def file_suffix(self) -> str:
        """Get file suffix."""
        return self.__file_path.suffix

    @property
    def file_parent(self) -> Path:
        """Get file parent directory."""
        return self.__file_path.parent

    @property
    def file_stem(self) -> str:
        """Get file stem."""
        return self.__file_path.stem

    def extract(self) -> list[TOCEntry]:
        """Extract TOC with parent-child relationships."""
        entries: list[TOCEntry] = []
        parent_stack: list[tuple[int, str]] = []

        try:
            with fitz.open(str(self.__file_path)) as doc:  # type: ignore
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

    def __str__(self) -> str:
        """String representation."""
        return f"TOCExtractor(file={self.__file_path.name})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"TOCExtractor(file_path={self.__file_path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.__file_path == other.__file_path

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__file_path))

    def __len__(self) -> int:
        return len(str(self.__file_path))

    def __bool__(self) -> bool:
        return self.__file_path.exists()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return str(self.__file_path) < str(other.__file_path)

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, text: str) -> bool:
        """Check if text in file path."""
        return text in str(self.__file_path)
