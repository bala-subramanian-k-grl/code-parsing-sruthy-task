"""Data models with OOP principles."""

from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class BaseContent(BaseModel):
    """Base content (Abstraction, Encapsulation)."""

    page: int = Field(gt=0)  # Encapsulation
    content: str = Field()  # Encapsulation

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.__content_hash: Optional[str] = None  # Private
        self.__word_count: Optional[int] = None  # Private

    @property
    def content_hash(self) -> str:
        """Get content hash."""
        if self.__content_hash is None:
            import hashlib

            self.__content_hash = hashlib.md5(
                self.content.encode(), usedforsecurity=False
            ).hexdigest()
        return self.__content_hash

    @property
    def word_count(self) -> int:
        """Get word count."""
        if self.__word_count is None:
            self.__word_count = len(self.content.split())
        return self.__word_count


class PageContent(BaseContent):  # Inheritance
    """Page content (Inheritance, Polymorphism)."""

    image_count: int = Field(ge=0, description="Number of images")
    table_count: int = Field(ge=0, description="Number of tables")


class TOCEntry(BaseModel):  # Encapsulation
    """TOC entry (Encapsulation, Abstraction)."""

    doc_title: str = Field()  # Encapsulation
    section_id: str = Field()  # Encapsulation
    title: str = Field()  # Encapsulation
    full_path: str = Field()  # Encapsulation
    page: int = Field(gt=0)  # Encapsulation
    level: int = Field(gt=0)  # Encapsulation
    parent_id: Optional[str] = Field(default=None)  # Encapsulation
    tags: list[str] = Field(default_factory=list)  # Encapsulation

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.__creation_time: Optional[Any] = None  # Private
        self.__modification_count: int = 0  # Private

    @property
    def creation_time(self) -> Optional[Any]:
        """Get creation time."""
        return self.__creation_time

    @property
    def modification_count(self) -> int:
        """Get modification count."""
        return self.__modification_count

    def __str__(self) -> str:  # Magic Method
        return f"TOCEntry({self.section_id}: {self.title})"

    def __hash__(self) -> int:  # Magic Method
        return hash((self.section_id, self.page))

    def __eq__(self, other: object) -> bool:  # Magic Method
        if not isinstance(other, TOCEntry):
            return False
        same_id = self.section_id == other.section_id
        same_page = self.page == other.page
        return same_id and same_page

    @field_validator("section_id")  # Encapsulation
    @classmethod
    def validate_section_id(cls, v: str) -> str:
        """Validate section ID (Abstraction)."""
        if not v.strip():
            raise ValueError("Empty section_id")
        return v.strip()

    @field_validator("level", mode="before")  # Encapsulation
    @classmethod
    def infer_level(cls, v: Any, info: ValidationInfo) -> int:
        """Infer level (Abstraction)."""
        if v is not None:
            return int(v)
        section_id = str(info.data.get("section_id", ""))
        return len(section_id.split("."))

    @field_validator("parent_id", mode="before")
    @classmethod
    def infer_parent(cls, v: Any, info: ValidationInfo) -> Optional[str]:
        """Infer parent (Abstraction)."""
        if v is not None:
            return str(v)
        section_id = str(info.data.get("section_id", ""))
        if "." not in section_id:
            return None
        return ".".join(section_id.split(".")[:-1])


class ContentItem(BaseContent):  # Inheritance
    """Content item (Inheritance, Polymorphism)."""

    doc_title: str = Field()  # Encapsulation
    content_id: str = Field()  # Encapsulation
    type: str = Field()  # Encapsulation
    block_id: str = Field()  # Encapsulation
    bbox: list[float] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.__processing_state: str = "new"  # Private
        self.__error_count: int = 0  # Private

    @property
    def processing_state(self) -> str:
        """Get processing state."""
        return self.__processing_state

    @property
    def error_count(self) -> int:
        """Get error count."""
        return self.__error_count
