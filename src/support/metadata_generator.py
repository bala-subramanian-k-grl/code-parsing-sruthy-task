"""Metadata generators with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Type


class BaseMetadataGenerator(ABC):
    """Abstract metadata generator."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize generator."""
        self.__output_dir = output_dir  # Private
        self.__stats: dict[str, int] = {}  # Private

    @property
    def output_dir(self) -> Path:
        """Get output directory."""
        return self.__output_dir

    @property
    def stats(self) -> dict[str, int]:
        """Get generation statistics."""
        return self.__stats.copy()

    @abstractmethod
    def generate_metadata(self, spec_file: Path) -> Path:
        """Generate metadata file."""
        pass

    def _update_stats(self, key: str, value: int) -> None:
        """Update internal statistics."""
        self.__stats[key] = value


class JSONLMetadataGenerator(BaseMetadataGenerator):
    """JSONL metadata generator."""

    def generate_metadata(self, spec_file: Path) -> Path:  # Polymorphism
        """Generate metadata from spec file."""
        metadata_file = self.output_dir / "usb_pd_metadata.jsonl"
        entry_count = 0

        if not spec_file.exists():
            self._update_stats("entries_processed", 0)
            return metadata_file

        try:
            with open(spec_file, encoding='utf-8') as f:
                with open(metadata_file, 'w', encoding='utf-8') as out:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            metadata = self._create_metadata(data)
                            out.write(json.dumps(metadata) + '\n')
                            entry_count += 1
        except (OSError, json.JSONDecodeError) as e:
            import logging
            logging.getLogger(__name__).debug("Metadata generation error: %s", e)

        self._update_stats("entries_processed", entry_count)
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


class CSVMetadataGenerator(BaseMetadataGenerator):
    """CSV metadata generator."""

    def generate_metadata(self, spec_file: Path) -> Path:  # Polymorphism
        """Generate CSV metadata from spec file."""
        metadata_file = self.output_dir / "usb_pd_metadata.csv"
        entry_count = 0

        if not spec_file.exists():
            self._update_stats("entries_processed", 0)
            return metadata_file

        try:
            with open(metadata_file, 'w', encoding='utf-8') as out:
                # Write CSV header
                out.write("doc_title,section_id,page,type,word_count,char_count\n")
                
                with open(spec_file, encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            metadata = self._create_csv_row(data)
                            out.write(metadata + '\n')
                            entry_count += 1
        except (OSError, json.JSONDecodeError) as e:
            import logging
            logging.getLogger(__name__).debug("CSV generation error: %s", e)

        self._update_stats("entries_processed", entry_count)
        return metadata_file

    def _create_csv_row(self, data: dict[str, Any]) -> str:
        """Create CSV row from data."""
        content = data.get("content", "")
        doc_title = data.get("doc_title", "USB PD Specification")
        section_id = data.get("section_id", "")
        page = data.get("page", 1)
        data_type = data.get("type", "paragraph")
        word_count = len(content.split())
        char_count = len(content)
        
        return f"{doc_title},{section_id},{page},{data_type},{word_count},{char_count}"


class MetadataGeneratorFactory:
    """Factory for metadata generators."""
    
    __GENERATORS: dict[str, Type[BaseMetadataGenerator]] = {
        "jsonl": JSONLMetadataGenerator,
        "csv": CSVMetadataGenerator  # Polymorphism - different implementations
    }
    
    @classmethod
    def create(cls, generator_type: str, output_dir: Path) -> BaseMetadataGenerator:
        """Create metadata generator instance."""
        if generator_type not in cls.__GENERATORS:
            raise ValueError(f"Unknown generator type: {generator_type}")
        return cls.__GENERATORS[generator_type](output_dir)


def create_metadata_file(output_dir: Path, spec_file: Path) -> Path:
    """Factory function to create metadata file."""
    generator = MetadataGeneratorFactory.create("jsonl", output_dir)
    return generator.generate_metadata(spec_file)
