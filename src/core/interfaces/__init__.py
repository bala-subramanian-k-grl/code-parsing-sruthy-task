"""Interfaces module for abstract base classes.

Provides:
- ParserInterface: Abstract parser interface
- ExtractionStrategy: Abstract extraction strategy
- PipelineInterface: Abstract pipeline interface
- ValidationResult: Pipeline validation result
"""

from src.core.interfaces.extraction_strategy import ExtractionStrategy
from src.core.interfaces.parser_interface import ParserInterface
from src.core.interfaces.pipeline_interface import (PipelineInterface,
                                                     ValidationResult)
from src.core.interfaces.report_interface import IReportGenerator

__version__ = "1.0.0"
__all__ = [
    "ParserInterface",
    "ExtractionStrategy",
    "PipelineInterface",
    "ValidationResult",
    "IReportGenerator"
]
