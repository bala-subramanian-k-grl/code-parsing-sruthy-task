# USB PD Specification Parser - PDF Extraction Module
"""PDF extraction with OOP principles."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

try:
    import fitz  # type: ignore
except ImportError as e:
    raise ImportError("PyMuPDF required. Install: pip install PyMuPDF==1.24.9") from e


class PDFNotFoundError(Exception):  # Encapsulation
    pass


class BaseExtractor:  # Abstraction
    """Base extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path):
        self._pdf_path = self._validate_path(pdf_path)  # Encapsulation
        self._logger = logging.getLogger(__name__)  # Encapsulation

    def _validate_path(self, path: Path) -> Path:  # Encapsulation
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
        doc: Optional[fitz.Document] = None  # type: ignore
        try:
            doc = fitz.open(str(self._pdf_path))  # type: ignore
            doc_len: int = len(doc)  # type: ignore
            total_pages = doc_len if max_pages is None else min(max_pages, doc_len)
            for i in range(total_pages):
                try:
                    yield str(doc[i].get_text("text") or "")  # type: ignore
                except (fitz.FileDataError, fitz.FileNotFoundError) as e:  # type: ignore
                    self._logger.warning(f"PDF error on page {i}: {e}")
                    yield ""
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:  # type: ignore
            self._logger.error(f"Cannot open PDF file: {e}")
            return
        finally:
            if doc:
                doc.close()  # type: ignore


class TitleExtractor(BaseExtractor):  # Inheritance
    """Title extractor (Inheritance, Polymorphism)."""

    def get_title(self) -> str:  # Polymorphism
        try:
            with fitz.open(str(self._pdf_path)) as doc:  # type: ignore
                metadata = doc.metadata  # type: ignore
                title = metadata.get("title") if metadata else None  # type: ignore
                return (
                    title
                    if isinstance(title, str)
                    else "USB Power Delivery Specification"
                )
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:  # type: ignore
            self._logger.warning(f"Cannot read PDF metadata: {e}")
            return "USB Power Delivery Specification"


# Factory functions (Abstraction)
def extract_front_pages(pdf_path: Path, max_pages: Optional[int] = 10) -> Iterator[str]:
    return FrontPageExtractor(pdf_path).extract_pages(max_pages)


def get_doc_title(pdf_path: Path) -> str:
    try:
        return TitleExtractor(pdf_path).get_title()
    except (PDFNotFoundError, OSError, ValueError) as e:
        logging.getLogger(__name__).error(f"Cannot extract title: {e}")
        return "USB Power Delivery Specification"
