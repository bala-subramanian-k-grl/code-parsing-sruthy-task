# USB PD Specification Parser - Logger Module
"""Logger with OOP principles."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseLoggerFactory(ABC):  # Abstraction
    """Abstract logger factory (Abstraction, Encapsulation)."""

    def __init__(self, name: str = "usb_pd_parser"):
        self._name = name  # Encapsulation
        self._formatter = self._create_formatter()  # Encapsulation

    @abstractmethod  # Abstraction
    def create_logger(
        self, output_dir: Optional[Path] = None, debug: bool = False
    ) -> logging.Logger:
        pass

    def _create_formatter(self) -> logging.Formatter:  # Encapsulation
        return logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )


class LoggerFactory(BaseLoggerFactory):  # Inheritance
    """Logger factory (Inheritance, Polymorphism)."""

    def create_logger(
        self, output_dir: Optional[Path] = None, debug: bool = False
    ) -> logging.Logger:  # Polymorphism
        logger = logging.getLogger(self._name)
        log_level = logging.DEBUG if debug else logging.INFO
        logger.setLevel(log_level)

        if not logger.handlers:
            self._add_console_handler(logger, log_level)
            if output_dir:
                self._add_file_handler(logger, output_dir, log_level)
        return logger

    def _add_console_handler(
        self, logger: logging.Logger, log_level: int
    ) -> None:  # Encapsulation
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(self._formatter)
        logger.addHandler(ch)

    def _add_file_handler(
        self, logger: logging.Logger, output_dir: Path, log_level: int
    ) -> None:  # Encapsulation
        try:
            safe_dir = self._validate_output_dir(output_dir)
            # Additional security check before mkdir
            if not safe_dir.name.replace("_", "").replace("-", "").isalnum():
                raise ValueError(f"Invalid directory name: {safe_dir.name}")
            safe_dir.mkdir(parents=True, exist_ok=True)
            log_file = safe_dir / "parser.log"
            # Validate log file path to prevent traversal
            if not log_file.resolve().is_relative_to(safe_dir.resolve()):
                raise ValueError("Log file path traversal detected")
            fh = logging.FileHandler(log_file)
            fh.setLevel(log_level)
            fh.setFormatter(self._formatter)
            logger.addHandler(fh)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not create file handler: {e}")

    def _validate_output_dir(self, output_dir: Path) -> Path:  # Encapsulation
        """Validate output directory against security vulnerabilities."""
        try:
            # Sanitize input to prevent command injection
            clean_path = Path(
                str(output_dir).replace("..", "").replace(";", "").replace("|", "")
            )
            resolved_path = clean_path.resolve(strict=False)
            working_dir = Path.cwd().resolve()

            # Prevent path traversal attacks
            if not resolved_path.is_relative_to(working_dir):
                raise ValueError(f"Path traversal detected: {output_dir}")

            # Additional security check for suspicious patterns
            path_str = str(resolved_path)
            if any(char in path_str for char in ["&", "`", "$", "(", ")", "<", ">"]):
                raise ValueError(f"Suspicious characters in path: {output_dir}")

            return resolved_path
        except (OSError, ValueError) as e:
            raise ValueError(f"Invalid output directory: {output_dir} - {e}") from e


def get_logger(
    name: str = "usb_pd_parser", output_dir: Optional[Path] = None, debug: bool = False
) -> logging.Logger:  # Factory function
    factory = LoggerFactory(name)  # Polymorphism
    return factory.create_logger(output_dir, debug)
