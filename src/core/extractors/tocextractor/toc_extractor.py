"""TOC extractor implementation."""

from pathlib import Path
from typing import Any

from src.core.extractors.tocextractor.base_extractor import BaseTOCExtractor
from src.core.models import TOCEntry


class TOCExtractor(BaseTOCExtractor):  # Inheritance
    """PDF TOC extractor (Inheritance, Polymorphism)."""

    def extract_toc(self, source: Path) -> list[TOCEntry]:  # Polymorphism
        content = self._get_content(source)
        return self._extract_entries(content)

    def _get_content(self, pdf_path: Path) -> str:  # Encapsulation
        try:
            import fitz

            doc: Any = fitz.open(str(pdf_path))
            doc_length: int = len(doc)
            content = "".join(
                str(doc[page_num].get_text()) for page_num in range(min(20, doc_length))
            )
            doc.close()
            return content
        except Exception as e:
            import logging

            logging.getLogger(__name__).warning("PDF read error: %s", e)
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
                entries.append(entry)
                counter += 1
        return entries
