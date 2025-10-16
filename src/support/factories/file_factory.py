"""Factory pattern for generating missing files."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List


class FileGenerator(ABC):
    """Abstract file generator."""
    
    @abstractmethod
    def generate(self, data: List[dict[str, Any]], output_path: Path) -> None:
        pass


class MetadataGenerator(FileGenerator):
    """Generate metadata JSONL file."""
    
    def generate(self, data: List[dict[str, Any]], output_path: Path) -> None:
        import json
        metadata = []
        for item in data:
            metadata.append({
                "doc_title": item.get("doc_title", ""),
                "section_id": item.get("section_id", ""),
                "page": item.get("page", 0),
                "type": item.get("type", ""),
                "word_count": len(item.get("content", "").split()),
                "char_count": len(item.get("content", "")),
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in metadata:
                f.write(json.dumps(item) + '\n')


class FileGeneratorFactory:
    """Factory for file generators."""
    
    @staticmethod
    def create_generator(file_type: str) -> FileGenerator:
        if file_type == "metadata":
            return MetadataGenerator()
        raise ValueError(f"Unknown file type: {file_type}")