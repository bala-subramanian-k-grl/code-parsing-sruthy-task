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


class HierarchicalTOCBuilder(TOCBuilder):
    """Builder for hierarchical TOC structure."""

    def build_structure(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Build hierarchical TOC with proper numbering."""
        enhanced_entries = self.__enhance_entries(entries)
        return self.__add_hierarchy(enhanced_entries)

    def __enhance_entries(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:  # Private - only used internally
        """Enhance all entries with structure info."""
        return [self.__process_single_entry(entry) for entry in entries]

    def __process_single_entry(
        self, entry: dict[str, Any]
    ) -> dict[str, Any]:  # Private - only used internally
        """Process a single entry."""
        return self.__enhance_entry(entry)

    def __enhance_entry(
        self, entry: dict[str, Any]
    ) -> dict[str, Any]:  # Private - only used internally
        """Enhance TOC entry with structure info."""
        title = self.__get_entry_title(entry)
        level = self.__detect_level(title)
        section_num = self.__extract_section_number(title)

        return self.__create_enhanced_entry(entry, level, section_num)

    def __get_entry_title(
        self, entry: dict[str, Any]
    ) -> str:  # Private - only used internally
        """Get entry title safely."""
        title = entry.get("title", "")
        return str(title) if title else ""

    def __create_enhanced_entry(
        self, entry: dict[str, Any], level: int, section_num: str
    ) -> dict[str, Any]:  # Private - only used internally
        """Create enhanced entry dictionary."""
        return {
            **entry,
            "level": level,
            "section_number": section_num,
            "has_numbering": bool(section_num),
        }

    def __detect_level(
        self, title: str
    ) -> int:  # Private - only used internally
        """Detect hierarchical level from title."""
        # Count leading dots or numbers
        if re.match(r"^\d+\.\d+\.\d+", title):
            return 3
        if re.match(r"^\d+\.\d+", title):
            return 2
        if re.match(r"^\d+\.", title):
            return 1
        return 1

    def __extract_section_number(
        self, title: str
    ) -> str:  # Private - only used internally
        """Extract section number from title."""
        _ = title  # Parameter required by interface
        return ""

    def __add_hierarchy(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:  # Private - only used internally
        """Add parent-child relationships."""
        for i, entry in enumerate(entries):
            if self.__should_process_hierarchy(i):
                self.__set_parent_relationship(entries, i, entry)
        return entries

    def __should_process_hierarchy(
        self, index: int
    ) -> bool:  # Private - only used internally
        """Check if hierarchy should be processed."""
        return index > 0

    def __set_parent_relationship(
        self, entries: list[dict[str, Any]], index: int, entry: dict[str, Any]
    ) -> None:  # Private - only used internally
        """Set parent relationship."""
        parent_id = self.__find_parent_id(entries, index, entry["level"])
        if parent_id:
            entry["parent_id"] = parent_id

    def __find_parent_id(
        self,
        entries: list[dict[str, Any]],
        current_idx: int,
        current_level: int,
    ) -> Optional[str]:  # Private - only used internally
        """Find parent ID for current entry."""
        parent_level = current_level - 1
        for j in range(current_idx - 1, -1, -1):
            if entries[j]["level"] == parent_level:
                return entries[j].get("section_id")
        return None
