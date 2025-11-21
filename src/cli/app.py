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
        self.__config_loader = config_loader or ConfigLoader()
        self.__orchestrator_cls = orchestrator_cls or PipelineOrchestrator

    @property
    def config_loader(self) -> ConfigLoader:
        """Get config loader."""
        return self.__config_loader

    @property
    def orchestrator_cls(self) -> type:
        """Get orchestrator class."""
        return self.__orchestrator_cls

    @property
    def has_config(self) -> bool:
        """Check if has config loader."""
        return self.__config_loader is not None

    @property
    def has_orchestrator(self) -> bool:
        """Check if has orchestrator class."""
        return self.__orchestrator_cls is not None

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
        file_path: Union[Path, None] = None
        try:
            args = self.parse_args()

            file_path_raw = args.file or self.__config_loader.get_pdf_path()
            file_path = (
                Path(file_path_raw) if isinstance(file_path_raw, str)
                else file_path_raw
            )

            if file_path is None:
                raise ValueError("No PDF file path provided")

            mode = self._resolve_mode(args.mode)

            logger.info(f"Processing {file_path} in {mode} mode")

            orchestrator = self.__orchestrator_cls(file_path, mode)
            result = orchestrator.execute()

            logger.info(f"Extracted {len(result.toc_entries)} TOC entries")
            logger.info(f"Extracted {len(result.content_items)} content items")

        except FileNotFoundError:
            logger.error(f"PDF file not found: {file_path}")

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

    def __str__(self) -> str:
        """String representation."""
        return "CLIApp(parser=USB-PD)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"CLIApp(config_loader={self.__config_loader!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CLIApp):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash((type(self).__name__, id(self.__config_loader)))

    def __len__(self) -> int:
        return 2

    def __bool__(self) -> bool:
        return self.__config_loader is not None


if __name__ == "__main__":
    CLIApp().run()
