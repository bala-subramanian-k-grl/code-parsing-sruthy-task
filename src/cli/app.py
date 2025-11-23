"""
CLI application entry point.

Enterprise-style OOP version with:
- Abstraction via BaseCLI and executor base classes
- Encapsulation via dedicated services
- Polymorphism through strategy pattern for parser modes
- Dependency Injection for configurability and testability
"""

import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Type, Union

from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.utils.logger import logger
from src.cli.strategies import ModeStrategyFactory


# =========================
# Abstractions
# =========================

class BaseCLI(ABC):
    @abstractmethod
    def parse_args(self) -> argparse.Namespace:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError


class BasePipelineExecutor(ABC):
    @abstractmethod
    def execute(self, file_path: Path, mode: ParserMode) -> ParserResult:
        raise NotImplementedError


# =========================
# Services
# =========================

class ArgumentParserService:
    def __init__(self) -> None:
        self._parser = self._build_parser()

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
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

        return parser

    def parse(self) -> argparse.Namespace:
        return self._parser.parse_args()


class FilePathResolver:
    def __init__(self, config_loader: ConfigLoader) -> None:
        self._config_loader = config_loader

    def resolve(self, file_arg: Optional[str]) -> Path:
        file_path_raw: Union[str, Path, None] = (
            file_arg or self._config_loader.get_pdf_path()
        )
        if not file_path_raw:
            raise ValueError("No PDF file path provided")

        file_path = Path(file_path_raw)
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        return file_path


class DefaultPipelineExecutor(BasePipelineExecutor):
    def __init__(self, orchestrator_cls: Type[PipelineOrchestrator]) -> None:
        self._orchestrator_cls = orchestrator_cls

    def execute(self, file_path: Path, mode: ParserMode) -> ParserResult:
        orchestrator = self._orchestrator_cls(file_path, mode)
        return orchestrator.execute()


class ResultLogger:
    @staticmethod
    def log(result: ParserResult) -> None:
        toc_count = len(result.toc_entries)
        content_count = len(result.content_items)
        logger.info("Extraction completed successfully")
        logger.info(f"Extracted {toc_count} TOC entries")
        logger.info(f"Extracted {content_count} content items")


# =========================
# CLI Application
# =========================

class CLIApp(BaseCLI):
    """Main CLI Application class."""

    def __init__(
        self,
        config_loader: Optional[ConfigLoader] = None,
        orchestrator_cls: Optional[Type[PipelineOrchestrator]] = None,
        arg_parser_service: Optional[ArgumentParserService] = None,
        mode_factory: Optional[ModeStrategyFactory] = None,
        pipeline_executor: Optional[BasePipelineExecutor] = None,
        result_logger: Optional[ResultLogger] = None,
    ) -> None:

        self._config_loader = config_loader or ConfigLoader()
        self._orchestrator_cls = orchestrator_cls or PipelineOrchestrator

        self._arg_parser_service = arg_parser_service or ArgumentParserService()
        self._mode_factory = mode_factory or ModeStrategyFactory()
        self._file_resolver = FilePathResolver(self._config_loader)
        self._pipeline_executor = (
            pipeline_executor or DefaultPipelineExecutor(self._orchestrator_cls)
        )
        self._result_logger = result_logger or ResultLogger()

    # ---- Parse args ----

    def parse_args(self) -> argparse.Namespace:
        return self._arg_parser_service.parse()

    # ---- Run CLI ----

    def run(self) -> None:
        try:
            args = self.parse_args()
            mode_strategy = self._mode_factory.create(args.mode)
            mode = mode_strategy.get_mode()

            file_path = self._file_resolver.resolve(args.file)

            logger.info(
                f"Processing {file_path} in {mode_strategy.name} "
                f"({mode}) mode"
            )

            result = self._pipeline_executor.execute(file_path, mode)
            self._result_logger.log(result)

        except FileNotFoundError as exc:
            logger.error(f"PDF file not found: {exc}")
        except ValueError as exc:
            logger.error(f"Configuration error: {exc}")
        except Exception as exc:
            logger.error(f"Unexpected error occurred: {exc}")

    # ---- Representations ----

    def __str__(self) -> str:
        return "CLIApp(parser=USB-PD)"

    def __repr__(self) -> str:
        return (
            f"CLIApp(config_loader={self._config_loader!r}, "
            f"orchestrator_cls={self._orchestrator_cls!r})"
        )


# Run directly
if __name__ == "__main__":
    CLIApp().run()
