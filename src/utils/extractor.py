"""PDF extractions with OOP principles."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

try:
    import fitz
except ImportError as e:
    MSG = "PyMuPDF required. Install: pip install PyMuPDF==1.24.9"
    raise ImportError(MSG) from e


from ..config.constants import DEFAULT_DOC_TITLE


class PDFNotFoundError(Exception):  # Encapsulation
    """PDF file not found error."""


class BaseExtractor:  # Abstraction
    """Base extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path):
        self._pdf_path = self._validate_path(pdf_path)  # Protected
        self._logger = logging.getLogger(__name__)  # Protected
        self.__extraction_count: int = 0  # Private counter
        self.__error_count: int = 0  # Private error tracking

    @property
    def pdf_path(self) -> Path:
        """Get PDF path (read-only)."""
        return self._pdf_path

    @property
    def extraction_count(self) -> int:
        """Get extraction count."""
        return self.__extraction_count

    @property
    def error_count(self) -> int:
        """Get error count."""
        return self.__error_count

    def _increment_extraction_count(self) -> None:  # Protected method
        """Increment extraction counter."""
        self.__extraction_count += 1

    def _increment_error_count(self) -> None:  # Protected method
        """Increment error counter."""
        self.__error_count += 1

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
            if max_pages is None:
                total_pages = doc_len
            else:
                total_pages = min(max_pages, doc_len)
            for i in range(total_pages):
                try:
                    self._increment_extraction_count()
                    yield str(doc[i].get_text("text") or "")
                except (fitz.FileDataError, fitz.FileNotFoundError) as e:
                    self._increment_error_count()
                    msg = f"PDF error on page {i}: {e}"
                    self._logger.warning(msg)
                    yield ""
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:
            self._increment_error_count()
            msg = f"Cannot open PDF file: {e}"
            self._logger.error(msg)
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
                self._increment_extraction_count()
                metadata = doc.metadata
                title = metadata.get("title") if metadata else None
                if isinstance(title, str):
                    return title
                return DEFAULT_DOC_TITLE
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:
            self._increment_error_count()
            msg = f"Cannot read PDF metadata: {e}"
            self._logger.warning(msg)
            return DEFAULT_DOC_TITLE


# Factory functions (Abstraction)
def extract_front_pages(
    pdf_path: Path, max_pages: Optional[int] = 10
) -> Iterator[str]:
    """Extract front pages from PDF."""
    return FrontPageExtractor(pdf_path).extract_pages(max_pages)


def get_doc_title(pdf_path: Path) -> str:
    """Get document title from PDF."""
    try:
        return TitleExtractor(pdf_path).get_title()
    except (PDFNotFoundError, OSError, ValueError) as e:
        msg = f"Cannot extract title: {e}"
        logging.getLogger(__name__).error(msg)
        return DEFAULT_DOC_TITLE
