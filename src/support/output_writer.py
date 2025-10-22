"""Output writers with polymorphism."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TextIO, Protocol, Type, Dict, cast


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

    @abstractmethod
    def get_format(self) -> str:
        """Get output format name."""
        pass

    def __call__(self, data: Any) -> None:  # Magic method polymorphism
        """Make writer callable."""
        self.write(data)

    def __str__(self) -> str:  # Magic method polymorphism
        """String representation."""
        return f"{self.__class__.__name__}({self.output_path.name})"

    @property  # Public property
    def output_path(self) -> Path:
        """Get output path."""
        return self.__output_path

    @property
    def output_directory(self) -> Path:
        """Get output directory."""
        return self.__output_path.parent


class WriterProtocol(Protocol):  # Protocol for polymorphism
    """Protocol for writer implementations."""
    
    def write(self, data: Any) -> None:
        """Write data to output."""
        ...
    
    def get_format(self) -> str:
        """Get format name."""
        ...


class JSONLWriter(BaseWriter):  # Polymorphic implementation
    """JSONL file writer with polymorphism."""

    @property
    def file_extension(self) -> str:
        """Get file extension for this writer."""
        return ".jsonl"

    def get_format(self) -> str:  # Polymorphism
        """Get output format name."""
        return "jsonl"

    def write(self, data: Any) -> None:  # Public method
        """Write data to JSONL file."""
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                if isinstance(data, list):
                    typed_data = cast(list[Any], data)
                    self._write_list(f, typed_data)
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
            logger.warning("Serialization error: %s", e)


class CSVWriter(BaseWriter):  # Additional polymorphic implementation
    """CSV file writer."""

    def get_format(self) -> str:  # Polymorphism
        """Get output format name."""
        return "csv"

    def write(self, data: Any) -> None:  # Polymorphism
        """Write data to CSV file."""
        import csv
        try:
            with open(
                self.output_path, "w", newline="", encoding="utf-8"
            ) as f:
                if isinstance(data, list) and data:
                    typed_data = cast(list[dict[str, Any]], data)
                    first_row = typed_data[0]
                    field_names = list(first_row.keys())
                    writer = csv.DictWriter(f, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(typed_data)
        except (OSError, AttributeError) as e:
            msg = f"Cannot write CSV to {self.output_path}: {e}"
            raise RuntimeError(msg) from e


class XMLWriter(BaseWriter):  # Polymorphic implementation
    """XML file writer."""

    def get_format(self) -> str:  # Polymorphism
        """Get output format name."""
        return "xml"

    def write(self, data: Any) -> None:  # Polymorphism
        """Write data to XML file."""
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<data>\n')
                if isinstance(data, list):
                    typed_data = cast(list[Any], data)
                    for item in typed_data:
                        f.write('  <item>\n')
                        if isinstance(item, dict):
                            typed_item = cast(dict[str, Any], item)
                            for key, value in typed_item.items():
                                f.write(f'    <{key}>{value}</{key}>\n')
                        f.write('  </item>\n')
                f.write('</data>\n')
        except OSError as e:
            msg = f"Cannot write XML to {self.output_path}: {e}"
            raise RuntimeError(msg) from e


class HTMLWriter(BaseWriter):  # Polymorphic implementation
    """HTML file writer."""

    def get_format(self) -> str:  # Polymorphism
        """Get output format name."""
        return "html"

    def write(self, data: Any) -> None:  # Polymorphism
        """Write data to HTML file."""
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write('<!DOCTYPE html>\n<html><head>')
                f.write('<title>Data Export</title></head><body>\n')
                f.write('<table border="1">\n')
                if isinstance(data, list) and data:
                    typed_data = cast(list[dict[str, Any]], data)
                    first_row = typed_data[0]
                    headers = list(first_row.keys())
                    f.write('<tr>')
                    for header in headers:
                        f.write(f'<th>{header}</th>')
                    f.write('</tr>\n')
                    for item in typed_data:
                        typed_item = item
                        f.write('<tr>')
                        for header in headers:
                            value = typed_item.get(header, '')
                            f.write(f'<td>{value}</td>')
                        f.write('</tr>\n')
                f.write('</table>\n</body></html>\n')
        except OSError as e:
            msg = f"Cannot write HTML to {self.output_path}: {e}"
            raise RuntimeError(msg) from e


class WriterFactory:  # Factory for polymorphism
    """Factory to create writer instances."""
    
    @staticmethod
    def create(format_type: str, output_path: Path) -> BaseWriter:
        """Create writer - runtime polymorphism."""
        writers: Dict[str, Type[BaseWriter]] = {
            "jsonl": JSONLWriter,
            "csv": CSVWriter,
            "xml": XMLWriter,
            "html": HTMLWriter
        }
        if format_type not in writers:
            raise ValueError(f"Unknown format: {format_type}")
        return writers[format_type](output_path)
