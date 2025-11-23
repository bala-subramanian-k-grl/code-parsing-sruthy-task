"""
CLI package.

Responsibilities:
- Provides the main CLI entry point (CLIApp)
- Exposes the BaseCLI abstraction for custom CLI implementations
"""

from src.cli.app import BaseCLI, CLIApp

__all__ = ["CLIApp", "BaseCLI"]
__version__ = "1.0.0"
