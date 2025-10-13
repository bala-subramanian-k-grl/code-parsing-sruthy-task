import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional




class BaseLoggerFactory(ABC):  # Abstraction
    """Abstract logger factory (Abstraction, Encapsulation)."""

    def __init__(self, name: str = "usb_pd_parser"):
        self._name = name  # Encapsulation
        self._formatter = self._create_formatter()  # Encapsulation
        self._setup_stream_logger()  # Encapsulation

    def _setup_stream_logger(self) -> None:  # Encapsulation
        """Setup stream logger to capture all logs to parser.log."""
        root_logger = logging.getLogger()
        if not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
            try:
                log_file = Path("outputs") / "parser.log"
                log_file.parent.mkdir(parents=True, exist_ok=True)
                fh = logging.FileHandler(log_file)
                fh.setLevel(logging.INFO)
                fh.setFormatter(self._formatter)
                root_logger.addHandler(fh)
                root_logger.setLevel(logging.INFO)
            except OSError:
                pass  # Silently fail if can't create log file

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


# Initialize stream logger when module is imported
_logger_factory = None

def _ensure_stream_logger():
    global _logger_factory
    if _logger_factory is None:
        from .logger import LoggerFactory
        _logger_factory = LoggerFactory()

_ensure_stream_logger()