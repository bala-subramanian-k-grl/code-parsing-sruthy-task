"""
CLI application entry point with improved OOP, encapsulation, and polymorphism.
"""

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from typing import overload

from src.cli.decorators import protected_access
from src.cli.strategies import ModeStrategyFactory
from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.utils.logger import logger

# =========================
# Abstractions
# =========================

class BaseCLI(ABC):
    """Abstract base class for CLI interfaces."""

    @abstractmethod
    def parse_args(self) -> argparse.Namespace:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    # Polymorphism added
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(abstract CLI)"

    def __repr__(self) -> str:
        return f"<BaseCLI abstract class {self.__class__.__name__}>"


class BasePipelineExecutor(ABC):
    """Abstract executor responsible for running the pipeline."""

    @abstractmethod
    def execute(self, file_path: Path, mode: ParserMode) -> ParserResult:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(abstract executor)"

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"<BasePipelineExecutor abstract class {cls_name}>"


# =========================
# Services
# =========================

class ArgumentValidator:
    """Helper class for validating CLI inputs."""

    def validate_file(self, path: str) -> bool:
        return Path(path).exists() if path else False

    def validate_mode(self, mode: str) -> bool:
        return mode in ["full", "toc", "content"]


class ArgumentParserService:
    """Handles CLI argument parsing."""

    def __init__(self) -> None:
        self._parser = self._build_parser()
        self._validator = ArgumentValidator()

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        desc = "USB-PD Specification Parser CLI"
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument(
            "--file", "-f", type=str,
            help="Path to PDF file. Overrides config value."
        )
        parser.add_argument(
            "--mode", "-m", type=str,
            choices=["full", "toc", "content"],
            default="full",
            help="Parser mode to use."
        )
        return parser

    def parse(self) -> argparse.Namespace:
        args = self._parser.parse_args()
        if args.file and not self._validator.validate_file(args.file):
            pass
        return args


class PathValidator:
    """Validates filesystem paths."""

    def exists(self, path: Path) -> bool:
        return path.exists()

    def is_file(self, path: Path) -> bool:
        return path.is_file()


class FilePathResolver:
    """Resolves file paths using CLI args or configuration."""

    def __init__(self, config_loader: ConfigLoader) -> None:
        self._config_loader = config_loader
        self._validator = PathValidator()

    def resolve(self, file_arg: str | None) -> Path:
        file_path_raw = file_arg or self._config_loader.get("pdf_path")
        if not file_path_raw:
            raise ValueError("No PDF file path provided")

        file_path = Path(file_path_raw)

        if not self._validator.exists(file_path):
            raise FileNotFoundError(file_path)

        return file_path


class DefaultPipelineExecutor(BasePipelineExecutor):
    """Executes the pipeline using the orchestrator."""

    def __init__(self, orchestrator_cls: type[PipelineOrchestrator]) -> None:
        self._orchestrator_cls = orchestrator_cls

    def execute(self, file_path: Path, mode: ParserMode) -> ParserResult:
        orchestrator = self._orchestrator_cls(file_path, mode)
        return orchestrator.execute()


class ResultFormatter:
    """Formats output results for logging."""

    def format_count(self, label: str, count: int) -> str:
        return f"Extracted {count} {label}"


class ResultLogger:
    """Logs final parsed counts."""

    def __init__(self) -> None:
        self._formatter = ResultFormatter()

    def log(self, result: ParserResult) -> None:
        logger.info("Extraction completed successfully")
        toc_msg = self._formatter.format_count(
            "TOC entries", len(result.toc_entries)
        )
        content_msg = self._formatter.format_count(
            "content items", len(result.content_items)
        )
        logger.info(toc_msg)
        logger.info(content_msg)


# =========================
# CLI Application
# =========================

