"""USB PD Specification Parser - Pipeline Orchestrator Module"""

from src.core.orchestrator.pipeline_coordinator import PipelineCoordinator


class PipelineOrchestrator(PipelineCoordinator):  # Inheritance
    """Legacy orchestrator class for backward compatibility."""

    def __init__(self, config_path: str):
        """Initialize with new coordinator architecture."""
        super().__init__(config_path)
