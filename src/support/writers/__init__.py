"""Writers module exports"""

from typing import Any

from .base_writer import BaseWriter, WriterProtocol
from .csv_writer import CSVWriter
from .jsonl_writer import JSONLWriter

__all__ = [
    "BaseWriter",
    "WriterProtocol",
    "CSVWriter",
    "JSONLWriter",
]


class WriterFactory:  # Factory for polymorphism
    """Factory to create writer instances."""

    @staticmethod
    def create(format_type: str, output_path: Any) -> BaseWriter:
        """Create writer - runtime polymorphism."""
        from pathlib import Path

        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        writers: dict[str, type[BaseWriter]] = {
            "jsonl": JSONLWriter,
            "csv": CSVWriter,
        }

        if format_type not in writers:
            available = ", ".join(writers.keys())
            raise ValueError(
                f"Unknown format: {format_type}. Available: {available}"
            )

        return writers[format_type](output_path)
