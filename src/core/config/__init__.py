"""Configuration module for USB-PD parser.

Provides:
- ConfigLoader: Load and manage YAML configuration
- BaseConfig: Base configuration classes
- ParserMode: Parser operation mode enum
- TOCEntry: Table of contents entry dataclass
- ContentItem: Content item dataclass
- Metadata: Metadata dataclass
- ParserResult: Parser result dataclass
"""

from src.core.config.base_config import BaseConfig
from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import (ContentItem, Metadata, ParserResult,
                                    TOCEntry)

__version__ = "1.0.0"
__all__ = [
    "BaseConfig",
    "ConfigLoader",
    "ParserMode",
    "TOCEntry",
    "ContentItem",
    "Metadata",
    "ParserResult"
]
