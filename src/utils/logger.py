"""Logger utility."""

import logging
from pathlib import Path


def _setup_logger(
    log_file: Path = Path("outputs") / "parser.log"
) -> logging.Logger:
    """Setup logger with file and console handlers."""
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Warning: Could not create log directory: {e}")

    _logger = logging.getLogger("PDFParser")
    _logger.setLevel(logging.INFO)
    _logger.handlers.clear()

    try:
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)
    except OSError as e:
        print(f"Warning: Could not create file handler: {e}")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    return _logger


class Logger:
    """Logger wrapper with common logging methods."""

    def __init__(
        self, log_file: Path = Path("outputs") / "parser.log"
    ) -> None:
        self._logger = _setup_logger(log_file)

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


logger = Logger()
