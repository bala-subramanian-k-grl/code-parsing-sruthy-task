"""
Parser Mode Strategies for CLI.

Implements the Strategy Pattern used to decide
parser behavior based on user input.
"""

from abc import ABC, abstractmethod
from typing import Type

from src.core.config.constants import ParserMode


# =========================
# Base Strategy
# =========================

class BaseModeStrategy(ABC):
    """Abstract base strategy for parser modes."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-friendly mode name."""
        raise NotImplementedError

    @abstractmethod
    def get_mode(self) -> ParserMode:
        """Return the parser mode."""
        raise NotImplementedError


# =========================
# Concrete Strategies
# =========================

class FullModeStrategy(BaseModeStrategy):
    @property
    def name(self) -> str:
        return "full"

    def get_mode(self) -> ParserMode:
        return ParserMode.FULL


class TocModeStrategy(BaseModeStrategy):
    @property
    def name(self) -> str:
        return "toc"

    def get_mode(self) -> ParserMode:
        return ParserMode.TOC


class ContentModeStrategy(BaseModeStrategy):
    @property
    def name(self) -> str:
        return "content"

    def get_mode(self) -> ParserMode:
        return ParserMode.CONTENT


# =========================
# Factory
# =========================

class ModeStrategyFactory:
    """Factory to create strategies from CLI arguments."""

    _default_strategy: Type[BaseModeStrategy] = FullModeStrategy

    _mode_map: dict[str, Type[BaseModeStrategy]] = {
        "full": FullModeStrategy,
        "toc": TocModeStrategy,
        "content": ContentModeStrategy,
    }

    def create(self, mode_str: str) -> BaseModeStrategy:
        """
        Return a strategy instance based on input string.
        Defaults to full mode if unknown.
        """
        mode_key = (mode_str or "").lower()
        strategy_cls = self._mode_map.get(mode_key, self._default_strategy)
        return strategy_cls()
