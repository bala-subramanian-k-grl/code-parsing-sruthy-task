"""Metadata generator with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseMetadataGenerator(ABC):
    """Abstract metadata generator."""

    def __init__(self, output_dir: Path):
        """Initialize generator."""
        self._output_dir = output_dir

    @abstractmethod
    def generate_metadata(self, spec_file: Path) -> Path:
        """Generate metadata file."""
        pass


class JSONLMetadataGenerator(BaseMetadataGenerator):
    """JSONL metadata generator."""

    def generate_metadata(self, spec_file: Path) -> Path:
        """Generate metadata from spec file."""
        metadata_file = self._output_dir / "usb_pd_metadata.jsonl"
        
        if not spec_file.exists():
            return metadata_file
            
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                with open(metadata_file, 'w', encoding='utf-8') as out:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            metadata = self._create_metadata(data)
                            out.write(json.dumps(metadata) + '\n')
        except (OSError, json.JSONDecodeError):
            pass
            
        return metadata_file

    def _create_metadata(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create metadata entry."""
        content = data.get("content", "")
        return {
            "doc_title": data.get("doc_title", "USB PD Specification"),
            "section_id": data.get("section_id", ""),
            "page": data.get("page", 1),
            "type": data.get("type", "paragraph"),
            "word_count": len(content.split()),
            "char_count": len(content)
        }


def create_metadata_file(output_dir: Path, spec_file: Path) -> Path:
    """Factory function to create metadata file."""
    generator = JSONLMetadataGenerator(output_dir)
    return generator.generate_metadata(spec_file)