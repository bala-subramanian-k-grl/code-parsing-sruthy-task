"""Logger with OOP principles."""

import logging
from pathlib import Path
from typing import Optional

from .base_logger import BaseLoggerFactory


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
            name = safe_dir.name
            clean_name = name.replace("_", "").replace("-", "")
            if not clean_name.isalnum():
                msg = f"Invalid directory name: {safe_dir.name}"
                raise ValueError(msg)
            safe_dir.mkdir(parents=True, exist_ok=True)
            log_file = safe_dir / "parser.log"
            # Validate log file path to prevent traversal
            log_resolved = log_file.resolve()
            safe_resolved = safe_dir.resolve()
            if not log_resolved.is_relative_to(safe_resolved):
                raise ValueError("Log file path traversal detected")
            fh = logging.FileHandler(log_file)
            fh.setLevel(log_level)
            fh.setFormatter(self._formatter)
            logger.addHandler(fh)
        except OSError as e:
            logger.warning(f"Could not create file handler: {e}")

    def _validate_output_dir(self, output_dir: Path) -> Path:  # Encapsulation
        """Validate output directory against security vulnerabilities."""
        try:
            # Sanitize input to prevent command injection
            path_str = str(output_dir)
            sanitized = (
                path_str.replace("..", "").replace(";", "").replace("|", "")
            )
            clean_path = Path(sanitized)
            resolved_path = clean_path.resolve(strict=False)
            working_dir = Path.cwd().resolve()

            # Prevent path traversal attacks
            if not resolved_path.is_relative_to(working_dir):
                msg = f"Path traversal detected: {output_dir}"
                raise ValueError(msg)

            # Additional security check for suspicious patterns
            path_str = str(resolved_path)
            suspicious_chars = ["&", "`", "$", "(", ")", "<", ">"]
            has_suspicious = any(char in path_str for char in suspicious_chars)
            if has_suspicious:
                msg = f"Suspicious characters in path: {output_dir}"
                raise ValueError(msg)

            return resolved_path
        except (OSError, ValueError) as e:
            error_msg = f"Invalid output directory: {output_dir} - {e}"
            raise ValueError(error_msg) from e


def get_logger(
    name: str = "usb_pd_parser",
    output_dir: Optional[Path] = None,
    debug: bool = False,
) -> logging.Logger:
    """Get logger instance."""
    factory = LoggerFactory(name)  # Polymorphism
    return factory.create_logger(output_dir, debug)
