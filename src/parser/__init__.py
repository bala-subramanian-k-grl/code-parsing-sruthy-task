"""Parser module."""

from src.parser.base_parser import BaseParser
from src.parser.parser_factory import ParserFactory
from src.parser.pdf_parser import PDFParser
from src.parser.text_parser import TextParser

__all__ = ["BaseParser", "PDFParser", "TextParser", "ParserFactory"]
