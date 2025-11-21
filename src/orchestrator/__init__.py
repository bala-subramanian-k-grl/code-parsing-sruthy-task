"""Orchestrator module for pipeline coordination.

Provides:
- PipelineOrchestrator: Main pipeline coordinator
- ResultValidator: Parser result validator
- StrictValidator: Strict validation requiring both TOC and content
"""

from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.orchestrator.validator import (BaseValidator, ResultValidator,
                                        StrictValidator)

__version__ = "1.0.0"
__all__ = [
    "PipelineOrchestrator",
    "BaseValidator",
    "ResultValidator",
    "StrictValidator"
]
