# USB PD Specification Parser - TOC Extractor Module
"""TOC extractor with OOP principles."""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

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
                groups = match.groups()
                if len(groups) == 2:
                    title, page_str = groups
                    section_id = f"S{counter}"
                elif len(groups) == 3:
                    section_id, title, page_str = groups
                else:
                    continue

                try:
                    page = int(page_str)
                    valid_page = 1 <= page <= 2000
                    valid_title = len(title.strip()) >= 3
                    if valid_page and valid_title:
                        # Calculate hierarchy level based on section structure
                        has_subsections = "." in section_id
                        level = section_id.count(".") + 1 if has_subsections else 1
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
                    pass
        return None


class TOCExtractor(BaseTOCExtractor):  # Inheritance
    """PDF TOC extractor (Inheritance, Polymorphism)."""

    def extract_toc(self, source: Path) -> list[TOCEntry]:  # Polymorphism
        content = self._get_content(source)
        return self._extract_entries(content)

    def _get_content(self, pdf_path: Path) -> str:  # Encapsulation
        try:
            import fitz  # type: ignore

            doc: Any = fitz.open(str(pdf_path))  # type: ignore
            doc_length: int = len(doc)  # type: ignore
            content = "".join(
                str(doc[page_num].get_text())  # type: ignore
                for page_num in range(min(20, doc_length))
            )
            doc.close()  # type: ignore
            return content
        except Exception as e:
            import logging

            logging.getLogger(__name__).warning(f"PDF read error: {e}")
            return ""

    def _extract_entries(self, content: str) -> list[TOCEntry]:
        """Extract TOC entries from content (Encapsulation)."""
        entries: list[TOCEntry] = []
        counter, in_toc = 1, False

        for line in content.split("\n"):
            line = line.strip()
            if len(line) < 5:
                continue
            if "contents" in line.lower():
                in_toc = True
                continue
            if not in_toc and not any(p in line for p in ["...", "  "]):
                continue
            entry = self._parse_line(line, counter)
            if entry:
                entries.append(entry)  # type: ignore
                counter += 1
        return entries
