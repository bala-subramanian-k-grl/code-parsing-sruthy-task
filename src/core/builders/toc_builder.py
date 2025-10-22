"""Builder pattern for TOC structure validation."""

import re
from abc import ABC, abstractmethod
from typing import Any, Optional


class TOCBuilder(ABC):
    """Abstract TOC builder."""

    @abstractmethod
    def build_structure(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Build TOC structure from entries."""
        pass


class HierarchicalTOCBuilder(TOCBuilder):
    """Builder for hierarchical TOC structure."""

    def build_structure(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Build hierarchical TOC with proper numbering."""
        enhanced_entries = self._enhance_entries(entries)
        return self._add_hierarchy(enhanced_entries)

    def _enhance_entries(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Enhance all entries with structure info."""
        return [self._process_single_entry(entry) for entry in entries]

    def _process_single_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        """Protected method to process a single entry."""
        return self._enhance_entry(entry)

    def _enhance_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        """Enhance TOC entry with structure info."""
        title = self._get_entry_title(entry)
        level = self._detect_level(title)
        section_num = self._extract_section_number(title)

        return self._create_enhanced_entry(entry, level, section_num)

    def _get_entry_title(self, entry: dict[str, Any]) -> str:
        """Protected method to get entry title safely."""
        return entry.get("title", "")

    def _create_enhanced_entry(
        self, entry: dict[str, Any], level: int, section_num: Optional[str]
    ) -> dict[str, Any]:
        """Protected method to create enhanced entry dictionary."""
        return {
            **entry,
            "level": level,
            "section_number": section_num,
            "has_numbering": bool(section_num),
        }

    def _detect_level(self, title: str) -> int:
        """Detect hierarchical level from title."""
        # Count leading dots or numbers
        if re.match(r"^\d+\.\d+\.\d+", title):
            return 3
        elif re.match(r"^\d+\.\d+", title):
            return 2
        elif re.match(r"^\d+\.", title):
            return 1
        return 1

    def _extract_section_number(self, title: str) -> Optional[str]:
        """Extract section number from title."""
        match = re.match(r"^(\d+(?:\.\d+)*)", title)
        return match.group(1) if match else None

    def _add_hierarchy(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Add parent-child relationships."""
        for i, entry in enumerate(entries):
            if self._should_process_hierarchy(i):
                self._set_parent_relationship(entries, i, entry)
        return entries

    def _should_process_hierarchy(self, index: int) -> bool:
        """Protected method to check if hierarchy should be processed."""
        return index > 0

    def _set_parent_relationship(
        self, entries: list[dict[str, Any]], index: int, entry: dict[str, Any]
    ) -> None:
        """Protected method to set parent relationship."""
        parent_id = self._find_parent_id(entries, index, entry["level"])
        if parent_id:
            entry["parent_id"] = parent_id

    def _find_parent_id(
        self,
        entries: list[dict[str, Any]],
        current_idx: int,
        current_level: int,
    ) -> Optional[str]:
        """Find parent ID for current entry."""
        parent_level = current_level - 1
        for j in range(current_idx - 1, -1, -1):
            if entries[j]["level"] == parent_level:
                return entries[j].get("section_id")
        return None
