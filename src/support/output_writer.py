"""Output writers - Modular Architecture."""

# Re-export from modular writers for backward compatibility
from src.support.writers import (
    BaseWriter,
    CSVWriter,
    JSONLWriter,
    WriterFactory,
    WriterProtocol,
)

__all__ = [
    "BaseWriter",
    "WriterProtocol",
    "JSONLWriter",
    "CSVWriter",
    "WriterFactory",
]
