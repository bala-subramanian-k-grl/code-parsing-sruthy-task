"""Text parser implementation."""

from pathlib import Path

from src.core.config.models import ContentItem, ParserResult
from src.parser.base_parser import BaseParser


class TextParser(BaseParser):
    """Concrete text parser."""

    def __init__(self, file_path: Path, doc_title: str = "Document") -> None:
        super().__init__(file_path)
        self._doc_title = doc_title

    def parse(self) -> ParserResult:
        """Parse text file and extract content."""
        try:
            with self._file_path.open("r", encoding="utf-8") as f:
                content = f.read()

            items = [
                ContentItem(
                    doc_title=self._doc_title,
                    section_id="text_content",
                    title=self._doc_title,
                    content=content,
                    page=1,
                )
            ]
            return ParserResult(content_items=items)
        except (OSError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to parse text file: {e}") from e

    def validate(self) -> bool:
        """Validate text file has .txt extension."""
        return super().validate() and self._file_path.suffix.lower() == ".txt"
