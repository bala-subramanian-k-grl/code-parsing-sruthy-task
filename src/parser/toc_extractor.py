"""Enterprise TOC Extractor with Overloading, Encapsulation & Polymorphism."""

from __future__ import annotations

from pathlib import Path
from typing import Any

# type: ignore[import-untyped]
# pyright: ignore[reportMissingTypeStubs]
import fitz  # type: ignore[import-untyped]

from src.core.config.models import TOCEntry
from src.extractors.extractor_interface import ExtractorInterface


class TOCExtractor(ExtractorInterface):
    """Extract hierarchical Table of Contents from a PDF file."""

    # ----------------------------------------------------------------------
    # INIT (ENCAPSULATION)
    # ----------------------------------------------------------------------
    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path
        self.__extraction_count = 0

    # ----------------------------------------------------------------------
    # Encapsulated Properties
    # ----------------------------------------------------------------------
    @property
    def file_path(self) -> Path:
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        return self.__file_path.exists()

    @property
    def file_suffix(self) -> str:
        return self.__file_path.suffix.lower()

    @property
    def extractor_type(self) -> str:
        return "TOC"

    @property
    def extraction_count(self) -> int:
        return self.__extraction_count

    @property
    def has_extractions(self) -> bool:
        return self.__extraction_count > 0

    @property
    def file_name(self) -> str:
        return self.file_path.name

    @property
    def file_stem(self) -> str:
        return self.file_path.stem

    @property
    def file_parent(self) -> str:
        return str(self.file_path.parent)

    @property
    def file_size_kb(self) -> float:
        if self.file_exists:
            return self.file_path.stat().st_size / 1024
        return 0.0

    @property
    def file_size_mb(self) -> float:
        if self.file_exists:
            return self.file_path.stat().st_size / (1024 * 1024)
        return 0.0

    @property
    def is_pdf(self) -> bool:
        return self.file_suffix == ".pdf"

    @property
    def file_absolute_path(self) -> str:
        return str(self.file_path.absolute())

    # ----------------------------------------------------------------------
    # Protected Validation Methods
    # ----------------------------------------------------------------------
    def _supports(self, extension: str) -> bool:
        return extension.lower() == ".pdf"

    def _validate(self) -> bool:
        return self.file_exists and self.file_suffix == ".pdf"

    # ----------------------------------------------------------------------
    # extract() - matches ExtractorInterface signature
    # ----------------------------------------------------------------------
    def extract(self, data: Any = None) -> list[TOCEntry]:
        """Extract TOC entries from PDF file."""
        self.__extraction_count += 1

        if not self._validate():
            msg = f"Invalid file for TOC extraction: {self.file_path}"
            raise ValueError(msg)

        raw_toc = self._read_toc()
        entries = self._build_entries(raw_toc)

        return entries

    # ----------------------------------------------------------------------
    # INTERNAL METHODS (ENCAPSULATED)
    # ----------------------------------------------------------------------
    def _read_toc(self) -> list[Any]:
        """Read raw TOC from PDF."""
        try:
            # type: ignore[attr-defined]
            with fitz.open(str(self.file_path)) as doc:
                toc_data = doc.get_toc()  # type: ignore[attr-defined]
                return list(toc_data) if toc_data else []
        except Exception as e:
            raise ValueError(f"Failed to read TOC: {e}") from e

    def _build_entries(self, toc: list[Any]) -> list[TOCEntry]:
        parent_stack: list[tuple[int, str]] = []
        entries: list[TOCEntry] = []

        for idx, entry in enumerate(toc):
            lvl = int(entry[0])
            title = str(entry[1])
            page = int(entry[2])

            sid = self._extract_section_id(title, idx)
            pid = self._get_parent_id(lvl, parent_stack)
            fpath = self._build_full_path(title)

            toc_entry = TOCEntry(
                section_id=sid,
                title=title,
                page=page,
                level=lvl,
                parent_id=pid,
                full_path=fpath,
            )
            entries.append(toc_entry)

            # Maintain stack
            while parent_stack and parent_stack[-1][0] >= lvl:
                parent_stack.pop()
            parent_stack.append((lvl, sid))

        return entries

    # ----------------------------------------------------------------------
    # Protected helper functions
    # ----------------------------------------------------------------------
    def _extract_section_id(self, title: str, idx: int) -> str:
        parts = title.split()
        first = parts[0].rstrip(".") if parts else ""
        if self._is_section_number(first):
            return first
        return f"section_{idx}"

    def _is_section_number(self, text: str) -> bool:
        return all(p.isdigit() for p in text.split(".") if p)

    def _get_parent_id(
        self, level: int, stack: list[tuple[int, str]]
    ) -> str | None:
        for parent_level, parent_id in reversed(stack):
            if parent_level < level:
                return parent_id
        return None

    def _build_full_path(self, title: str) -> str:
        return title

    # ----------------------------------------------------------------------
    # Magic Methods
    # ----------------------------------------------------------------------
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
        return self.extraction_count

    def __bool__(self) -> bool:
        return self.file_exists

    def __contains__(self, text: str) -> bool:
        return text.lower() in str(self.file_path).lower()

    def __int__(self) -> int:
        return self.extraction_count

    def __float__(self) -> float:
        return float(self.extraction_count)

    def __getitem__(self, index: int) -> str:
        return str(self.file_path)[index]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.file_path < other.file_path

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.file_path > other.file_path

    def __ge__(self, other: object) -> bool:
        return self == other or self > other

    def __enter__(self) -> "TOCExtractor":
        """Context manager support."""
        return self

    def __call__(self) -> list[TOCEntry]:
        """Make extractor callable."""
        return self.extract()
