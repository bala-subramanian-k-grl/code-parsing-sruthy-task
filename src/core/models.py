# USB PD Specification Parser - Data Models Module
"""Data models with OOP principles."""

from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class BaseContent(BaseModel):  # Abstraction
    """Base content (Abstraction, Encapsulation)."""

    page: int = Field(gt=0)  # Encapsulation
    content: str = Field()  # Encapsulation


class PageContent(BaseContent):  # Inheritance
    """Page content (Inheritance, Polymorphism)."""

    image_count: int = Field(ge=0, description="Number of images on page")
    table_count: int = Field(ge=0, description="Number of tables on page")


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

    @field_validator("section_id")  # Encapsulation
    @classmethod
    def validate_section_id(cls, v: str) -> str:
        """Validate section ID (Abstraction)."""
        if not v.strip():
            raise ValueError("Empty section_id")
        import re

        if not re.match(r"^[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*$", v.strip()):
            raise ValueError(f"Invalid format: {v}")
        return v.strip()

    @field_validator("level", mode="before")  # Encapsulation
    @classmethod
    def infer_level(cls, v: Any, info: ValidationInfo) -> int:
        """Infer level (Abstraction)."""
        if v is not None:
            return int(v)
        section_id = str(info.data.get("section_id", ""))
        return len(section_id.split("."))

    @field_validator("parent_id", mode="before")  # Encapsulation
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
    bbox: list[float] = Field(default_factory=lambda: [])  # Encapsulation
    metadata: dict[str, Any] = Field(default_factory=dict)  # Encapsulation
