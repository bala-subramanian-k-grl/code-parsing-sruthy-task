#!/usr/bin/env python3
"""Generate USB PD metadata file from existing spec data."""

import json
from pathlib import Path
from typing import Any


def generate_metadata():
    """Generate metadata JSONL from spec file."""
    spec_file = Path("outputs/usb_pd_spec.jsonl")
    metadata_file = Path("outputs/usb_pd_metadata.jsonl")
    
    if not spec_file.exists():
        print(f"Spec file not found: {spec_file}")
        return
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        with open(metadata_file, 'w', encoding='utf-8') as out:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    metadata: dict[str, Any] = {
                        "doc_title": data.get("doc_title", "USB PD Specification"),
                        "section_id": data.get("section_id", ""),
                        "page": data.get("page", 1),
                        "type": data.get("type", "paragraph"),
                        "word_count": len(data.get("content", "").split()),
                        "char_count": len(data.get("content", ""))
                    }
                    out.write(json.dumps(metadata) + '\n')
    
    print(f"Generated {metadata_file}")


if __name__ == "__main__":
    generate_metadata()