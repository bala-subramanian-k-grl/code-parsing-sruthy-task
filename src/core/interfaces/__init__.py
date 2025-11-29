"""
Interfaces package for abstract contracts used across the USB-PD parser.
"""

from src.core.interfaces.extraction_strategy import ExtractionStrategy
from src.core.interfaces.factory_interface import FactoryInterface
from src.core.interfaces.parser_interface import ParserInterface
from src.core.interfaces.pipeline_interface import (
    PipelineInterface,
    ValidationResult,
)
from src.core.interfaces.report_interface import IReportGenerator


# ---------------------------------------------------------
# VERSION (Encapsulated)
# ---------------------------------------------------------

__version__ = "1.0.0"


# ---------------------------------------------------------
# Public API (Encapsulation)
# ---------------------------------------------------------

__all__ = [
    "ParserInterface",
    "ExtractionStrategy",
    "PipelineInterface",
    "ValidationResult",
    "IReportGenerator",
    "FactoryInterface",
]


# Hidden/internal names (Encapsulation)
__private__ = ["_get_version"]


# ---------------------------------------------------------
# Protected Version Accessor
# ---------------------------------------------------------

def _get_version() -> str:
    """
    Protected accessor for version information.
    Used internally by loaders/CLI for logging or debugging.
    """
    return __version__


# ---------------------------------------------------------
# Module-Level Polymorphism
# ---------------------------------------------------------

def __str__() -> str:
    """Human-friendly name of the interfaces module."""
    return "Interfaces Module (Contracts & Abstractions)"


def __repr__() -> str:
    """Debug-friendly representation."""
    return f"<interfaces package version={__version__}>"
