"""
Utils module providing application-wide utilities.

Provides:
- logger   : Singleton application-wide logger (Enterprise-grade)
- timer    : Decorator for measuring execution time
- Timer    : Context manager for profiling code blocks
"""

from src.utils.logger import logger
from src.utils.timer import Timer, timer

__version__ = "2.0.0"
__all__ = ["Timer", "logger", "timer"]
