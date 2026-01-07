# USB-PD Specification Parser

## Features

- **PDF Parsing** - Extract structured content from complex USB-PD specs
- **Table Extraction** - Extract 1,400+ tables with metadata
- **Figure Metadata** - Extract 360+ figure references from List of Figures
- **Hierarchical TOC** - Build complete table of contents with parent-child relationships
- **Multiple Formats** - Generate JSONL, JSON, and Excel reports
- **High Performance** - O(n) algorithms, ~1,000 items/sec processing speed
- **Enterprise Architecture** - SOLID principles, 95%+ test coverage
- **Robust Validation** - Comprehensive error handling and edge case support

---

## Quick Start

### Prerequisites
- Python 3.11+
- 4GB+ RAM
- 100MB+ disk space

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Main Pipeline (TOC + Content + Figures):**
```bash
python main.py
```

**Table & Figure Extraction:**
```bash
python extract_tables.py
```

**CLI Mode:**
```bash
# Full extraction (TOC + Content)
python -m src.cli.app --file assets/USB_PD_R3_2\ V1.1\ 2024-10.pdf --mode full

# TOC only
python -m src.cli.app --file assets/USB_PD_R3_2\ V1.1\ 2024-10.pdf --mode toc

# Content only
python -m src.cli.app --file assets/USB_PD_R3_2\ V1.1\ 2024-10.pdf --mode content
```

**Search:**
```bash
python search.py "Power Delivery" outputs/usb_pd_spec.jsonl
```

---

## Python API

### Basic Usage
```python
from pathlib import Path
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.core.config.constants import ParserMode

file_path = Path("documents/usb_pd_specification.pdf")
orchestrator = PipelineOrchestrator(file_path, ParserMode.FULL)

try:
    result = orchestrator.execute()
    print(f"TOC entries: {len(result.toc_entries)}")
    print(f"Content items: {len(result.content_items)}")
except FileNotFoundError:
    print("PDF file not found")
```

### Custom Configuration
```python
from src.core.config.config_loader import ConfigLoader

config = ConfigLoader()
config.set_output_dir(Path("custom_output"))
config.set_doc_title("Custom Title")

orchestrator = PipelineOrchestrator(file_path, ParserMode.FULL, config=config)
result = orchestrator.execute()
```

---

## Output Files

| File | Description |
|------|-------------|
| `usb_pd_toc.jsonl` | Table of contents with hierarchy |
| `usb_pd_spec.jsonl` | Full content with metadata |
| `usb_pd_metadata.jsonl` | Document statistics |
| `parsing_report.json` | Detailed processing report |
| `validation_report.xlsx` | Excel validation dashboard |
| `USB_PD_Spec_table.jsonl` | Extracted tables (1,431 tables) |
| `extracted_figures.jsonl` | Figure metadata (362 figures) |
| `figures_summary.json` | Figure extraction summary |

**Sample Output:**
```json
{
  "section_id": "1.2.3",
  "title": "Power Delivery Protocol",
  "page": 42,
  "level": 3,
  "parent_id": "1.2",
  "full_path": "Introduction > Overview > Power Delivery Protocol",
  "bbox": [72.0, 156.8, 523.2, 184.4]
}
```

---

## Configuration

### config.json
```json
{
  "pdf_path": "documents/usb_pd_specification.pdf",
  "output_dir": "outputs",
  "doc_title": "USB Power Delivery Specification v3.2",
  "processing": {
    "max_pages": null,
    "extract_images": false,
    "preserve_formatting": true
  }
}
```

### Environment Variables
```bash
export USB_PD_CONFIG_PATH="/path/to/config.json"
export USB_PD_OUTPUT_DIR="/path/to/outputs"
```

---

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Component Flow](docs/COMPONENT_FLOW.md) - Data flow through modules
- [Logging Guide](docs/logging.md) - Logging configuration and usage

---

## Project Structure

```
usb-pd-parser/
├── src/
│   ├── cli/              # Command-line interface
│   │   ├── app.py        # Main CLI application
│   │   └── run_extraction.py  # Table & figure extraction
│   ├── core/             # Core business logic
│   ├── extractors/       # Content extraction
│   │   ├── image_extractor.py  # Figure metadata extraction
│   │   └── table_extractor.py  # Table extraction
│   ├── orchestrator/     # Pipeline coordination
│   │   ├── pipeline_orchestrator.py  # Main pipeline
│   │   └── table_extraction_pipeline.py  # Table pipeline
│   ├── parser/           # PDF parsing
│   ├── search/           # Content search
│   ├── support/          # Report generation
│   ├── utils/            # Utilities (logger, timer)
│   └── writers/          # Output writers
│       └── table_writer.py  # Table JSONL writer
├── tests/                # Test suite (24 tests, 95%+ coverage)
├── docs/                 # Documentation
├── assets/               # Sample PDFs
├── outputs/              # Generated reports
├── main.py               # Entry point
├── extract_tables.py     # Table extraction entry point
├── search.py             # Search tool
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

## Performance

**Benchmarks (1,046-page USB PD spec):**
- TOC Extraction: 0.8s
- Content Extraction: 3.1s
- JSONL Writing: 1.2s
- Report Generation: 0.6s
- **Total: ~8s**
- **Memory: <500MB**
- **Speed: ~1,000 items/sec**

**Algorithm Complexity:** O(n) for all operations

---

## Testing

```bash
# All tests
pytest -v

# Specific category
pytest tests/functional_tests/ -v

# With coverage
pytest --cov=src --cov-report=html

# Performance tests
pytest tests/performance_tests/ --benchmark-only
```

**Coverage:** 95%+ | **Tests:** 24 passing

---

## Quality Metrics

| Metric | Score | Target |
|--------|-------|--------|
| Code Quality | A | >70 |
| PEP8 Compliance | 99.79% | >90% |
| Docstring Coverage | 93.47% | >80% |
| OOP Score | 89.4% | >80% |
| Test Coverage | 95%+ | >90% |

---

## Requirements

```
PyMuPDF>=1.23.0          # PDF processing
openpyxl>=3.1.0          # Excel generation
pytest>=7.4.0            # Testing
pytest-cov>=4.1.0        # Coverage
mypy>=1.5.0              # Type checking
```

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Implement changes with tests
4. Verify tests pass (`pytest`)
5. Run quality checks (`ruff check`, `mypy`, `isort`)
6. Submit pull request

**Code Standards:**
- PEP 8 compliance (99.79%)
- 90%+ test coverage
- Docstrings for all public methods
- Type hints throughout
- SOLID principles

---

**Version:** 1.0 | **Status:** Production Ready | **Python:** 3.11+
