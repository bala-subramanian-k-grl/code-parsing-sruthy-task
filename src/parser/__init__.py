"""
Parser Package (Enterprise OOP Version)
"""

from src.parser.base_parser import BaseParser
from src.parser.parser_factory import ParserFactory
from src.parser.pdf_parser import PDFParser
from src.parser.text_parser import TextParser
from src.parser.toc_extractor import TOCExtractor

# -------------------------------------------------------
# PACKAGE METADATA (ENCAPSULATION)
# -------------------------------------------------------

__version__ = "1.1.0"
__author__ = "USB-PD Parser Team"
__package_name__ = "parser"
__description__ = "Enterprise-level parsing engine for USB-PD Specification."

# Public API
__all__ = [
    "BaseParser",
    "PDFParser",
    "ParserFactory",
    "TOCExtractor",
    "TextParser",
]


# -------------------------------------------------------
# POLYMORPHIC PACKAGE DESCRIPTION
# -------------------------------------------------------

def package_info() -> str:
    """Return human-readable description (polymorphism)."""
    return (
        f"{__package_name__} v{__version__} — "
        f"{__description__}"
    )
