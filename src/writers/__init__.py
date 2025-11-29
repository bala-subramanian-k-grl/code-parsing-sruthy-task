"""
Writers module for file output operations.

Provides:
- JSONLWriter: Writer for JSONL output (TOC + content + metadata)
- WriterInterface: Abstract base interface for all writers

"""

from src.writers.jsonl_writer import JSONLWriter
from src.writers.writer_interface import WriterInterface

__version__ = "1.1.0"

__all__ = [
    "JSONLWriter",
    "WriterInterface",
]
