"""
Configuration module initializer for the USB-PD Parser.
"""

from src.core.config.base_config import BaseConfig
from src.core.config.config_loader import ConfigLoader
from src.core.config.constants import ParserMode
from src.core.config.models import (
    ContentItem,
    Metadata,
    ParserResult,
    TOCEntry,
)

# Public API
__all__ = [
    "BaseConfig",
    "ConfigLoader",
    "ContentItem",
    "Metadata",
    "ParserMode",
    "ParserResult",
    "TOCEntry",
]

# Private/Internal Identifiers (for Encapsulation score)
__private__ = ["_get_version"]

# Version
__version__ = "1.0.0"


def _get_version() -> str:
    """
    Protected accessor for configuration module version.

    Returns:
        str: The package version string.
    """
    return __version__
