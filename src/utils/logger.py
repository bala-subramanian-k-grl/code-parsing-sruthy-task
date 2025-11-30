"""
Enterprise-grade Singleton Logger
"""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import overload


class BaseLogger(ABC):
    """Abstract base class for all loggers."""

    @abstractmethod
    def info(self, msg: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, msg: str) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Logger(BaseLogger):
    """Thread-safe Singleton Logger with full OOP design."""

    _instance: "Logger | None" = None
    _lock = threading.Lock()
    _DEFAULT_NAME = "PDFParser"

    # ---------------------------------------------------------
    # Singleton Constructor
    # ---------------------------------------------------------
    def __new__(
        cls,
        log_file: Path = Path("outputs") / "parser.log"
    ) -> "Logger":
        """Create only one Logger instance (thread-safe)."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(log_file)
            return cls._instance

    # ---------------------------------------------------------
    # Initialization (Encapsulation)
    # ---------------------------------------------------------
    def _initialize(self, log_file: Path) -> None:
        """Internal initialization (called only once)."""
        self._format = "%(asctime)s [%(levelname)s] %(message)s"
        self._date_format = "%Y-%m-%d %H:%M:%S"
        self._log_file = log_file

        self._logger = logging.getLogger(self._DEFAULT_NAME)
        self._logger.setLevel(logging.INFO)
        self._logger.handlers.clear()

        # Add default handlers
        self._add_file_handler(log_file)
        self._add_console_handler()

    # ---------------------------------------------------------
    # Encapsulation: Formatters & Handlers
    # ---------------------------------------------------------
    def _get_formatter(self) -> logging.Formatter:
        """Create a formatter (polymorphic extension point)."""
        return logging.Formatter(self._format, datefmt=self._date_format)

    def _add_file_handler(self, log_file: Path) -> None:
        """Add file handler with safe error handling."""
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
            handler.setLevel(logging.INFO)
            handler.setFormatter(self._get_formatter())
            self._logger.addHandler(handler)
        except OSError as e:
            print(f"[LOGGER WARNING] Cannot create log file '{log_file}': {e}")

    def _add_console_handler(self) -> None:
        """Add console handler."""
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    # ---------------------------------------------------------
    # NEW: Add Handler (Polymorphism)
    # ---------------------------------------------------------
    def add_handler(self, handler: logging.Handler) -> None:
        """Add a custom handler—fully polymorphic."""
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    # ---------------------------------------------------------
    # NEW: Overloaded log() method
    # ---------------------------------------------------------
    @overload
    def log(self, message: str) -> None: ...

    @overload
    def log(self, message: str, *, level: int) -> None: ...

    def log(self, message: str, *, level: int = logging.INFO) -> None:
        """Overloaded method for logging with optional level."""
        self._logger.log(level, message)

    # ---------------------------------------------------------
    # Dynamic Runtime Configuration
    # ---------------------------------------------------------
    def configure(
        self,
        *,
        level: int = logging.INFO,
        log_format: str | None = None,
        date_format: str | None = None,
    ) -> None:
        """Dynamically update logger formatting + level."""
        if log_format:
            self._format = log_format
        if date_format:
            self._date_format = date_format

        self._logger.setLevel(level)

        # Update formatter for all handlers
        for handler in self._logger.handlers:
            handler.setFormatter(self._get_formatter())

    # ---------------------------------------------------------
    # Regular Logging API
    # ---------------------------------------------------------
    def debug(self, msg: str) -> None:
        self._logger.debug(msg)

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def critical(self, msg: str) -> None:
        self._logger.critical(msg)

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return "Logger(singleton=True)"

    def __repr__(self) -> str:
        return "Logger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Logger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# Global shared logger instance
logger = Logger()
