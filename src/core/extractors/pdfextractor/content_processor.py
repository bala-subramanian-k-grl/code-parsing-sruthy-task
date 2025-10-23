"""Content Processing Logic Module"""

from dataclasses import dataclass
from typing import Any, Optional

from src.config.constants import MAX_TITLE_LENGTH, MIN_TEXT_LENGTH
from src.core.analyzer.content_analyzer import ContentAnalyzer


@dataclass
class ContentItemData:
    """Data class for content item creation."""

    text: str
    content_type: str
    block_num: int
    page_num: int
    block: dict[str, Any]


class ContentProcessor:  # Encapsulation
    """Processes content with classification and validation."""

    def __init__(self) -> None:
        """Initialize content processor."""
        self.__analyzer = ContentAnalyzer()  # Private composition
        self.__stats: dict[str, int] = {}  # Private statistics
        self.__processing_mode = "standard"  # Private mode

    @property
    def stats(self) -> dict[str, int]:  # Encapsulation
        """Get processing statistics (read-only)."""
        return self.__stats.copy()

    @property
    def processing_mode(self) -> str:  # Encapsulation
        """Get processing mode."""
        return self.__processing_mode

    @processing_mode.setter
    def processing_mode(self, mode: str) -> None:
        """Set processing mode with validation."""
        valid_modes = ["standard", "fast", "comprehensive"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}")
        self.__processing_mode = mode

    def process_block_data(
        self, block_data: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Process block data and return content item."""
        block = block_data["block"]
        block_num = block_data["block_num"]
        page_num = block_data["page_num"]

        text = self.__extract_block_text(block)
        if not self.__is_valid_text(text):
            return None

        content_type = self.__analyzer.classify(text)
        self.__update_stats(content_type)

        item_data = ContentItemData(
            text=text,
            content_type=content_type,
            block_num=block_num,
            page_num=page_num,
            block=block,
        )
        return self.__create_content_item(item_data)

    def __extract_block_text(self, block: dict[str, Any]) -> str:
        """Extract text from block."""
        text_parts = [
            str(span["text"])
            for line in block["lines"]
            for span in line["spans"]
        ]
        return "".join(text_parts)

    def __is_valid_text(self, text: str) -> bool:
        """Check if text is valid for processing."""
        return bool(text.strip()) and len(text) > MIN_TEXT_LENGTH

    def __update_stats(self, content_type: str) -> None:
        """Update processing statistics."""
        self.__stats[content_type] = self.__stats.get(content_type, 0) + 1

    def __create_content_item(self, data: ContentItemData) -> dict[str, Any]:
        """Create content item dictionary."""
        title = self.__get_title(data.text)
        prefix = data.content_type[0]
        page = data.page_num + 1
        section_id = f"{prefix}{page}_{data.block_num}"

        return {
            "doc_title": "USB PD Specification",
            "section_id": section_id,
            "title": title,
            "content": data.text.strip(),
            "page": page,
            "level": 1,
            "parent_id": None,
            "full_path": title,
            "type": data.content_type,
            "block_id": section_id,
            "bbox": list(data.block.get("bbox", [])),
        }

    def __get_title(self, text: str) -> str:
        """Get title from text."""
        return self.__truncate_text(text.strip(), MAX_TITLE_LENGTH)

    def __truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to maximum length."""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    def reset_stats(self) -> None:
        """Reset processing statistics."""
        self.__stats.clear()

    def process_table_data(
        self, table: Any, page_num: int, table_num: int
    ) -> Optional[dict[str, Any]]:
        """Process table data."""
        if not self.__is_valid_table(table):
            return None

        table_text = self.__format_table_text(table)
        return {
            "type": "table",
            "content": table_text,
            "page": page_num + 1,
            "block_id": f"tbl{page_num + 1}_{table_num}",
            "bbox": [],
        }

    def __is_valid_table(self, table: Any) -> bool:
        """Check if table is valid for processing."""
        return table and len(table) > 1

    def __format_table_text(self, table: Any) -> str:
        """Format table as text."""
        rows = [" | ".join(str(cell or "") for cell in row) for row in table]
        return "\n".join(rows)
