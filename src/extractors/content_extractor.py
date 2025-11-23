"""Content extraction from PDF documents."""

from typing import Any

from src.core.config.models import ContentItem
from src.extractors.text_extractor import TextExtractor
from src.extractors.extractor_interface import ExtractorInterface


class ContentExtractor(ExtractorInterface):
    """Extract content items from PDF documents."""

    _TITLE_MAX_LENGTH = 100
    _MIN_TEXT_LENGTH = 1

    # -------------------------------------------------
    # Encapsulated & Abstracted Initializer
    # -------------------------------------------------
    def __init__(self, doc_title: str) -> None:
        if not doc_title:
            raise ValueError("doc_title cannot be empty")

        self.__doc_title = doc_title
        self.__text_extractor = TextExtractor()

    # -------------------------------------------------
    # Required OOP Properties (ENCAPSULATION + POLYMORPHISM)
    # -------------------------------------------------

    @property
    def extractor_type(self) -> str:
        """Polymorphic extractor type identifier."""
        return "ContentExtractor"

    @property
    def is_stateful(self) -> bool:
        """This extractor holds internal state -> True."""
        return True

    # -------------------------------------------------
    # Required Abstract Method (INHERITANCE + POLYMORPHISM)
    # -------------------------------------------------

    def extract(self, data: Any) -> list[ContentItem]:
        """Extract all content from PDF document."""
        items: list[ContentItem] = []
        for page_num, page in enumerate(data, start=1):
            items.extend(self._extract_from_page(page, page_num))
        return items

    # -------------------------------------------------
    # Optional Validation (POLYMORPHISM)
    # -------------------------------------------------

    def validate(self) -> None:
        """Validate extractor configuration."""
        if not self.__doc_title:
            raise ValueError("ContentExtractor requires a document title.")

    # -------------------------------------------------
    # INTERNAL EXTRACTION LOGIC (ENCAPSULATED)
    # -------------------------------------------------

    def _extract_from_page(self, page: Any, page_num: int) -> list[ContentItem]:
        """Extract content from a single page."""
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])
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
        return "lines" in block

    def _is_valid_text(self, text: str) -> bool:
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
        return f"p{page_num}_{block_num}"

    # -------------------------------------------------
    # Existing Encapsulated Properties (UNCHANGED)
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Magic Methods (UNCHANGED)
    # -------------------------------------------------

    def __str__(self) -> str:
        return f"ContentExtractor(doc_title={self.__doc_title})"

    def __repr__(self) -> str:
        return f"ContentExtractor(doc_title={self.__doc_title!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContentExtractor):
            return NotImplemented
        return self.__doc_title == other.__doc_title

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
