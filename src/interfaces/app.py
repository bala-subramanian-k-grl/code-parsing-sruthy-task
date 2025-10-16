# USB PD Specification Parser - CLI Application Module
"""Minimal CLI app with OOP principles."""

import argparse
import logging
import sys
from abc import ABC, abstractmethod

from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator


class BaseApp(ABC):  # Abstraction
    def __init__(self) -> None:
        """Initialize base application."""
        self._logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)

    @abstractmethod  # Abstraction
    def run(self) -> None:
        pass


class CLIApp(BaseApp):  # Inheritance
    def __init__(self) -> None:
        """Initialize CLI application."""
        super().__init__()
        self._parser = self._create_parser()  # Encapsulation

    def _create_parser(self) -> argparse.ArgumentParser:  # Encapsulation
        """Create argument parser."""
        parser = argparse.ArgumentParser(description="USB PD Parser")
        parser.add_argument("--config", default="application.yml")
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser

    def _execute_pipeline(self, args: argparse.Namespace) -> None:
        """Execute pipeline based on arguments."""
        print("\n=== USB PD Specification Parser ===")
        print("Processing entire PDF document...\n")

        orchestrator = PipelineOrchestrator(args.config)
        if args.toc_only:
            result = orchestrator.run_toc_only()
            count = len(result)
            self._logger.info("TOC extraction completed: %s entries", count)
        elif args.content_only:
            result = orchestrator.run_content_only()
            msg = "Content extraction completed: %s items processed"
            self._logger.info(msg, result)
        else:
            result = orchestrator.run_full_pipeline()
            toc_count = result["toc_entries"]
            content_count = result["spec_counts"]["content_items"]
            self._logger.info(
                "Processing completed: %s TOC entries, %s content items",
                toc_count,
                content_count,
            )

    def run(self) -> None:  # Polymorphism
        """Run CLI application."""
        try:
            args = self._parser.parse_args()
            self._execute_pipeline(args)
        except Exception as e:
            self._logger.error("Application execution failed: %s", e)
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    CLIApp().run()  # Factory pattern + Polymorphism
