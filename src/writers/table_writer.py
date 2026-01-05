"""Table writer for JSONL output with enhanced OOP design."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from src.utils.logger import logger


class WriterError(Exception):
    """Custom exception for writer errors."""
    pass


class TableWriterInterface(Protocol):
    """Interface for table writers."""
    
    def write_tables(self, tables: list[dict[str, Any]], path: Path) -> None:
        """Write tables to specified path."""
        ...


class TableWriter:
    """Write extracted tables to JSONL with enhanced error handling and validation."""

    def __init__(self, doc_title: str) -> None:
        """Initialize table writer."""
        self._doc_title = self._validate_doc_title(doc_title)
        self._tables_written = 0

    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self._doc_title

    @property
    def tables_written(self) -> int:
        """Get number of tables written."""
        return self._tables_written

    def write_tables(self, tables: list[dict[str, Any]], path: Path) -> None:
        """Write tables to JSONL with comprehensive validation and error handling."""
        self._validate_inputs(tables, path)
        
        try:
            self._prepare_output_directory(path)
            self._write_tables_to_file(tables, path)
            self._tables_written = len(tables)
            logger.info(f"Successfully wrote {len(tables)} tables to {path.name}")
            
        except Exception as e:
            logger.error(f"Failed to write tables to {path}: {str(e)}")
            raise WriterError(f"Table writing failed: {str(e)}") from e

    def _validate_doc_title(self, doc_title: str) -> str:
        """Validate and sanitize document title."""
        if not doc_title or not doc_title.strip():
            raise ValueError("Document title cannot be empty")
        
        # Sanitize title for file system
        sanitized = "".join(c for c in doc_title.strip() if c.isalnum() or c in (' ', '-', '_'))
        if not sanitized:
            raise ValueError("Document title contains no valid characters")
            
        return sanitized

    def _validate_inputs(self, tables: list[dict[str, Any]], path: Path) -> None:
        """Validate input parameters."""
        if not isinstance(tables, list):
            raise TypeError("Tables must be a list")
        
        if not tables:
            logger.warning("No tables to write")
            return
        
        if not isinstance(path, Path):
            raise TypeError("Path must be a Path object")
        
        # Validate table structure
        for i, table in enumerate(tables):
            if not isinstance(table, dict):
                raise ValueError(f"Table {i} is not a dictionary")
            
            required_keys = {'page', 'data'}
            if not required_keys.issubset(table.keys()):
                missing = required_keys - table.keys()
                raise ValueError(f"Table {i} missing required keys: {missing}")

    def _prepare_output_directory(self, path: Path) -> None:
        """Ensure output directory exists."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise WriterError(f"Failed to create output directory {path.parent}: {str(e)}") from e

    def _write_tables_to_file(self, tables: list[dict[str, Any]], path: Path) -> None:
        """Write tables to JSONL file."""
        try:
            with path.open("w", encoding="utf-8") as f:
                for i, table in enumerate(tables):
                    try:
                        json_line = json.dumps(table, ensure_ascii=False)
                        f.write(json_line + "\n")
                    except (TypeError, ValueError) as e:
                        logger.error(f"Failed to serialize table {i}: {str(e)}")
                        raise WriterError(f"Serialization error for table {i}: {str(e)}") from e
                        
        except OSError as e:
            raise WriterError(f"File I/O error: {str(e)}") from e
        except PermissionError as e:
            raise WriterError(f"Permission denied: {str(e)}") from e

    def get_metadata(self) -> dict[str, Any]:
        """Get writer metadata."""
        return {
            "doc_title": self._doc_title,
            "tables_written": self._tables_written,
            "writer_type": "TableWriter"
        }