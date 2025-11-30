"""
ContentExtractor
-----------------
Enterprise-grade content extraction component.

Implements:
- Strategy Pattern compatibility
- Full OOP: Encapsulation, Polymorphism, Abstraction
- Clean extension hooks for NLP/ML enhancements
- Safe internal state handling
"""

from __future__ import annotations

from typing import Any

from src.core.config.models import ContentItem
from src.extractors.extractor_interface import ExtractorInterface
from src.extractors.text_extractor import TextExtractor


class ContentExtractor(ExtractorInterface):
    """Extract structured content items from PDF documents."""

    # ==========================================================
    # CLASS-LEVEL CONSTANTS (ENCAPSULATION)
    # ==========================================================
    _TITLE_MAX_LENGTH = 100
    _MIN_TEXT_LENGTH = 1

    # ==========================================================
    # INITIALIZATION
    # ==========================================================
    def __init__(self, doc_title: str) -> None:
        self.__doc_title = doc_title.strip()
        self.__text_extractor = TextExtractor()
        self._validate_init()

    def _validate_init(self) -> None:
        """Encapsulated initializer validation."""
        if not self.__doc_title:
            msg = "ContentExtractor requires a non-empty doc_title."
            raise ValueError(msg)

    # ==========================================================
    # PROPERTIES (ENCAPSULATION + POLYMORPHISM)
    # ==========================================================
    @property
    def extractor_type(self) -> str:
        return "ContentExtractor"

    @property
    def is_stateful(self) -> bool:
        return True  # holds document title

    # ==========================================================
    # PRIMARY EXTRACTION ENTRY (POLYMORPHISM)
    # ==========================================================
    def extract(self, data: Any) -> list[ContentItem]:
        """Extract content from entire PDF document."""
        results: list[ContentItem] = []

        for page_num, page in enumerate(data, start=1):
            processed_page = self._preprocess_page(page)
            results.extend(self._extract_from_page(processed_page, page_num))

        return results

    # ==========================================================
    # VALIDATION HOOK
    # ==========================================================
    def validate(self) -> None:
        if not self.__doc_title:
            msg = "ContentExtractor validation failed: Missing title"
            raise ValueError(msg)

    # ==========================================================
    # HOOKS FOR EXTENSIBILITY
    # ==========================================================
    def _preprocess_page(self, page: Any) -> Any:
        """
        Hook: future NLP/image preprocessing.
        Can be overridden by subclasses.
        """
        return page

    def _normalize_text(self, text: str) -> str:
        """Hook: normalize extracted text."""
        return text.replace("\n", " ").strip()

    def _clean_text(self, text: str) -> str:
        """Internal cleaning with encapsulation."""
        return " ".join(text.split())

    # ==========================================================
    # PAGE-LEVEL EXTRACTION
    # ==========================================================
    def _extract_from_page(
        self, page: Any, page_num: int
    ) -> list[ContentItem]:
        """Extract structured content from a single page."""
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])

        items: list[ContentItem] = []

        for block_num, block in enumerate(blocks):
            if not self._is_valid_block(block):
                continue

            raw_text = self.__text_extractor.extract(block)
            text = self._normalize_text(raw_text)

            if not self._is_valid_text(text):
                continue

            text = self._clean_text(text)

            items.append(
                self._build_content_item(
                    text=text,
                    page_num=page_num,
                    block_num=block_num,
                    block=block,
                )
            )

        return items

    # ==========================================================
    # VALIDATION HELPERS
    # ==========================================================
    def _is_valid_block(self, block: dict[str, Any]) -> bool:
        return "lines" in block

    def _is_valid_text(self, text: str) -> bool:
        return len(text.strip()) >= self._MIN_TEXT_LENGTH

    # ==========================================================
    # MODEL CREATION
    # ==========================================================
    def _build_content_item(
        self,
        text: str,
        page_num: int,
        block_num: int,
        block: dict[str, Any],
    ) -> ContentItem:
        block_id = self._generate_block_id(page_num, block_num)

        return ContentItem(
            doc_title=self.__doc_title,
            section_id=block_id,
            title=text[: self._TITLE_MAX_LENGTH],
            content=text,
            page=page_num,
            block_id=block_id,
            bbox=list(block.get("bbox", [])),
        )

    @staticmethod
    def _generate_block_id(page_num: int, block_num: int) -> str:
        return f"p{page_num}_{block_num}"

    # ==========================================================
    # READ-ONLY PUBLIC PROPERTIES (ENCAPSULATION)
    # ==========================================================
    @property
    def doc_title(self) -> str:
        return self.__doc_title

    @property
    def title_length(self) -> int:
        return len(self.__doc_title)

    @property
    def has_title(self) -> bool:
        return bool(self.__doc_title)

    @property
    def title_words(self) -> int:
        return len(self.__doc_title.split())

    @property
    def title_chars(self) -> int:
        return len(self.__doc_title)

    @property
    def title_upper(self) -> str:
        return self.__doc_title.upper()

    @property
    def title_lower(self) -> str:
        return self.__doc_title.lower()

    @property
    def title_capitalized(self) -> str:
        return self.__doc_title.capitalize()

    @property
    def title_stripped(self) -> str:
        return self.__doc_title.strip()

    @property
    def title_is_empty(self) -> bool:
        return not self.__doc_title.strip()

    @property
    def title_is_uppercase(self) -> bool:
        return self.__doc_title.isupper()

    @property
    def title_is_lowercase(self) -> bool:
        return self.__doc_title.islower()

    @property
    def title_first_char(self) -> str:
        return self.__doc_title[0] if self.__doc_title else ""

    @property
    def title_last_char(self) -> str:
        return self.__doc_title[-1] if self.__doc_title else ""

    @property
    def title_reversed(self) -> str:
        return self.__doc_title[::-1]

    # ==========================================================
    # MAGIC METHODS (CLEAN + CONSISTENT)
    # ==========================================================
    def __str__(self) -> str:
        return f"ContentExtractor(title={self.__doc_title})"

    def __repr__(self) -> str:
        return f"ContentExtractor(doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ContentExtractor)
            and self.__doc_title == other.__doc_title
        )

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.__doc_title))

    def __len__(self) -> int:
        return len(self.__doc_title)

    def __bool__(self) -> bool:
        return bool(self.__doc_title)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ContentExtractor):
            return NotImplemented
        return self.__doc_title < other.__doc_title

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, ContentExtractor):
            return NotImplemented
        return self.__doc_title > other.__doc_title

    def __ge__(self, other: object) -> bool:
        return self == other or self > other

    def __add__(self, other: str) -> str:
        return self.__doc_title + other

    def __mul__(self, other: int) -> str:
        return self.__doc_title * other

    def __getitem__(self, index: int) -> str:
        return self.__doc_title[index]

    def __contains__(self, text: str) -> bool:
        return text.lower() in self.__doc_title.lower()

    def __enter__(self) -> "ContentExtractor":
        return self

    def __int__(self) -> int:
        return len(self.__doc_title)

    def __float__(self) -> float:
        return float(len(self.__doc_title))
