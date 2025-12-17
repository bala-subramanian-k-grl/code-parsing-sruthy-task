# Architecture

## System Overview

USB-PD Parser transforms unstructured PDF content into structured, hierarchical data through a modular pipeline.

**Problem:** USB-PD specs are 1,000+ page technical documents with complex hierarchies and dense content.

**Solution:** Automated extraction with 75.2% coverage, hierarchical structuring, and multiple output formats.

---

## System Layers

```
User Interface (CLI, API)
    ↓
Orchestration (PipelineOrchestrator)
    ↓
Processing (Parser, Extractors, Writers)
    ↓
Support (Reports, Metadata, Logging)
    ↓
Infrastructure (Config, Interfaces, Utils)
```

---

## Core Components

### 1. Input Layer - Parser Module

**Responsibility:** Read and validate PDF documents

**Components:**
- **ParserFactory** - Creates parser based on file type (extensible)
- **PDFParser** - High-performance PDF parsing with PyMuPDF
- **TextParser** - Fallback for text files

**Data Flow:**
```
PDF File → ParserFactory → PDFParser → ParserResult
```

**Validation:**
- File exists
- Size ≤ 100MB
- Valid PDF structure
- Readable permissions

---

### 2. Processing Layer - Extractors

**Responsibility:** Transform raw PDF data into structured content

**Components:**

**TOCExtractor:**
- Reads PDF's native TOC
- Builds parent-child relationships
- Generates section IDs (1.2.3)
- Output: `List[TOCEntry]`

**ContentExtractor:**
- Processes text blocks per page
- Normalizes and cleans text
- Generates bounding boxes
- Output: `List[ContentItem]`

**TextExtractor:**
- Low-level text extraction from blocks

---

### 3. Output Layer - Writers

**Responsibility:** Serialize data to multiple formats

**Components:**
- **JSONLWriter** - Line-delimited JSON (streaming-friendly)
- **ExcelReportGenerator** - Validation dashboard
- **JSONReportGenerator** - Comprehensive report
- **MetadataGenerator** - Document statistics

**Output Files:**
```
outputs/
├── usb_pd_toc.jsonl          # Table of contents
├── usb_pd_spec.jsonl         # Full content
├── usb_pd_metadata.jsonl     # Statistics
├── parsing_report.json       # Detailed report
├── validation_report.xlsx    # Excel dashboard
└── parser.log                # Execution log
```

---

### 4. Orchestration Layer

**PipelineOrchestrator** - Coordinates entire workflow

**Execution Flow:**
```
1. Start logging
2. Create output directory
3. Validate input
4. Parse document
5. Write JSONL files
6. Generate reports
7. Log completion
8. Cleanup
```

**Key Features:**
- Lifecycle management
- Error handling
- Progress tracking
- Configuration management

---

### 5. Support Layer

**Configuration Module:**
- ConfigLoader - Dynamic settings
- ConstantManager - Encapsulated constants
- ParserMode - Enum (TOC, CONTENT, FULL)

**Utilities:**
- Logger - Thread-safe singleton
- Timer - Execution timing

---

## Design Patterns

| Pattern | Usage |
|---------|-------|
| **Factory** | Parser creation by file type |
| **Strategy** | Extraction modes |
| **Template Method** | Pipeline execution |
| **Singleton** | Logger instance |
| **Observer** | Progress tracking |
| **Chain of Responsibility** | Validation pipeline |

---

## Data Structures

**TOCEntry:**
```python
section_id: str          # "1.2.3"
title: str              # Section title
page: int               # Page number
level: int              # Hierarchy level
parent_id: str          # Parent section ID
full_path: str          # "Intro > Overview > Protocol"
```

**ContentItem:**
```python
doc_title: str          # Document title
section_id: str         # Block ID
title: str              # Content title
content: str            # Text content
page: int               # Page number
block_id: str           # Block identifier
bbox: list              # Bounding box [x1, y1, x2, y2]
```

---

## Performance

**Algorithm Complexity:**
- TOC Extraction: O(n)
- Content Extraction: O(n)
- Hierarchy Building: O(n)
- JSONL Writing: O(n)

