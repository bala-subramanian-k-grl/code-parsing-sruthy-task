"""
CLI application entry point with rich OOP design.
"""

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
from pathlib import Path

from src.cli.decorators import protected_access
from src.cli.strategies import ModeStrategyFactory
from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import ParserResult
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.utils.logger import logger

# ======================================================================
# ABSTRACT BASE TYPES
# ======================================================================


class BaseCLI(ABC):
    """Abstract base class for all CLI front-ends."""

    @abstractmethod
    def parse_args(self) -> argparse.Namespace:
        """Parse CLI arguments into a namespace."""
        raise NotImplementedError

    @abstractmethod
    def run(self, *args: object, **kwargs: object) -> None:
        """Run the CLI application."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}(abstract CLI)"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"<{self.__class__.__name__} abstract>"


class BasePipelineExecutor(ABC):
    """Abstract executor responsible for running the parsing pipeline."""

    @abstractmethod
    def execute(self, file_path: Path, mode: ParserMode) -> ParserResult:
        """Execute pipeline and return ParserResult."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}(abstract executor)"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"<{self.__class__.__name__} abstract>"


class BaseValidator(ABC):
    """Abstract base for value/path/mode validators."""

    @abstractmethod
    def validate(self, value: str) -> bool:
        """Return True if the provided value is considered valid."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"


class BaseFormatter(ABC):
    """Abstract base for output formatters used for logging or display."""

    @abstractmethod
    def format(self, *args: object, **kwargs: object) -> str:
        """Return formatted string for given args."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"


class BaseService(ABC):
    """Abstract base for service classes."""

    @abstractmethod
    def execute(self, *args: object, **kwargs: object) -> object:
        """Execute service operation."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"


class BaseResolver(ABC):
    """Abstract base for resolver classes."""

    @abstractmethod
    def resolve(self, *args: object, **kwargs: object) -> object:
        """Resolve and return result."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"


