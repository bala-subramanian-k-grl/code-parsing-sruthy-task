"""Interfaces module."""

from src.core.interfaces.extraction_strategy import ExtractionStrategy
from src.core.interfaces.parser_interface import ParserInterface
from src.core.interfaces.pipeline_interface import PipelineInterface

__all__ = ["ParserInterface", "ExtractionStrategy", "PipelineInterface"]
