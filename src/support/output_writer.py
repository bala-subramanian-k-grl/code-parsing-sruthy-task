"""Output writers with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TextIO


class BaseWriter(ABC):  # Abstraction: abstract base class
    """Abstract writer (Abstraction, Encapsulation)."""

    def __init__(self, output_path: Path):
        """Initialize writer with output path."""
        self.__output_path = self._validate_path(output_path)  # Private

    def _validate_path(self, path: Path) -> Path:  # Protected method
        """Validate and secure output path."""
        safe_path = path.resolve()  # Prevent path traversal
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        return safe_path

    @abstractmethod  # Abstraction: must be implemented by subclasses
    def write(self, data: Any) -> None:
        """Abstract write method."""
        pass

    @property  # Public property
    def output_path(self) -> Path:
        """Get output path."""
        return self.__output_path
    
    def get_output_directory(self) -> Path:  # Public method
        """Get output directory."""
        return self.__output_path.parent


class JSONLWriter(BaseWriter):  # Inheritance: extends BaseWriter
    """JSONL file writer (Inheritance, Polymorphism)."""
    
    def get_file_extension(self) -> str:  # Public method
        """Get file extension for this writer."""
        return ".jsonl"

    def write(self, data: Any) -> None:  # Public method
        """Write data to JSONL file."""
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                if isinstance(data, list):
                    self._write_list(f, data)
                else:
                    self._write_single(f, data)
        except OSError as e:
            msg = f"Cannot write to {self.output_path}: {e}"
            raise RuntimeError(msg) from e

    def _write_list(self, f: TextIO, data: list[Any]) -> None:  # Protected
        """Write list of items."""
        for item in data:
            self._write_single(f, item)

    def _write_single(self, f: TextIO, item: Any) -> None:  # Protected
        """Write single item."""
        try:
            if hasattr(item, "model_dump"):
                f.write(item.model_dump_json() + "\n")
            else:
                json_str = json.dumps(item, ensure_ascii=False)
                f.write(json_str + "\n")
        except (TypeError, ValueError) as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Serialization error: {e}")
