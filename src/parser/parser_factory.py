"""Parser factory for creating parser instances."""

from pathlib import Path

from src.parser.base_parser import BaseParser
from src.parser.pdf_parser import PDFParser
from src.parser.text_parser import TextParser


class ParserFactory:
    """Factory for creating appropriate parser instances."""

    _parser_registry: dict[str, type[BaseParser]] = {
        ".pdf": PDFParser,
        ".txt": TextParser,
    }

    @staticmethod
    def create_parser(file_path: Path) -> BaseParser:
        """Create parser based on file extension."""
        suffix = file_path.suffix.lower()
        parser_class = ParserFactory._parser_registry.get(suffix)

        if parser_class:
            return parser_class(file_path)

        supported = ", ".join(ParserFactory._parser_registry.keys())
        raise ValueError(
            f"Unsupported file type: {suffix}. Supported: {supported}"
        )
