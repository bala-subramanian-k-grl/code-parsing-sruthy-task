"""Parser module for document parsing.

Provides:
- BaseParser: Abstract base parser class
- PDFParser: PDF document parser
- TextParser: Text file parser
- ParserFactory: Factory for creating parsers
- TOCExtractor: Table of contents extractor
"""

from src.parser.base_parser import BaseParser
from src.parser.parser_factory import ParserFactory
from src.parser.pdf_parser import PDFParser
from src.parser.text_parser import TextParser
from src.parser.toc_extractor import TOCExtractor

__version__ = "1.0.0"
__all__ = [
    "BaseParser",
    "PDFParser",
    "TextParser",
    "ParserFactory",
    "TOCExtractor"
]
