"""Logger utility with improved OOP design."""

import logging
from pathlib import Path
from typing import Optional


class Logger:
    """Singleton logger with extensible configuration and helper methods."""

    _instance: Optional["Logger"] = None
    _DEFAULT_NAME = "PDFParser"

    def __new__(cls, log_file: Path = Path("outputs") / "parser.log") -> "Logger":
        """Singleton pattern ensuring only one logger instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(log_file)
        return cls._instance

    # ----------------------------------------------------------------------
    # Initialization (Abstraction + Encapsulation)
    # ----------------------------------------------------------------------
    def _initialize(self, log_file: Path) -> None:
        # Instance-level format settings (can be modified)
        self._format = "%(asctime)s [%(levelname)s] %(message)s"
        self._date_format = "%Y-%m-%d %H:%M:%S"

        self._logger = logging.getLogger(self._DEFAULT_NAME)
        self._logger.setLevel(logging.INFO)
        self._logger.handlers.clear()

        self._add_file_handler(log_file)
        self._add_console_handler()

    def _get_formatter(self) -> logging.Formatter:
        """Create a formatter (Polymorphic extension point)."""
        return logging.Formatter(self._format, datefmt=self._date_format)

    # ----------------------------------------------------------------------
    # Handlers (Encapsulation)
    # ----------------------------------------------------------------------
    def _add_file_handler(self, log_file: Path) -> None:
        """Add a file handler with internal error handling."""
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(log_file, mode="w")
            handler.setLevel(logging.INFO)
            handler.setFormatter(self._get_formatter())
            self._logger.addHandler(handler)
        except OSError as e:
            print(f"Warning: Could not create log file '{log_file}': {e}")

    def _add_console_handler(self) -> None:
        """Add console stream handler."""
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    # ----------------------------------------------------------------------
    # New OOP Features (Safe Additions)
    # ----------------------------------------------------------------------
    def add_handler(self, handler: logging.Handler) -> None:
        """Public method to add custom handlers (Polymorphism)."""
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    def set_level(self, level: int) -> None:
        """Update logging level at runtime."""
        self._logger.setLevel(level)

    def configure(
        self,
        *,
        level: int = logging.INFO,
        log_format: Optional[str] = None,
        date_format: Optional[str] = None,
    ) -> None:
        """
        Update logger configuration dynamically.
        (Abstraction + Polymorphism)
        """
        if log_format:
            self._format = log_format
        if date_format:
            self._date_format = date_format

        self.set_level(level)

        # Refresh format on all handlers
        for handler in self._logger.handlers:
            handler.setFormatter(self._get_formatter())

    # ----------------------------------------------------------------------
    # Logging methods (No change)
    # ----------------------------------------------------------------------
    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)


# Global instance used across the project
logger = Logger()
