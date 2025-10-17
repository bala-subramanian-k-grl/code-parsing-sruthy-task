# USB PD Specification Parser - TOC Extractor Module
"""Module for extracting Table of Contents from USB PD documents."""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from src.core.models import TOCEntry


class BaseTOCExtractor(ABC):  # Abstraction
    """Abstract TOC extractor (Abstraction, Encapsulation)."""

    def __init__(self, doc_title: str = "USB PD Specification"):
        self._doc_title = doc_title  # Encapsulation
        # Encapsulation: protected patterns
        self._patterns = [
            r"^([A-Z][^.]*?)\s*\.{3,}\s*(\d+)$",
            r"^(\d+(?:\.\d+)*)\s+([^.]+?)\s*\.{2,}\s*(\d+)$",
            r"^([A-Z][A-Za-z\s&(),-]+)\s+(\d+)$",
        ]

    @abstractmethod  # Abstraction
    def extract_toc(self, source: Path) -> list[TOCEntry]:
        pass

    def _parse_line(self, line: str, counter: int) -> Optional[TOCEntry]:
        """Parse line for TOC entry (Encapsulation)."""
        for pattern in self._patterns:
            match = re.match(pattern, line)
            if match:
                entry = self._process_match(match, counter)
                if entry:
                    return entry
        return None

    def _process_match(
        self, match: re.Match[str], counter: int
    ) -> Optional[TOCEntry]:
        """Process regex match (Encapsulation)."""
        groups = match.groups()
        section_id, title, page_str = self._extract_groups(groups, counter)

        if not section_id:
            return None

        return self._create_toc_entry(section_id, title, page_str)

    def _extract_groups(
        self, groups: tuple[str, ...], counter: int
    ) -> tuple[str, str, str]:
        """Extract section_id, title, page_str from groups (Encapsulation)."""
        if len(groups) == 2:
            title, page_str = groups
            return f"S{counter}", title, page_str
        elif len(groups) == 3:
            section_id, title, page_str = groups
            return section_id, title, page_str
        return "", "", ""

    def _create_toc_entry(
        self, section_id: str, title: str, page_str: str
    ) -> Optional[TOCEntry]:
        """Create TOC entry if valid (Encapsulation)."""
        try:
            page = int(page_str)
            if not self._is_valid_entry(page, title):
                return None

            level = self._calculate_level(section_id)
            return TOCEntry(
                doc_title=self._doc_title,
                section_id=section_id,
                title=title.strip(),
                full_path=title.strip(),
                page=page,
                level=level,
                parent_id=None,
                tags=[],
            )
        except ValueError:
            return None

    def _is_valid_entry(self, page: int, title: str) -> bool:
        """Check if entry is valid (Encapsulation)."""
        return 1 <= page <= 2000 and len(title.strip()) >= 3

    def _calculate_level(self, section_id: str) -> int:
        """Calculate hierarchy level (Encapsulation)."""
        return section_id.count(".") + 1 if "." in section_id else 1
