"""Core module for configuration and interfaces.

Provides:
- ParserMode: Enum for parser operation modes
- TOCEntry: Table of contents entry model
- ContentItem: Content item model
- ParserResult: Parser execution result model
"""

from src.core.config.constants import ParserMode
from src.core.config.models import ContentItem, ParserResult, TOCEntry

__version__ = "1.0.0"
__all__ = ["ContentItem", "ParserMode", "ParserResult", "TOCEntry"]
