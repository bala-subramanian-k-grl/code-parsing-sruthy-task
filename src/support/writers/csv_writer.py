"""CSV Writer Module"""

import csv
from pathlib import Path
from typing import Any, cast

from src.support.writers.base_writer import BaseWriter


class CSVWriter(BaseWriter):  # Inheritance and Polymorphism
    """CSV file writer with proper encapsulation."""

    def __init__(self, output_path: Path):
        """Initialize CSV writer."""
        super().__init__(output_path)
        self.__delimiter = ","  # Private delimiter setting
        self.__encoding = "utf-8"  # Private encoding setting

    @property  # Encapsulation
    def file_extension(self) -> str:
        """Get file extension for this writer."""
        return ".csv"

    @property  # Encapsulation
    def delimiter(self) -> str:
        """Get CSV delimiter."""
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        """Set CSV delimiter with validation."""
        if len(value) != 1:
            raise ValueError("Delimiter must be a single character")
        self.__delimiter = value

    def get_format(self) -> str:  # Polymorphism
        """Get output format name."""
        return "csv"

    def validate_data(self, data: Any) -> bool:  # Polymorphism
        """Validate data for CSV format."""
        if not super().validate_data(data):
            return False

        if not isinstance(data, list) or not data:
            return False

        return all(isinstance(item, dict) for item in data if item is not None)

    def write(self, data: Any) -> None:  # Polymorphism
        """Write data to CSV file."""
        if not self.validate_data(data):
            raise ValueError("Data must be a non-empty list of dictionaries")

        try:
            with open(
                self.output_path, "w", newline="", encoding=self.__encoding
            ) as f:
                typed_data = cast("list[dict[str, Any]]", data)
                self.__write_csv_data(f, typed_data)
        except OSError as e:
            msg = f"Cannot write CSV to {self.output_path}: {e}"
            raise RuntimeError(msg) from e

    def __write_csv_data(self, f: Any, data: list[dict[str, Any]]) -> None:
        """Write CSV data with headers."""
        if not data:
            return

        field_names = self.__get_field_names(data)
        writer = csv.DictWriter(
            f, fieldnames=field_names, delimiter=self.__delimiter
        )
        writer.writeheader()
        writer.writerows(data)

    def __get_field_names(self, data: list[dict[str, Any]]) -> list[str]:
        """Get field names from data."""
        if not data:
            return []

        # Get all unique keys from all dictionaries
        all_keys: set[str] = set()
        for item in data:
            all_keys.update(item.keys())

        return sorted(all_keys)

    def append_row(self, row: dict[str, Any]) -> None:
        """Append a single row to existing CSV file."""
        if not row:
            raise ValueError("Row cannot be empty")

        try:
            # Check if file exists to determine if we need headers
            file_exists = self.output_path.exists()

            with open(
                self.output_path, "a", newline="", encoding=self.__encoding
            ) as f:
                if not file_exists:
                    # Write header for new file
                    field_names = list(row.keys())
                    writer = csv.DictWriter(
                        f, fieldnames=field_names, delimiter=self.__delimiter
                    )
                    writer.writeheader()
                    writer.writerow(row)
                else:
                    # For existing file, assume headers are already there
                    field_names = list(row.keys())
                    writer = csv.DictWriter(
                        f, fieldnames=field_names, delimiter=self.__delimiter
                    )
                    writer.writerow(row)
        except OSError as e:
            msg = f"Cannot append to CSV {self.output_path}: {e}"
            raise RuntimeError(msg) from e
