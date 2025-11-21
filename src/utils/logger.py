"""Logger utility."""

import logging
from pathlib import Path
from typing import Optional


class Logger:
    """Logger wrapper with common logging methods."""

    _instance: Optional["Logger"] = None
    _FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __new__(cls, log_file: Path = Path("outputs") / "parser.log") -> "Logger":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(log_file)
        return cls._instance

    def _initialize(self, log_file: Path) -> None:
        """Initialize logger with handlers."""
        self._logger = logging.getLogger("PDFParser")
        self._logger.setLevel(logging.INFO)
        self._logger.handlers.clear()

        self._add_file_handler(log_file)
        self._add_console_handler()

    def _add_file_handler(self, log_file: Path) -> None:
        """Add file handler."""
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(log_file, mode="w")
            handler.setLevel(logging.INFO)
            handler.setFormatter(self._get_formatter())
            self._logger.addHandler(handler)
        except OSError as e:
            print(f"Warning: Could not create file handler: {e}")

    def _add_console_handler(self) -> None:
        """Add console handler."""
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    def _get_formatter(self) -> logging.Formatter:
        """Get formatter instance."""
        return logging.Formatter(self._FORMAT, datefmt=self._DATE_FORMAT)

    def debug(self, message: str) -> None:
        """Log debug message."""
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """Log info message."""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message."""
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical message."""
        self._logger.critical(message)


# Global instance for convenience
logger = Logger()