class BaseLogger(ABC):
    """Abstract base for logger classes."""

    @abstractmethod
    def log(self, *args: object, **kwargs: object) -> None:
        """Log information."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}()"


# ======================================================================
# VALIDATORS & ARGUMENT SERVICES
# ======================================================================


class ArgumentValidator(BaseValidator, ABC):
    """Helper class for validating CLI input strings (paths, modes)."""

    def validate(self, value: str) -> bool:
        """Validate generic non-empty string."""
        return bool(value)

    def validate_file(self, path: str) -> bool:
        """Validate that a file path exists."""
        return Path(path).exists() if path else False

    def validate_mode(self, mode: str) -> bool:
        """Validate that mode is one of allowed parser modes."""
        return mode in {"full", "toc", "content"}


class ArgumentParserService(BaseService):
    """
    Service that encapsulates argument parsing logic.

    Responsibilities:
    - Build argparse.ArgumentParser
    - Parse command line
    - Perform basic input validations
    """

    def __init__(self) -> None:
        """Method implementation."""
        self._parser = self._build_parser()
        self._validator = ArgumentValidator()

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        """Method implementation."""
        desc = "USB-PD Specification Parser CLI"
        parser = argparse.ArgumentParser(description=desc)

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

    def execute(self, *args: object, **kwargs: object) -> argparse.Namespace:
        """Execute service - parse arguments."""
        return self.parse()

    def parse(self) -> argparse.Namespace:
        """Parse CLI arguments and apply basic validation."""
        args = self._parser.parse_args()

        if args.file and not self._validator.validate_file(args.file):
            # Soft validation: log warning, let downstream raise if needed
            logger.warning(f"File does not exist: {args.file}")

        if not self._validator.validate_mode(args.mode):
            raise ValueError(f"Invalid mode value: {args.mode}")

        return args

    def __str__(self) -> str:
        """Method implementation."""
        return "ArgumentParserService"

    def __repr__(self) -> str:
        """Method implementation."""
        return "ArgumentParserService()"


class PathValidator(BaseValidator, ABC):
    """Validates filesystem paths using pathlib.Path."""

    def validate(self, value: str) -> bool:
        """Method implementation."""
        return Path(value).exists()

    def exists(self, path: Path) -> bool:
        """Method implementation."""
        return path.exists()

    def is_file(self, path: Path) -> bool:
        """Method implementation."""
        return path.is_file()


class FilePathResolver(BaseResolver):
    """
    Resolves input file path using precedence:
        1. CLI argument
        2. Configuration (input.pdf_path)
    """

    def __init__(self, config_loader: ConfigLoader) -> None:
        """Method implementation."""
        self._config_loader = config_loader
        self._validator = PathValidator()

    def resolve(self, *args: object, **kwargs: object) -> object:
        """Resolve final file path to use for parsing."""
        file_arg = (
            args[0]
            if args and isinstance(args[0], (str, type(None)))
            else None
        )
        file_path_raw = file_arg or self._config_loader.get("input.pdf_path")
        if not file_path_raw:
            raise ValueError("No PDF file path provided")

        file_path = Path(file_path_raw)

        if not self._validator.exists(file_path):
            raise FileNotFoundError(file_path)

        if not self._validator.is_file(file_path):
            raise ValueError(f"Path is not a file: {file_path}")

        return file_path

    def __str__(self) -> str:
        """Method implementation."""
        return "FilePathResolver"

    def __repr__(self) -> str:
        """Method implementation."""
        return "FilePathResolver()"


# ======================================================================
# PIPELINE EXECUTION & RESULT LOGGING
# ======================================================================


class DefaultPipelineExecutor(BasePipelineExecutor, ABC):
    """
    Default implementation of pipeline executor.

    Delegates:
    - Construction of PipelineOrchestrator
    - Calling execute()
    """

    def __init__(self, orchestrator_cls: type[PipelineOrchestrator]) -> None:
        """Method implementation."""
        self._orchestrator_cls = orchestrator_cls

    def execute(self, file_path: Path, mode: ParserMode) -> ParserResult:
        """Method implementation."""
        orchestrator = self._orchestrator_cls(file_path, mode)
        return orchestrator.execute()

    def __repr__(self) -> str:
        """Method implementation."""
        cls_name = self._orchestrator_cls.__name__
        return (
            f"{self.__class__.__name__}"
            f"(orchestrator_cls={cls_name})"
        )


class ResultFormatter(BaseFormatter, ABC):
    """Formats counts and messages for result logging."""

    def format(self, *args: object, **kwargs: object) -> str:
        """
        Generic format implementation.

        Expected usage:
            format(label, count)
        """
        if len(args) >= 2:
            label, count = args[0], args[1]
            return f"Extracted {count} {label}"
        return ""

    def format_count(self, label: str, count: int) -> str:
        """Method implementation."""
        return f"Extracted {count} {label}"


class ResultLogger(BaseLogger):
    """Logs high-level statistics of ParserResult."""

    def __init__(self) -> None:
        """Method implementation."""
        self._formatter = ResultFormatter()

    def log(
        self,
        *args: object,
        **kwargs: object
    ) -> None:
        """Method implementation."""
        if not args or not isinstance(args[0], ParserResult):
            return
        result = args[0]
        logger.info("Extraction completed successfully")

        toc_msg = self._formatter.format_count(
            "TOC entries", len(result.toc_entries)
        )
        content_msg = self._formatter.format_count(
            "content items", len(result.content_items)
        )

        logger.info(toc_msg)
        logger.info(content_msg)

    def __str__(self) -> str:
        """Method implementation."""
        return "ResultLogger"

    def __repr__(self) -> str:
        """Method implementation."""
        return "ResultLogger()"


# ======================================================================
# MAIN CLI APPLICATION
# ======================================================================


class CLIApp(BaseCLI, ABC):
    """
    Main CLI application.

    Responsibilities:
    - Read configuration
    - Parse CLI arguments
    - Resolve file path
    - Choose ParserMode via strategy
    - Execute pipeline via executor
    - Log results via ResultLogger

    OOP Features:
    - Abstraction via BaseCLI
    - Overloaded run()
    - Encapsulated counters (run/success/error)
    - Composition of multiple services for SRP
    """

    def __init__(
        self,
        config_loader: ConfigLoader | None = None,
        orchestrator_cls: type[PipelineOrchestrator] | None = None,
        arg_parser_service: ArgumentParserService | None = None,
        mode_factory: ModeStrategyFactory | None = None,
        pipeline_executor: BasePipelineExecutor | None = None,
        result_logger: ResultLogger | None = None,
    ) -> None:
        # Core collaborators (composition)
        self._config_loader = config_loader or ConfigLoader()
        self._orchestrator_cls = orchestrator_cls or PipelineOrchestrator
        self._arg_parser_service = (
            arg_parser_service or ArgumentParserService()
        )
        self._mode_factory = mode_factory or ModeStrategyFactory()
        self._file_resolver = FilePathResolver(self._config_loader)
        self._pipeline_executor = (
            pipeline_executor
            or DefaultPipelineExecutor(self._orchestrator_cls)
        )
        self._result_logger = result_logger or ResultLogger()

        # Encapsulated execution counters
        self.__run_count = 0
        self.__success_count = 0
        self.__error_count = 0

    # --------------------------------------------------
    # Protected counter mutators (decorator-based control)
    # --------------------------------------------------

    @protected_access
    def _increment_run_count(self) -> None:
        """Method implementation."""
        self.__run_count += 1

    @protected_access
    def _increment_success_count(self) -> None:
        """Method implementation."""
        self.__success_count += 1

    @protected_access
    def _increment_error_count(self) -> None:
        """Method implementation."""
        self.__error_count += 1

    # --------------------------------------------------
    # Read-only statistics (encapsulation)
    # --------------------------------------------------

    @property
    def run_count(self) -> int:
        """Method implementation."""
        return self.__run_count

    @property
    def success_count(self) -> int:
        """Method implementation."""
        return self.__success_count

    @property
    def error_count(self) -> int:
        """Method implementation."""
        return self.__error_count

    # --------------------------------------------------
    # BaseCLI implementation
    # --------------------------------------------------

    def parse_args(self) -> argparse.Namespace:
        """Parse CLI arguments using service."""
        return self._arg_parser_service.parse()

    # --------------------------------------------------
    # run() method matching base signature
    # --------------------------------------------------

    def run(self, *args: object, **kwargs: object) -> None:
        """
        Run CLI application.

        Usage:
            - run()                        → internally parse args
            - run(parsed_args)             → use already parsed args
        """
        self._increment_run_count()

        try:
            # 1. Resolve arguments
            if args and isinstance(args[0], argparse.Namespace):
                parsed_args = args[0]
            else:
                parsed_args = None
            if parsed_args is None:
                parsed_args = self.parse_args()

            # 2. Resolve mode via strategy
            mode_strategy = self._mode_factory.create(parsed_args.mode)
            mode = mode_strategy.get_mode()

            # 3. Resolve file path
            resolved = self._file_resolver.resolve(parsed_args.file)
            if not isinstance(resolved, Path):
                raise TypeError("Resolver must return Path")
            file_path = resolved

            logger.info(
                f"Processing {file_path} in {mode_strategy.name} "
                f"({mode.value}) mode"
            )

            # 4. Execute pipeline
            result = self._pipeline_executor.execute(file_path, mode)

            # 5. Log summary
            self._result_logger.log(result)

            self._increment_success_count()

        except (FileNotFoundError, ValueError) as exc:
            logger.error(f"Error: {exc}")
            self._increment_error_count()

        except Exception as exc:  # noqa: BLE001 - last-resort catch for CLI
            logger.error(f"Unexpected error occurred: {exc}")
            self._increment_error_count()

    # --------------------------------------------------
    # Magic methods (meaningful only)
    # --------------------------------------------------

    def __str__(self) -> str:
        """Method implementation."""
        return (
            f"CLIApp(run={self.__run_count}, "
            f"success={self.__success_count}, "
            f"errors={self.__error_count})"
        )

    def __repr__(self) -> str:
        """Method implementation."""
        return (
            f"CLIApp(config_loader={self._config_loader!r}, "
            f"orchestrator_cls={self._orchestrator_cls!r}"
        )

    def __len__(self) -> int:
        """Return how many times the app has been executed."""
        return self.__run_count

    def __bool__(self) -> bool:
        """CLIApp is always considered truthy (instantiated app)."""
        return True


# Script-style execution (still useful for direct `python -m src.cli.app`)
if __name__ == "__main__":
    CLIApp().run()
