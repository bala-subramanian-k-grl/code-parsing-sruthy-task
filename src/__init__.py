"""USB-PD Specification Parser.

Enterprise-grade Python toolkit for parsing USB Power Delivery specification
documents with advanced content extraction and analysis capabilities.

Main modules:
- cli: Command-line interface
- core: Core configuration and interfaces
- orchestrator: Pipeline coordination
- parser: Document parsing engines
- search: Content search functionality
- support: Report generation
- utils: Shared utilities
"""

from src.cli import CLIApp
from src.core import ContentItem, ParserMode, ParserResult, TOCEntry
from src.orchestrator import PipelineOrchestrator
from src.parser import PDFParser, ParserFactory

__version__ = "1.0.0"
__author__ = "USB-PD Parser Team"
__all__ = [
    "CLIApp",
    "PipelineOrchestrator",
    "ParserFactory",
    "PDFParser",
    "ParserMode",
    "TOCEntry",
    "ContentItem",
    "ParserResult",
]
