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
from typing import Optional, Union

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
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

    def parse_args(self):
        """Parse command-line arguments."""
        parser = argparse.ArgumentParser(
            description="USB-PD Specification Parser CLI"
        )

        parser.add_argument(
            "--file",
            "-f",
            type=str,
            help="Path to the PDF file. Overrides config file value.",
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

    def resolve_mode(self, mode_str: str) -> ParserMode:
        """Convert CLI string mode to ParserMode enum."""
        mode_map = {
            "full": ParserMode.FULL,
            "toc": ParserMode.TOC_ONLY,
            "content": ParserMode.CONTENT_ONLY,
        }
        return mode_map.get(mode_str.lower(), ParserMode.FULL)

    def run(self) -> None:
        """Run the CLI application."""
        file_path: Union[Path, None] = None
        try:
            args = self.parse_args()

            file_path_raw = args.file or self._config_loader.get_pdf_path()
            file_path = (
                Path(file_path_raw) if isinstance(file_path_raw, str)
                else file_path_raw
            )

            if file_path is None:
                raise ValueError("No PDF file path provided")

            mode = self.resolve_mode(args.mode)

            logger.info(f"Processing {file_path} in {mode} mode")

            orchestrator = self._orchestrator_cls(file_path, mode)
            result = orchestrator.execute()

            logger.info(f"Extracted {len(result.toc_entries)} TOC entries")
            logger.info(f"Extracted {len(result.content_items)} content items")

        except FileNotFoundError:
            logger.error(f"PDF file not found: {file_path}")

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    CLIApp().run()