class CLIApp(BaseCLI):
    """Main CLI application with full OOP enhancements."""

    def __init__(
        self,
        config_loader: ConfigLoader | None = None,
        orchestrator_cls: type[PipelineOrchestrator] | None = None,
        arg_parser_service: ArgumentParserService | None = None,
        mode_factory: ModeStrategyFactory | None = None,
        pipeline_executor: BasePipelineExecutor | None = None,
        result_logger: ResultLogger | None = None,
    ) -> None:

        self._config_loader = config_loader or ConfigLoader()
        self._orchestrator_cls = (
            orchestrator_cls or PipelineOrchestrator
        )
        self._arg_parser_service = (
            arg_parser_service or ArgumentParserService()
        )
        self._mode_factory = mode_factory or ModeStrategyFactory()
        self._file_resolver = FilePathResolver(self._config_loader)
        self._pipeline_executor = (
            pipeline_executor or
            DefaultPipelineExecutor(self._orchestrator_cls)
        )
        self._result_logger = result_logger or ResultLogger()

        # Encapsulated Counters
        self.__run_count = 0
        self.__success_count = 0
        self.__error_count = 0

    # ---------------------------
    # Protected Internal Methods
    # ---------------------------

    @protected_access
    def _increment_run_count(self) -> None:
        self.__run_count += 1

    @protected_access
    def _increment_success_count(self) -> None:
        self.__success_count += 1

    @protected_access
    def _increment_error_count(self) -> None:
        self.__error_count += 1

    # ---------------------------
    # Properties (Encapsulation)
    # ---------------------------

    @property
    def run_count(self) -> int:
        return self.__run_count

    @run_count.setter
    def run_count(self, value: int):
        if value < 0:
            raise ValueError("run_count cannot be negative")
        self.__run_count = value

    @property
    def success_count(self) -> int:
        return self.__success_count

    @success_count.setter
    def success_count(self, value: int):
        if value < 0:
            raise ValueError("success_count cannot be negative")
        self.__success_count = value

    @property
    def error_count(self) -> int:
        return self.__error_count

    @error_count.setter
    def error_count(self, value: int):
        if value < 0:
            raise ValueError("error_count cannot be negative")
        self.__error_count = value

    # ---------------------------
    # Abstract Method Implementation
    # ---------------------------

    def parse_args(self) -> argparse.Namespace:
        """Override: Parse command line arguments."""
        return self._arg_parser_service.parse()

    # ---------------------------
    # Run (With Overloading)
    # ---------------------------

    @overload
    def run(self) -> None: ...

    @overload
    def run(self, args: argparse.Namespace) -> None: ...

    def run(self, args: argparse.Namespace | None = None) -> None:
        """Run the CLI application, optionally using pre-parsed arguments."""
        self._increment_run_count()

        try:
            if args is None:
                args = self.parse_args()

            mode_strategy = self._mode_factory.create(args.mode)
            mode = mode_strategy.get_mode()
            file_path = self._file_resolver.resolve(args.file)

            msg = (
                f"Processing {file_path} in "
                f"{mode_strategy.name} ({mode}) mode"
            )
            logger.info(msg)

            result = self._pipeline_executor.execute(file_path, mode)
            self._result_logger.log(result)

            self._increment_success_count()

        except (FileNotFoundError, ValueError) as exc:
            logger.error(f"Error: {exc}")
            self._increment_error_count()

        except Exception as exc:
            logger.error(f"Unexpected error occurred: {exc}")
            self._increment_error_count()

    # ---------------------------
    # Polymorphic Magic Methods
    # ---------------------------

    def __str__(self) -> str:
        return "CLIApp(parser=USB-PD)"

    def __repr__(self) -> str:
        return (
            f"CLIApp(config_loader={self._config_loader!r}, "
            f"orchestrator_cls={self._orchestrator_cls!r})"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CLIApp)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __len__(self) -> int:
        return self.__run_count

    def __bool__(self) -> bool:
        return True

    def __int__(self) -> int:
        return self.__run_count

    def __float__(self) -> float:
        return float(self.__success_count)


# Run directly
if __name__ == "__main__":
    CLIApp().run()
