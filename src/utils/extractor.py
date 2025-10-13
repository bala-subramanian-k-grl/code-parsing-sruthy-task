# USB PD Specification Parser - PDF Extraction Module
"""PDF extraction with OOP principles."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

try:
    import fitz
except ImportError as e:
    raise ImportError("PyMuPDF required. Install: pip install PyMuPDF==1.24.9") from e


from ..config.constants import DEFAULT_DOC_TITLE


class PDFNotFoundError(Exception):  # Encapsulation
    """PDF file not found error."""


class BaseExtractor:  # Abstraction
    """Base extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path):
        self._pdf_path = self._validate_path(pdf_path)  # Encapsulation
        self._logger = logging.getLogger(__name__)  # Encapsulation

    def _validate_path(self, path: Path) -> Path:  # Encapsulation
        """Validate PDF path securely."""
        if not path.exists():
            raise PDFNotFoundError(f"PDF not found: {path}")
        safe_path = path.resolve()
        assets_dir = Path.cwd().resolve() / "assets"
        try:
            safe_path.relative_to(assets_dir)
        except ValueError:
            raise PDFNotFoundError(f"Path outside assets: {path}") from None
        return safe_path


class FrontPageExtractor(BaseExtractor):  # Inheritance
    """Front page extractor (Inheritance, Polymorphism)."""

    def extract_pages(
        self, max_pages: Optional[int] = 10
    ) -> Iterator[str]:  # Polymorphism
        """Extract pages from PDF."""
        doc: Optional[fitz.Document] = None
        try:
            doc = fitz.open(str(self._pdf_path))
            if doc is None:
                return
            doc_len: int = len(doc)
            total_pages = doc_len if max_pages is None else min(max_pages, doc_len)
            for i in range(total_pages):
                try:
                    yield str(doc[i].get_text("text") or "")
                except (fitz.FileDataError, fitz.FileNotFoundError) as e:
                    self._logger.warning("PDF error on page %s: %s", i, e)
                    yield ""
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:
            self._logger.error("Cannot open PDF file: %s", e)
            return
        finally:
            if doc:
                doc.close()


class TitleExtractor(BaseExtractor):  # Inheritance
    """Title extractor (Inheritance, Polymorphism)."""

    def get_title(self) -> str:  # Polymorphism
        """Get PDF title from metadata."""
        try:
            with fitz.open(str(self._pdf_path)) as doc:
                metadata = doc.metadata
                title = metadata.get("title") if metadata else None
                return title if isinstance(title, str) else DEFAULT_DOC_TITLE
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:
            self._logger.warning("Cannot read PDF metadata: %s", e)
            return DEFAULT_DOC_TITLE


# Factory functions (Abstraction)
def extract_front_pages(pdf_path: Path, max_pages: Optional[int] = 10) -> Iterator[str]:
    """Extract front pages from PDF."""
    return FrontPageExtractor(pdf_path).extract_pages(max_pages)


def get_doc_title(pdf_path: Path) -> str:
    """Get document title from PDF."""
    try:
        return TitleExtractor(pdf_path).get_title()
    except (PDFNotFoundError, OSError, ValueError) as e:
        logging.getLogger(__name__).error("Cannot extract title: %s", e)
        return DEFAULT_DOC_TITLE
