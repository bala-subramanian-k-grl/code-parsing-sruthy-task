"""Content extraction from PDF documents."""

from typing import Any

from src.core.config.models import ContentItem
from src.extractors.text_extractor import TextExtractor


class ContentExtractor:
    """Extract content items from PDF documents."""

    _TITLE_MAX_LENGTH = 100
    _MIN_TEXT_LENGTH = 1

    def __init__(self, doc_title: str) -> None:
        if not doc_title:
            raise ValueError("doc_title cannot be empty")
        self.__doc_title = doc_title
        self.__text_extractor = TextExtractor()

    def extract(self, data: Any) -> list[ContentItem]:
        """Extract all content from PDF document."""
        items: list[ContentItem] = []
        for page_num, page in enumerate(data, start=1):
            items.extend(self._extract_from_page(page, page_num))
        return items

    def _extract_from_page(
        self, page: Any, page_num: int
    ) -> list[ContentItem]:
        """Extract content from single page."""
        text_dict = page.get_text("dict")
        blocks = text_dict["blocks"]
        items: list[ContentItem] = []
        for block_num, block in enumerate(blocks):
            if not self._is_valid_block(block):
                continue
            text = self.__text_extractor.extract(block)
            if not self._is_valid_text(text):
                continue
            items.append(
                self._build_content_item(text, page_num, block_num, block)
            )
        return items

    def _is_valid_block(self, block: dict[str, Any]) -> bool:
        """Check if block contains valid lines."""
        return "lines" in block

    def _is_valid_text(self, text: str) -> bool:
        """Check if extracted text is valid."""
        return len(text.strip()) >= self._MIN_TEXT_LENGTH

    def _build_content_item(
        self, text: str, page_num: int, block_num: int, block: dict[str, Any]
    ) -> ContentItem:
        """Build ContentItem from extracted data."""
        block_id = self._generate_block_id(page_num, block_num)
        return ContentItem(
            doc_title=self.__doc_title,
            section_id=block_id,
            title=text[:self._TITLE_MAX_LENGTH],
            content=text,
            page=page_num,
            block_id=block_id,
            bbox=list(block.get("bbox", []))
        )

    @staticmethod
    def _generate_block_id(page_num: int, block_num: int) -> str:
        """Generate unique block identifier."""
        return f"p{page_num}_{block_num}"

    @property
    def doc_title(self) -> str:
        """Get document title."""
        return self.__doc_title

    def __str__(self) -> str:
        return f"ContentExtractor(doc_title={self.__doc_title})"

    def __repr__(self) -> str:
        return f"ContentExtractor(doc_title={self.__doc_title!r})"
