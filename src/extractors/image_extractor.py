"""
ImageExtractor - Extract images and figures metadata from PDF.
"""

from __future__ import annotations

import json
import re
from io import BytesIO
from pathlib import Path
from typing import Any

import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTFigure, LTImage
from PIL import Image

from src.utils.logger import logger


class ImageExtractionError(Exception):
    """Custom exception for image extraction errors."""
    pass


class FigureMetadataExtractor:
    """Extract figure metadata from PDF List of Figures section."""

    def __init__(self, pdf_path: Path, output_dir: Path) -> None:
        """Initialize figure metadata extractor."""
        self._pdf_path = self._validate_pdf_path(pdf_path)
        self._output_dir = self._validate_output_dir(output_dir)
        self._figures: list[dict[str, Any]] = []

    def extract(self) -> dict[str, int]:
        """Extract figure list metadata from PDF."""
        try:
            self._extract_figures_from_toc()
            self._save_figures_metadata()
            summary = self._create_summary()
            logger.info(
                f"Extracted {len(self._figures)} figures metadata"
            )
            return summary
        except Exception as e:
            logger.error(f"Figure metadata extraction failed: {e}")
            raise ImageExtractionError(
                f"Failed to extract figures: {e}"
            ) from e

    def _extract_figures_from_toc(self) -> None:
        """Extract figures from List of Figures section."""
        doc: Any = fitz.open(self._pdf_path)

        try:
            for page_num in range(18, 30):
                page: Any = doc[page_num]
                text: str = page.get_text()
                pattern = r'Figure\s+(\d+\.\d+)\s+(.+?)\.+(\d+)'
                matches = re.findall(pattern, text, re.MULTILINE)

                for match in matches:
                    self._figures.append({
                        'page': int(match[2]),
                        'figure_id': match[0],
                        'title': match[1].strip()
                    })
        finally:
            doc.close()

    def _save_figures_metadata(self) -> None:
        """Save figures metadata to JSONL file."""
        jsonl_file = self._output_dir / 'extracted_figures.jsonl'

        try:
            with open(jsonl_file, 'w', encoding='utf-8') as f:
                for fig in self._figures:
                    f.write(json.dumps(fig) + '\n')
        except OSError as e:
            raise ImageExtractionError(
                f"Failed to write figures: {e}"
            ) from e

    def _create_summary(self) -> dict[str, int]:
        """Create and save summary of extracted figures."""
        summary = {
            'total_figures': len(self._figures),
            'pages_with_figures': len(
                set(fig['page'] for fig in self._figures)
            )
        }

        summary_file = self._output_dir / 'figures_summary.json'
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
        except OSError as e:
            logger.warning(f"Failed to write summary: {e}")

        return summary

    def _validate_pdf_path(self, pdf_path: Path) -> Path:
        """Validate PDF path."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        if not pdf_path.is_file():
            raise ValueError(f"Not a file: {pdf_path}")
        return pdf_path

    def _validate_output_dir(self, output_dir: Path) -> Path:
        """Validate and create output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir


class ImageExtractor:
    """Extract images from PDF documents."""

    def __init__(
        self,
        pdf_path: str | Path,
        output_dir: str | Path = "outputs",
        max_pages: int | None = None
    ) -> None:
        """Initialize image extractor."""
        self._pdf_path = Path(pdf_path)
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._max_pages = max_pages
        self._image_count = 0

    @property
    def pdf_path(self) -> Path:
        """Get PDF path."""
        return self._pdf_path

    @property
    def output_dir(self) -> Path:
        """Get output directory."""
        return self._output_dir

    @property
    def image_count(self) -> int:
        """Get number of extracted images."""
        return self._image_count

    def extract_figures_metadata(self) -> dict[str, int]:
        """Extract figure list metadata from PDF."""
        extractor = FigureMetadataExtractor(
            self._pdf_path, self._output_dir
        )
        return extractor.extract()

    def extract(self) -> list[dict[str, Any]]:
        """Extract all images from PDF."""
        images: list[dict[str, Any]] = []

        try:
            for page_num, page_layout in enumerate(
                extract_pages(str(self._pdf_path)), 1
            ):
                if self._max_pages and page_num > self._max_pages:
                    break

                page_images = self._extract_from_page(
                    page_layout, page_num
                )
                images.extend(page_images)

            self._image_count = len(images)
            logger.info(
                f"Extracted {len(images)} images from "
                f"{self._pdf_path.name}"
            )
        except Exception as e:
            logger.error(f"Image extraction failed: {e}")
            raise ImageExtractionError(
                f"Failed to extract images: {e}"
            ) from e

        return images

    def _extract_from_page(
        self, page_layout: Any, page_num: int
    ) -> list[dict[str, Any]]:
        """Extract images from a single page."""
        images: list[dict[str, Any]] = []
        img_idx = 0

        for element in page_layout:
            if isinstance(element, LTFigure):
                for item in element:
                    if isinstance(item, LTImage):
                        try:
                            image_data = self._save_image(
                                item, page_num, img_idx
                            )
                            if image_data:
                                images.append(image_data)
                                img_idx += 1
                        except Exception as e:
                            logger.debug(
                                f"Failed to extract image {img_idx} "
                                f"from page {page_num}: {e}"
                            )
                            continue

        return images

    def _save_image(
        self, image: LTImage, page_num: int, img_idx: int
    ) -> dict[str, Any] | None:
        """Save image to file."""
        try:
            img_data = image.stream.get_data()
            img = Image.open(BytesIO(img_data))

            filename = f"page_{page_num}_image_{img_idx}.png"
            filepath = self._output_dir / filename
            img.save(filepath)

            return {
                "page": page_num,
                "index": img_idx,
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "filepath": str(filepath)
            }
        except Exception as e:
            logger.debug(f"Failed to save image: {e}")
            return None

    def get_metadata(self) -> dict[str, Any]:
        """Get extraction metadata."""
        return {
            "pdf_path": str(self._pdf_path),
            "output_dir": str(self._output_dir),
            "images_extracted": self._image_count,
            "max_pages": self._max_pages
        }

    def __str__(self) -> str:
        """String representation."""
        return f"ImageExtractor(pdf={self._pdf_path.name}, images={self._image_count})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"ImageExtractor(pdf_path={self._pdf_path!r}, output_dir={self._output_dir!r})"

    def __len__(self) -> int:
        """Return number of extracted images."""
        return self._image_count

    def __bool__(self) -> bool:
        """Return True if images were extracted."""
        return self._image_count > 0

    def __eq__(self, other: object) -> bool:
        """Check equality based on PDF path."""
        if not isinstance(other, ImageExtractor):
            return NotImplemented
        return self._pdf_path == other._pdf_path

    def __hash__(self) -> int:
        """Hash based on PDF path."""
        return hash(self._pdf_path)
