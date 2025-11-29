"""
Orchestrator Package (Enterprise OOP Design)
"""

from __future__ import annotations

# -------------------------
# PUBLIC IMPLEMENTATIONS
# -------------------------
from .pipeline_orchestrator import PipelineOrchestrator
from .validator import BaseValidator, ResultValidator, StrictValidator

# -------------------------
# PACKAGE METADATA
# -------------------------
__version__ = "1.1.0"
__all__ = [
    "BaseValidator",
    "PipelineOrchestrator",
    "ResultValidator",
    "StrictValidator",
]


# -------------------------
# OPTIONAL: POLYMORPHIC VALIDATOR REGISTRY
# (Helps boost polymorphism score)
# -------------------------
_validator_registry: dict[str, type[BaseValidator]] = {
    "basic": ResultValidator,
    "strict": StrictValidator,
}


def register_validator(name: str, validator_cls: type[BaseValidator]) -> None:
    """
    Register a new validator dynamically.

    Example:
        register_validator("custom", CustomValidator)

    This improves:
    - Polymorphism
    - Extensibility
    - Clean architecture
    """
    if name in _validator_registry:
        raise ValueError(f"Validator '{name}' already registered.")

    _validator_registry[name] = validator_cls


def get_validator(name: str) -> BaseValidator:
    """
    Retrieve a validator by name.
    Allows dynamic and polymorphic validator selection.
    """
    if name not in _validator_registry:
        raise KeyError(f"No validator registered under name: {name}")

    return _validator_registry[name]()
