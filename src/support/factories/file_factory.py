"""Factory pattern for generating missing files."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FileGenerator(ABC):
    """Abstract file generator."""

    @abstractmethod
    def generate(self, data: list[dict[str, Any]], output_path: Path) -> None:
        pass


class MetadataGenerator(FileGenerator):
    """Generate metadata JSONL file."""

    def generate(self, data: list[dict[str, Any]], output_path: Path) -> None:
        metadata = self.__create_metadata_entries(data)
        self.__write_metadata_file(metadata, output_path)

    def __create_metadata_entries(
        self, data: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:  # Private
        """Create metadata entries from data."""
        metadata: list[dict[str, Any]] = []
        for item in data:
            metadata_entry: dict[str, Any] = {
                "doc_title": item.get("doc_title", ""),
                "section_id": item.get("section_id", ""),
                "page": item.get("page", 0),
                "type": item.get("type", ""),
                "word_count": len(item.get("content", "").split()),
                "char_count": len(item.get("content", "")),
            }
            metadata.append(metadata_entry)
        return metadata

    def __write_metadata_file(
        self, metadata: list[dict[str, Any]], output_path: Path
    ) -> None:  # Private
        """Write metadata to file."""
        import json

        with open(output_path, "w", encoding="utf-8") as f:
            for metadata_item in metadata:
                f.write(json.dumps(metadata_item) + "\n")


class FileGeneratorFactory:
    """Factory for file generators."""

    @staticmethod
    def create_generator(file_type: str) -> FileGenerator:
        if file_type == "metadata":
            return MetadataGenerator()
        raise ValueError(f"Unknown file type: {file_type}")
