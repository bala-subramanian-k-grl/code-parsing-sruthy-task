"""JSONL Writer Module"""

import json
from pathlib import Path
from typing import Any, TextIO

from src.support.writers.base_writer import BaseWriter


class JSONLWriter(BaseWriter):  # Inheritance and Polymorphism
    """JSONL file writer with proper encapsulation."""

    def __init__(self, output_path: Path):
        """Initialize JSONL writer."""
        super().__init__(output_path)
        self.__encoding = "utf-8"  # Private encoding setting

    @property  # Encapsulation
    def file_extension(self) -> str:
        """Get file extension for this writer."""
        return ".jsonl"

    @property  # Encapsulation
    def encoding(self) -> str:
        """Get file encoding."""
        return self.__encoding

    def get_format(self) -> str:  # Polymorphism
        """Get output format name."""
        return "jsonl"

    def validate_data(self, data: Any) -> bool:  # Polymorphism
        """Validate data for JSONL format."""
        return super().validate_data(data)

    def write(self, data: Any) -> None:  # Polymorphism
        """Write data to JSONL file."""
        if not self.validate_data(data):
            raise ValueError("Invalid data for JSONL format")

        try:
            with open(self.output_path, "w", encoding=self.__encoding) as f:
                if isinstance(data, list):
                    self.__write_list(f, list(data))
                else:
                    self.__write_single(f, data)
        except OSError as e:
            msg = f"Cannot write to {self.output_path}: {e}"
            raise RuntimeError(msg) from e

    def __write_list(self, f: TextIO, data: list[Any]) -> None:  # Private
        """Write list of items."""
        for item in data:
            self.__write_single(f, item)

    def __write_single(self, f: TextIO, item: Any) -> None:  # Private
        """Write single item."""
        try:
            if hasattr(item, "model_dump"):
                f.write(item.model_dump_json() + "\n")
            else:
                json_str = json.dumps(item, ensure_ascii=False)
                f.write(json_str + "\n")
        except (TypeError, ValueError) as e:
            self.__log_error(f"Serialization error: {e}")

    def __log_error(self, message: str) -> None:  # Private
        """Log error message."""
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(message)

    def append(self, data: Any) -> None:
        """Append data to existing JSONL file."""
        if not self.validate_data(data):
            raise ValueError("Invalid data for JSONL format")

        try:
            with open(self.output_path, "a", encoding=self.__encoding) as f:
                if isinstance(data, list):
                    self.__write_list(f, list(data))
                else:
                    self.__write_single(f, data)
        except OSError as e:
            msg = f"Cannot append to {self.output_path}: {e}"
            raise RuntimeError(msg) from e
