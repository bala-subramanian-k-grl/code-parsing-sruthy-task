"""USB PD Specification Parser - A modular PDF content extraction tool."""
__version__ = "1.0.0"
__author__ = "USB PD Parser Team"

from .core.models import TOCEntry
from .core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

__all__ = [
    "PipelineOrchestrator",
    "TOCEntry",
]
