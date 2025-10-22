"""TOC extractors implementation."""

from pathlib import Path
from typing import Any, Optional

from src.core.extractors.tocextractor.base_extractor import BaseTOCExtractor
from src.core.models import TOCEntry


class TOCExtractor(BaseTOCExtractor):  # Inheritance
    """PDF TOC extractor (Inheritance, Polymorphism)."""

    def extract_toc(self, source: Path) -> list[TOCEntry]:  # Polymorphism
        """Extract table of contents from PDF source."""
        content = self._get_content(source)
        return self._extract_entries(content)

    def _get_content(self, pdf_path: Path) -> Any:  # Encapsulation
        """Get PDF document for TOC extraction."""
        try:
            import fitz
            return fitz.open(str(pdf_path))
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("PDF read error: %s", e)
            return None

    def _extract_entries(self, doc: Any) -> list[TOCEntry]:
        """Extract TOC entries from PDF document."""
        if not doc:
            return []

        entries: list[TOCEntry] = []
        toc = doc.get_toc()

        for level, title, page in toc:
            section_id = self._extract_section_id(title)
            clean_title = self._clean_title(title, section_id)
            parent_id = self._get_parent_id(section_id)
            full_path = self._build_full_path(section_id, clean_title)

            entry = TOCEntry(
                doc_title="USB PD Specification",
                section_id=section_id,
                title=clean_title,
                full_path=full_path,
                page=page,
                level=level,
                parent_id=parent_id,
                tags=[]
            )
            entries.append(entry)

        doc.close()
        return entries

    def _extract_section_id(self, title: str) -> str:
        """Extract section ID from title."""
        import re

        # Try numeric section pattern first
        match = re.match(r'^(\d+(?:\.\d+)*)', title.strip())
        if match:
            return match.group(1)
        # Try alphanumeric pattern
        match = re.match(r'^([A-Za-z\d]+(?:\.[A-Za-z\d]+)*)', title.strip())
        if match:
            return match.group(1)
        # Generate simple ID from title
        clean = re.sub(r'[^A-Za-z\d]', '', title.strip())
        return clean[:10] if clean else 'section'

    def _clean_title(self, title: str, section_id: str) -> str:
        """Clean title by removing section ID."""
        if section_id in title:
            return title.replace(section_id, '').strip().lstrip('.')
        return title.strip()

    def _get_parent_id(self, section_id: str) -> Optional[str]:
        """Get parent section ID."""
        parts = section_id.split('.')
        return '.'.join(parts[:-1]) if len(parts) > 1 else None

    def _build_full_path(self, section_id: str, title: str) -> str:
        """Build full path for section."""
        return f"{section_id} {title}" if '.' in section_id else title
