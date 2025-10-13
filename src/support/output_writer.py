# USB PD Specification Parser - Output Writer Module
"""Output writers with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TextIO, Union


class BaseWriter(ABC):  # Abstraction: abstract base class
    """Abstract writer (Abstraction, Encapsulation)."""

    def __init__(self, output_path: Path):
        self._output_path = self._validate_path(output_path)  # Encapsulation

    def _validate_path(self, path: Path) -> Path:  # Encapsulation
        """Validate and secure output path."""
        safe_path = path.resolve()  # Prevent path traversal
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        return safe_path

    @abstractmethod  # Abstraction: must be implemented by subclasses
    def write(self, data: Any) -> None:
        """Abstract write method."""
        pass

    @property  # Encapsulation: controlled access
    def output_path(self) -> Path:
        """Get output path."""
        return self._output_path


class JSONLWriter(BaseWriter):  # Inheritance: extends BaseWriter
    """JSONL file writer (Inheritance, Polymorphism)."""

    def write(self, data: Union[list[Any], Any]) -> None:  # Polymorphism
        """Write data to JSONL file."""
        try:
            with open(self._output_path, "w", encoding="utf-8") as f:
                if isinstance(data, list):
                    self._write_list(f, data)
                else:
                    self._write_single(f, data)
        except OSError as e:
            raise RuntimeError(f"Cannot write to {self._output_path}: {e}") from e

    def _write_list(self, f: TextIO, data: list[Any]) -> None:  # Encapsulation: private
        """Write list of items."""
        for item in data:
            self._write_single(f, item)

    def _write_single(self, f: TextIO, item: Any) -> None:  # Encapsulation: private
        """Write single item."""
        try:
            if hasattr(item, "model_dump"):
                f.write(item.model_dump_json() + "\n")
            else:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        except (TypeError, ValueError) as e:
            import logging

            logging.getLogger(__name__).warning(f"Serialization error: {e}")
