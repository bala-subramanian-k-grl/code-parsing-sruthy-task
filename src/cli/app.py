"""
CLI application entry point.
Improved version with:
- Dependency Injection
- argparse support
- error handling
- flexible parser mode
- testability
"""

import argparse
from pathlib import Path
from typing import Optional

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.utils.logger import logger


class CLIApp:
    """Command-line interface application."""

    def __init__(
        self,
        config_loader: Optional[ConfigLoader] = None,
        orchestrator_cls: Optional[type] = None,
    ) -> None:
        """
        Initialize CLI application with dependency injection.

        Args:
            config_loader: Inject custom ConfigLoader for testing.
            orchestrator_cls: Inject custom orchestrator class.
        """
        self._config_loader = config_loader or ConfigLoader()
        self._orchestrator_cls = orchestrator_cls or PipelineOrchestrator

    @property
    def config_loader(self) -> ConfigLoader:
        """Get config loader."""
        return self._config_loader

    @property
    def orchestrator_cls(self) -> type:
        """Get orchestrator class."""
        return self._orchestrator_cls

    def parse_args(self) -> argparse.Namespace:
        """Parse command-line arguments."""
        parser = argparse.ArgumentParser(
            description="USB-PD Specification Parser CLI"
        )

        parser.add_argument(
            "--file",
            "-f",
            type=str,
            help="Path to PDF file. Overrides config value.",
        )

        parser.add_argument(
            "--mode",
            "-m",
            type=str,
            choices=["full", "toc", "content"],
            default="full",
            help="Parser mode to use.",
        )

        return parser.parse_args()

    def _resolve_mode(self, mode_str: str) -> ParserMode:
        """Convert CLI string mode to ParserMode enum."""
        mode_map = {
            "full": ParserMode.FULL,
            "toc": ParserMode.TOC,
            "content": ParserMode.CONTENT,
        }
        return mode_map.get(mode_str.lower(), ParserMode.FULL)

    def run(self) -> None:
        """Run the CLI application."""
        try:
            args = self.parse_args()
            file_path = self._get_file_path(args)
            mode = self._resolve_mode(args.mode)

            logger.info(f"Processing {file_path} in {mode} mode")

            result = self._execute_pipeline(file_path, mode)
            self._log_results(result)

        except FileNotFoundError as e:
            logger.error(f"PDF file not found: {e}")
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

    def _get_file_path(self, args: argparse.Namespace) -> Path:
        """Get and validate file path from args or config."""
        file_path_raw = (
            args.file or self._config_loader.get_pdf_path()
        )
        file_path = (
            Path(file_path_raw)
            if isinstance(file_path_raw, str)
            else file_path_raw
        )
        if file_path is None:
            raise ValueError("No PDF file path provided")
        return file_path

    def _execute_pipeline(
        self,
        file_path: Path,
        mode: ParserMode
    ) -> ParserResult:
        """Execute orchestrator pipeline."""
        orchestrator = self._orchestrator_cls(file_path, mode)
        return orchestrator.execute()

    def _log_results(self, result: ParserResult) -> None:
        """Log extraction results."""
        toc_count = len(result.toc_entries)
        content_count = len(result.content_items)
        logger.info(f"Extracted {toc_count} TOC entries")
        logger.info(f"Extracted {content_count} content items")

    def __str__(self) -> str:
        """String representation."""
        return "CLIApp(parser=USB-PD)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"CLIApp(config_loader={self._config_loader!r})"


if __name__ == "__main__":
    CLIApp().run()
