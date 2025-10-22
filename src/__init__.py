"""USB PD Specifications Parser - Main Package"""

from .config import Config
from .core import PipelineOrchestrator
from .core.extractors import PDFExtractor, TOCExtractor
from .loggers import get_logger
from .support import JSONLWriter

__version__ = "1.0.0"
__all__ = [
    "Config",
    "PipelineOrchestrator",
    "PDFExtractor",
    "TOCExtractor",
    "get_logger",
    "JSONLWriter",
]
