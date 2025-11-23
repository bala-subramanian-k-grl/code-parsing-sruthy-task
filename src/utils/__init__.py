"""Utils module for logging and timing utilities.

Provides:
- logger: Singleton application-wide logger
- timer: Decorator for measuring execution time
- Timer: Context manager for profiling sections of code
"""

from src.utils.logger import logger
from src.utils.timer import timer, Timer

__version__ = "1.1.0"
__all__ = ["logger", "timer", "Timer"]
