#!/usr/bin/env python3
"""Enterprise-grade table and figure extraction pipeline."""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.config.config_loader import ConfigLoader
from src.extractors.image_extractor import (
    FigureMetadataExtractor,
    ImageExtractionError,
)
from src.orchestrator.table_extraction_pipeline import (
    PipelineError,
    TableExtractionPipeline,
)
from src.utils.logger import logger


class BaseExtractionRunner(ABC):
    """Abstract base for extraction runners."""

    def __init__(self, pdf_path: Path, output_dir: Path) -> None:
        self._pdf_path = self._validate_pdf(pdf_path)
        self._output_dir = self._ensure_output_dir(output_dir)
        self._result: dict[str, Any] = {}

    @abstractmethod
    def run(self) -> dict[str, Any]:
        """Execute extraction process."""

    @abstractmethod
    def _log_results(self) -> None:
        """Log extraction results."""

    @property
    def result(self) -> dict[str, Any]:
        return self._result

    def _validate_pdf(self, path: Path) -> Path:
        """Validate PDF file exists and is readable."""
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        if not path.is_file() or path.suffix.lower() != '.pdf':
            raise ValueError(f"Invalid PDF: {path}")
        return path

    def _ensure_output_dir(self, path: Path) -> Path:
        """Ensure output directory exists."""
        path.mkdir(parents=True, exist_ok=True)
        return path


class TableExtractionRunner(BaseExtractionRunner):
    """Table extraction runner."""

    def __init__(
        self, pdf_path: Path, output_dir: Path, doc_title: str
    ) -> None:
        super().__init__(pdf_path, output_dir)
        self._doc_title = doc_title.strip() or "document"

    def run(self) -> dict[str, Any]:
        try:
            pipeline = TableExtractionPipeline(
                self._doc_title, self._output_dir, self._pdf_path
            )
            self._result = pipeline.extract_and_save()
            self._log_results()
            return self._result
        except (PipelineError, FileNotFoundError) as e:
            logger.error(f"Table extraction failed: {e}")
            raise

    def _log_results(self) -> None:
        count = self._result['tables_extracted']
        path = self._result.get('output_path', 'N/A')
        logger.info(f"Tables: {count} → {path}")


class FigureExtractionRunner(BaseExtractionRunner):
    """Figure metadata extraction runner."""

    def run(self) -> dict[str, Any]:
        try:
            extractor = FigureMetadataExtractor(
                self._pdf_path, self._output_dir
            )
            summary = extractor.extract()
            jsonl = self._output_dir / 'extracted_figures.jsonl'
            json_summary = self._output_dir / 'figures_summary.json'
            self._result = {
                'success': True,
                'total_figures': summary['total_figures'],
                'pages_with_figures': summary['pages_with_figures'],
                'output_jsonl': str(jsonl),
                'output_summary': str(json_summary)
            }
            self._log_results()
            return self._result
        except (ImageExtractionError, FileNotFoundError) as e:
            logger.error(f"Figure extraction failed: {e}")
            raise

    def _log_results(self) -> None:
        count = self._result['total_figures']
        path = self._result['output_jsonl']
        logger.info(f"Figures: {count} → {path}")


class ExtractionOrchestrator:
    """Coordinate extraction pipeline."""

    def __init__(
        self, pdf_path: Path, output_dir: Path, doc_title: str
    ) -> None:
        self._pdf_path = pdf_path
        self._output_dir = output_dir
        self._doc_title = doc_title

    def execute(self) -> dict[str, Any]:
        """Execute complete extraction pipeline."""
        results: dict[str, Any] = {'success': False}

        try:
            results['table_extraction'] = TableExtractionRunner(
                self._pdf_path, self._output_dir, self._doc_title
            ).run()

            results['figure_extraction'] = FigureExtractionRunner(
                self._pdf_path, self._output_dir
            ).run()

            results['success'] = True
            logger.info("✓ Extraction pipeline completed")
        except Exception as e:
            logger.error(f"✗ Pipeline failed: {e}")
            results['error'] = str(e)

        return results


def main() -> int:
    """Entry point with configuration-driven execution."""
    try:
        config = ConfigLoader()
        orchestrator = ExtractionOrchestrator(
            Path(config['input']['pdf_path']),
            Path(config['output']['base_dir']),
            config['metadata']['doc_title']
        )
        return 0 if orchestrator.execute()['success'] else 1
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
