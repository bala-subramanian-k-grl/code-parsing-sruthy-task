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
        parser.add_argument("--mode", type=int, choices=[1, 2, 3])
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser

    def _get_mode(self) -> int:  # Encapsulation
        """Get processing mode from user input."""
        self._display_mode_options()
        return self._get_user_choice()
    
    def _display_mode_options(self) -> None:
        """Display available processing modes."""
        print("\n=== USB PD Specification Parser ===")
        print("Please select processing mode:")
        print("  [1] Full Document    - Process entire PDF (all pages)")
        print("  [2] Extended Mode    - Process first 600 pages")
        print("  [3] Standard Mode    - Process first 200 pages")
        print("")
    
    def _get_user_choice(self) -> int:
        """Get and validate user choice."""
        mode_names = {1: "Full Document", 2: "Extended Mode", 3: "Standard Mode"}
        
        while True:
            try:
                choice = int(input("Enter your choice (1-3): ").strip())
                if self._is_valid_choice(choice):
                    print(f"\nSelected: {mode_names[choice]}")
                    return choice
                print("Invalid selection. Please choose 1, 2, or 3.")
            except (ValueError, KeyboardInterrupt):
                self._handle_input_error()
    
    def _is_valid_choice(self, choice: int) -> bool:
        """Check if choice is valid."""
        return 1 <= choice <= 3
    
    def _handle_input_error(self) -> None:
        """Handle input errors."""
        self._logger.warning("User provided invalid input")
        print("Invalid input. Please enter a valid number (1-3).")

    def _execute_pipeline(self, args: argparse.Namespace) -> None:
        """Execute pipeline based on arguments."""
        orchestrator = PipelineOrchestrator(args.config)
        if args.toc_only:
            result = orchestrator.run_toc_only()
            self._logger.info(
                f"TOC extraction completed: {len(result)} entries extracted"
            )
        elif args.content_only:
            result = orchestrator.run_content_only()
            self._logger.info(
                f"Content extraction completed: {result} items processed"
            )
        else:
            mode = args.mode or self._get_mode()
            result = orchestrator.run_full_pipeline(mode)
            toc_count = result["toc_entries"]
            content_count = result["spec_counts"]["content_items"]
            msg = f"Processing completed: {toc_count} TOC entries, "
            msg += f"{content_count} content items processed"
            self._logger.info(msg)

    def run(self) -> None:  # Polymorphism
        """Run CLI application."""
        try:
            args = self._parser.parse_args()
            self._execute_pipeline(args)
        except Exception as e:
            self._logger.error(f"Application execution failed: {e}")
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    CLIApp().run()  # Factory pattern + Polymorphism
