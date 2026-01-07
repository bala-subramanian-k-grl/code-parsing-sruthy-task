"""Enterprise TOC Extractor with Overloading, Encapsulation & Polymorphism."""

from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Any

import fitz

from src.core.config.models import TOCEntry
from src.extractors.extractor_interface import ExtractorInterface
from src.utils.logger import logger


class TOCExtractor(ExtractorInterface, ABC):
    """Extract hierarchical Table of Contents from a PDF file."""

    # ----------------------------------------------------------------------
    # INIT (ENCAPSULATION)
    # ----------------------------------------------------------------------
    def __init__(self, file_path: Path) -> None:
        """Method implementation."""
        self.__file_path = file_path
        self.__extraction_count = 0

    # ----------------------------------------------------------------------
    # Encapsulated Properties
    # ----------------------------------------------------------------------
    @property
    def file_path(self) -> Path:
        """Method implementation."""
        return self.__file_path

    @property
    def file_exists(self) -> bool:
        """Method implementation."""
        return self.__file_path.exists()

    @property
    def file_suffix(self) -> str:
        """Method implementation."""
        return self.__file_path.suffix.lower()

    @property
    def extractor_type(self) -> str:
        """Method implementation."""
        return "TOC"

    @property
    def extraction_count(self) -> int:
        """Method implementation."""
        return self.__extraction_count

    @property
    def has_extractions(self) -> bool:
        """Method implementation."""
        return self.__extraction_count > 0

    @property
    def file_name(self) -> str:
        """Method implementation."""
        return self.file_path.name

    @property
    def file_stem(self) -> str:
        """Method implementation."""
        return self.file_path.stem

    @property
    def file_parent(self) -> str:
        """Method implementation."""
        return str(self.file_path.parent)

    @property
    def file_size_mb(self) -> float:
        """Method implementation."""
        if self.file_exists:
            return self.file_path.stat().st_size / (1024 * 1024)
        return 0.0

    # ----------------------------------------------------------------------
    # Protected Validation Methods
    # ----------------------------------------------------------------------
    def _supports(self, extension: str) -> bool:
        """Method implementation."""
        return extension.lower() == ".pdf"

    def _validate(self) -> bool:
        """Method implementation."""
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

        msg = (f"TOC extraction started: {self.file_path.name} "
               f"({self.file_size_mb:.2f} MB)")
        logger.info(msg)
        raw_toc = self._read_toc()
        entries = self._build_entries(raw_toc)
        msg = f"TOC extraction completed: {len(entries)} entries extracted"
        logger.info(msg)

        return entries

    # ----------------------------------------------------------------------
    # INTERNAL METHODS (ENCAPSULATED)
    # ----------------------------------------------------------------------
    def _read_toc(self) -> list[Any]:
        """Read raw TOC from PDF."""
        try:
            with fitz.open(str(self.file_path)) as doc:
                toc_data = doc.get_toc()
                return list(toc_data) if toc_data else []
        except Exception as e:
            raise ValueError(f"Failed to read TOC: {e}") from e

    def _build_entries(self, toc: list[Any]) -> list[TOCEntry]:
        """Method implementation."""
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
        """Method implementation."""
        parts = title.split()
        first = parts[0].rstrip(".") if parts else ""
        if self._is_section_number(first):
            return first
        return f"section_{idx}"

    def _is_section_number(self, text: str) -> bool:
        """Method implementation."""
        return all(p.isdigit() for p in text.split(".") if p)

    def _get_parent_id(
        self, level: int, stack: list[tuple[int, str]]
    ) -> str | None:
        for parent_level, parent_id in reversed(stack):
            if parent_level < level:
                return parent_id
        return None

    def _build_full_path(self, title: str) -> str:
        """Method implementation."""
        return title

    # ----------------------------------------------------------------------
    # Magic Methods
    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        """Method implementation."""
        return f"TOCExtractor(file={self.file_path.name})"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"TOCExtractor(file_path={self.file_path!r})"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.file_path == other.file_path

    def __hash__(self) -> int:
        """Method implementation."""
        return hash((type(self).__name__, self.file_path))

    def __len__(self) -> int:
        """Method implementation."""
        return self.extraction_count

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.file_exists

    def __contains__(self, text: str) -> bool:
        """Method implementation."""
        return text.lower() in str(self.file_path).lower()

    def __int__(self) -> int:
        """Method implementation."""
        return self.extraction_count

    def __float__(self) -> float:
        """Method implementation."""
        return float(self.extraction_count)

    def __getitem__(self, index: int) -> str:
        """Method implementation."""
        return str(self.file_path)[index]

    def __lt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.file_path < other.file_path

    def __le__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Method implementation."""
        if not isinstance(other, TOCExtractor):
            return NotImplemented
        return self.file_path > other.file_path

    def __ge__(self, other: object) -> bool:
        """Method implementation."""
        return self == other or self > other

    def __enter__(self) -> TOCExtractor:
        """Context manager support."""
        return self

    def __call__(self) -> list[TOCEntry]:
        """Make extractor callable."""
        return self.extract()
