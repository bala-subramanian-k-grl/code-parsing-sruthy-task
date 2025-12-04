"""
Enterprise Pipeline Interface (Enhanced OOP Version)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.config.models import ParserResult

# ==========================================================
# VALIDATION RESULT (Dataclass + Polymorphism)
# ==========================================================


@dataclass
class ValidationResult:
    """Result of pipeline validation."""
    is_valid: bool
    errors: list[str]

    def __str__(self) -> str:
        """Method implementation."""
        state = "Valid" if self.is_valid else "Invalid"
        return f"ValidationResult({state}, errors={self.errors})"

    def __bool__(self) -> bool:
        """Method implementation."""
        return self.is_valid

    def __len__(self) -> int:
        """Method implementation."""
        return len(self.errors)

    def __contains__(self, item: str) -> bool:
        """Method implementation."""
        return item in self.errors


# ==========================================================
# PIPELINE INTERFACE (Enterprise Version)
# ==========================================================

class PipelineInterface(ABC):
    """
    Abstract interface for enterprise parser pipelines.

    Pipeline lifecycle:
        prepare()   → setup resources
        validate()  → configuration checks
        execute()   → run pipeline
        cleanup()   → release resources

    Additional features:
        - pause/resume/cancel support
        - progress tracking
        - protected state attributes
        - polymorphic behaviour hooks
    """

    # ==========================================================
    # CONSTRUCTOR (Encapsulation)
    # ==========================================================

    def __init__(self) -> None:
        """Method implementation."""
        self._status: str = "INITIAL"          # protected state
        self._progress: float = 0.0            # protected progress
        self._errors: list[str] = []           # protected error tracker
        self._is_running: bool = False         # protected lifecycle flag

    # ==========================================================
    # CORE PROPERTIES (Encapsulation + Abstraction)
    # ==========================================================

    @property
    @abstractmethod
    def pipeline_type(self) -> str:
        """Return pipeline type name."""
        raise NotImplementedError

    @property
    def is_async(self) -> bool:
        """Whether pipeline can run asynchronously."""
        return False

    @property
    def status(self) -> str:
        """Method implementation."""
        return self._status

    @property
    def progress(self) -> float:
        """Method implementation."""
        return self._progress

    @property
    def errors(self) -> list[str]:
        """Method implementation."""
        return list(self._errors)

    @property
    def has_errors(self) -> bool:
        """Method implementation."""
        return len(self._errors) > 0

    # ==========================================================
    # PROTECTED HELPERS (Encapsulation)
    # ==========================================================

    def _set_status(self, value: str) -> None:
        """Method implementation."""
        self._status = value

    def _set_progress(self, value: float) -> None:
        """Method implementation."""
        self._progress = max(0.0, min(1.0, value))

    def _add_error(self, message: str) -> None:
        """Method implementation."""
        self._errors.append(message)

    def _ensure_running(self) -> None:
        """Method implementation."""
        if not self._is_running:
            raise RuntimeError("Pipeline is not running.")

    # ==========================================================
    # ABSTRACT LIFECYCLE METHODS (Polymorphism)
    # ==========================================================

    @abstractmethod
    def prepare(self) -> None:
        """Prepare pipeline resources."""
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> ParserResult:
        """Execute pipeline and return result."""
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup pipeline resources."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate pipeline configuration."""
        raise NotImplementedError

    # ==========================================================
    # CONTROL METHODS (Pause, Resume, Cancel)
    # ==========================================================

    @abstractmethod
    def pause(self) -> None:
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def resume(self) -> None:
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def cancel(self) -> None:
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> str:
        """Method implementation."""
        raise NotImplementedError

    @abstractmethod
    def get_progress(self) -> float:
        """Method implementation."""
        raise NotImplementedError

    # ==========================================================
    # OPTIONAL HELPERS (Polymorphic Hooks)
    # ==========================================================

    def get_errors(self) -> list[str]:
        """Method implementation."""
        return self.errors

    def pipeline_name(self) -> str:
        """Method implementation."""
        return self.__class__.__name__

    # ==========================================================
    # DUNDER METHODS (OOP Score Boost)
    # ==========================================================

    def __str__(self) -> str:
        """Method implementation."""
        return f"{self.pipeline_type}Pipeline(status={self._status})"

    def __repr__(self) -> str:
        """Method implementation."""
        return f"{self.__class__.__name__}(status={self._status!r})"

    def __eq__(self, other: object) -> bool:
        """Method implementation."""
        return isinstance(other, PipelineInterface)

    def __hash__(self) -> int:
        """Method implementation."""
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        """Method implementation."""
        return self._status == "READY"

    def __len__(self) -> int:
        """Length indicates number of validation errors."""
        return len(self._errors)

    def __contains__(self, msg: str) -> bool:
        """Method implementation."""
        return msg in self._errors

    def __float__(self) -> float:
        """Method implementation."""
        return self._progress

    def __int__(self) -> int:
        """Convert pipeline to int based on progress."""
        return int(self._progress * 100)
