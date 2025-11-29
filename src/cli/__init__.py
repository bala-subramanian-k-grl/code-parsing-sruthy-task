"""
CLI package initializer.
"""

from src.cli.app import BaseCLI, CLIApp

# Public exports
__all__ = ["BaseCLI", "CLIApp"]

__private__ = ["_get_version"]

# Package version
__version__ = "1.0.0"


def _get_version() -> str:
    """
    Protected accessor for package version.

    Returns:
        str: Current CLI package version.
    """
    return __version__