**Benchmarks (1,046-page USB PD spec):**
| Operation | Time | Memory |
|-----------|------|--------|
| Parsing | 2.3s | 45MB |
| TOC Extraction | 0.8s | 12MB |
| Content Extraction | 3.1s | 120MB |
| JSONL Writing | 1.2s | 8MB |
| Report Generation | 0.6s | 15MB |
| **Total** | **~8s** | **<500MB** |

**Processing Speed:** ~1,000 items/sec

---

## Extensibility

### Adding New Parser Types
```python
class DocxParser(BaseParser):
    def parse(self) -> ParserResult:
        pass

ParserFactory.register_parser(".docx", DocxParser)
```

### Custom Extraction Strategies
```python
class CustomExtractor(ExtractorInterface):
    def extract(self, data: Any) -> list[ContentItem]:
        pass
```

### Adding Report Formats
```python
class CSVReportGenerator(BaseReportGenerator):
    def generate(self, result: ParserResult, output_path: Path) -> None:
        pass
```

---

## Module Dependencies

```
PipelineOrchestrator
├─ ParserFactory
│  ├─ PDFParser
│  └─ TextParser
├─ TOCExtractor
├─ ContentExtractor
│  └─ TextExtractor
├─ JSONLWriter
├─ MetadataGenerator
├─ JSONReportGenerator
└─ ExcelReportGenerator

All depend on:
├─ ConfigLoader
├─ Logger
├─ Timer
└─ Constants
```

---

## Error Handling

**Validation Pipeline:**
```
File Exists? → PDF Format? → Size Valid? → Readable? → Has Content?
```

**Error Recovery:**
| Error | Handling | Recovery |
|-------|----------|----------|
| File Not Found | Raise FileNotFoundError | Provide valid path |
| Invalid Format | Raise ValueError | Use supported format |
| Corrupted PDF | Log warning, skip page | Continue processing |
| Memory Exceeded | Raise MemoryError | Process smaller chunks |
| Write Permission | Raise PermissionError | Check output directory |

---

## Testing

**Test Categories:**
- Functional tests (Core functionality)
- OOP tests (Design principles)
- Performance tests (Benchmarks)
- Regression tests (Prevent regressions)
- Coverage tests (Coverage boost)

**Coverage:** 95%+

**Run Tests:**
```bash
pytest -v                                    # All tests
pytest tests/functional_tests/ -v            # Specific category
pytest --cov=src --cov-report=html          # With coverage
pytest tests/performance_tests/ --benchmark-only  # Performance
```

---

## Technology Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| PDF Processing | PyMuPDF (fitz) | High performance, native TOC |
| Excel Generation | openpyxl | Pure Python, no dependencies |
| Testing | pytest | Industry standard |
| Type Checking | mypy | Static type safety |
| Linting | ruff/flake8 | Code quality |

---

## Key Design Decisions

1. **Hierarchical TOC** - Stack-based algorithm for O(n) parent-child relationships
2. **JSONL Format** - Line-delimited JSON for streaming efficiency
3. **Encapsulation** - Private attributes with property getters
4. **Method Overloading** - Type-safe multiple signatures
5. **Factory with Fallback** - Extensible parser creation

---

## Scalability Roadmap

| Aspect | Current | Target | Strategy |
|--------|---------|--------|----------|
| Document Size | 1,000 pages | 10,000+ pages | Streaming, chunking |
| Processing Speed | 1,000 items/sec | 5,000+ items/sec | Parallelization |
| Memory Usage | <500MB | <200MB | Lazy loading |
| Concurrent Jobs | 1 | 100+ | Job queue, workers |
| Output Formats | 6 | 15+ | Plugin architecture |

---

## Installation & Usage

**Install:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Usage:**
```bash
python main.py                    # Interactive
python -m src.cli.app --file <pdf> --mode full  # CLI
python search.py "keyword" outputs/usb_pd_spec.jsonl  # Search
```

---

**Version:** 1.0 | **Status:** Production Ready
