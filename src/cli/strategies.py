"""
Parser Mode Strategies for CLI.

"""

from abc import ABC, abstractmethod
from typing import Any, Type

from src.core.config.constants import ParserMode
from src.core.interfaces.factory_interface import FactoryInterface
from src.cli.decorators import protected_access


# =====================================================
# Base Strategy (Abstract)
# =====================================================

class BaseModeStrategy(ABC):
    """
    Abstract base class for parser mode strategies.
    Provides common polymorphic behavior.
    """

    def __init__(self) -> None:
        self.__usage_count = 0

    # ---------- Abstract Interface ----------

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-friendly strategy name."""
        raise NotImplementedError

    @abstractmethod
    def get_mode(self) -> ParserMode:
        """Return ParserMode enumeration."""
        raise NotImplementedError

    # ---------- Encapsulation: Protected Increment ----------

    @protected_access
    def _increment_usage(self) -> None:
        self.__usage_count += 1

    # ---------- Encapsulation: Property Getter ----------

    @property
    def usage_count(self) -> int:
        """Current usage count (read-only)."""
        return self.__usage_count

    # ---------- Base Polymorphism (Magic Methods) ----------

    def __str__(self) -> str:
        return f"{self.name.capitalize()}ModeStrategy"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(usage={self.usage_count})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return self.usage_count

    def __int__(self) -> int:
        return self.usage_count

    def __float__(self) -> float:
        return float(self.usage_count)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.usage_count < other.usage_count

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __contains__(self, text: str) -> bool:
        return text.lower() in self.name.lower()


# =====================================================
# Concrete Strategies
# =====================================================

class FullModeStrategy(BaseModeStrategy):

    @property
    def name(self) -> str:
        return "full"

    def get_mode(self) -> ParserMode:
        self._increment_usage()
        return ParserMode.FULL


class TocModeStrategy(BaseModeStrategy):

    @property
    def name(self) -> str:
        return "toc"

    def get_mode(self) -> ParserMode:
        self._increment_usage()
        return ParserMode.TOC


class ContentModeStrategy(BaseModeStrategy):

    @property
    def name(self) -> str:
        return "content"

    def get_mode(self) -> ParserMode:
        self._increment_usage()
        return ParserMode.CONTENT


# =====================================================
# Factory Class
# =====================================================

class ModeStrategyFactory(FactoryInterface[BaseModeStrategy]):
    """Factory to create strategies based on a mode string."""

    _default_strategy: Type[BaseModeStrategy] = FullModeStrategy

    _mode_map: dict[str, Type[BaseModeStrategy]] = {
        "full": FullModeStrategy,
        "toc": TocModeStrategy,
        "content": ContentModeStrategy,
    }

    def __init__(self) -> None:
        self.__creation_count = 0

    @property
    def creation_count(self) -> int:
        return self.__creation_count

    @protected_access
    def _increment_creation(self) -> None:
        self.__creation_count += 1

    # ---------- Factory Logic ----------

    def create(self, mode_str: str, *args: Any, **kwargs: Any) -> BaseModeStrategy:
        """Return a strategy instance based on mode string."""
        self._increment_creation()
        mode_key = (mode_str or "").lower()
        strategy_cls = self._mode_map.get(mode_key, self._default_strategy)
        return strategy_cls()

    # ---------- Polymorphism ----------

    def __str__(self) -> str:
        return "ModeStrategyFactory"

    def __repr__(self) -> str:
        return f"ModeStrategyFactory(created={self.creation_count})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ModeStrategyFactory)

    def __hash__(self) -> int:
        return hash(type(self).__name__)

    def __len__(self) -> int:
        return self.__creation_count
