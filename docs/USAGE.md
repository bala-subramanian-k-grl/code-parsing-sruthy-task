# Usage Guide

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/sruthypanigrahi/code-parsing.git
cd code-parsing

# Install dependencies
pip install -r requirements.txt

# Run with interactive interface
python main.py
```

### Basic Usage

```bash
# Interactive mode (recommended)
python main.py

# Direct mode selection
python main.py --mode 3  # Standard mode (200 pages)
python main.py --mode 2  # Extended mode (600 pages)
python main.py --mode 1  # Full document

# Specialized extraction
python main.py --toc-only     # Extract only Table of Contents
python main.py --content-only # Extract only content
```

## Processing Modes

### Mode 1: Full Document
- Processes entire PDF (all pages)
- Memory intensive
- Complete extraction
- Use for comprehensive analysis

```bash
python main.py --mode 1
```

### Mode 2: Extended Mode
- Processes first 600 pages
- Balanced performance/coverage
- Good for large documents
- Recommended for detailed analysis

```bash
python main.py --mode 2
```

### Mode 3: Standard Mode (Recommended)
- Processes first 200 pages
- Memory efficient
- Fast processing
- Ideal for most use cases

```bash
python main.py --mode 3
```

## Output Files

The parser generates 5 comprehensive output files:

### 1. TOC File (`usb_pd_toc.jsonl`)
Table of Contents entries in JSONL format.

```json
{
  "doc_title": "USB PD Specification",
  "section_id": "1.1",
  "title": "Introduction",
  "full_path": "1. Overview > 1.1 Introduction",
  "page": 15,
  "level": 2,
  "parent_id": "1",
  "tags": ["introduction", "overview"]
}
```

### 2. Specification Content (`usb_pd_spec.jsonl`)
Complete document content with metadata.

```json
{
  "doc_title": "USB PD Specification",
  "section_id": "p1_0",
  "title": "Universal Serial Bus",
  "content": "Universal Serial Bus Power Delivery Specification...",
  "page": 1,
  "level": 1,
  "parent_id": null,
  "full_path": "Universal Serial Bus",
  "type": "paragraph",
  "block_id": "p1_0",
  "bbox": [171.33, 62.91, 423.95, 95.74]
}
```

### 3. Parsing Report (`parsing_report.json`)
Processing metadata and statistics.

```json
{
  "processing_info": {
    "start_time": "2024-12-19T10:30:00Z",
    "end_time": "2024-12-19T10:30:08Z",
    "duration_seconds": 8.45,
    "mode": "Standard Mode (200 pages)",
    "pages_processed": 200
  },
  "extraction_stats": {
    "toc_entries": 369,
    "content_items": 4403,
    "tables_extracted": 45,
    "images_found": 12
  },
  "validation_results": {
    "jsonl_format_valid": true,
    "required_fields_present": true,
    "data_integrity_check": "passed"
  }
}
```

### 4. Validation Report (`validation_report.xlsx`)
Excel report comparing TOC vs parsed content with styling.

- **Summary Sheet**: Overview statistics
- **TOC Analysis**: Table of Contents validation
- **Content Analysis**: Content extraction validation
- **Discrepancies**: Issues found during processing

### 5. Processing Log (`parser.log`)
Detailed processing logs with security tracking.

```
2024-12-19 10:30:00,123 - PipelineOrchestrator - INFO - Configuration loaded successfully
2024-12-19 10:30:00,456 - PipelineOrchestrator - INFO - Starting pipeline execution - Mode: Standard (200 pages)
2024-12-19 10:30:02,789 - PDFExtractor - INFO - Executing extract_content
2024-12-19 10:30:05,012 - PDFExtractor - INFO - extract_content took 2.23 seconds
2024-12-19 10:30:06,345 - TOCExtractor - INFO - TOC extraction completed: 369 entries found
2024-12-19 10:30:08,678 - PipelineOrchestrator - INFO - Pipeline execution completed successfully
```

## Search Functionality

### Basic Search

```bash
# Search in extracted content
python search.py "USB Power Delivery"

# Search in specific file
python search.py "connector" outputs/usb_pd_spec.jsonl

# Case-sensitive search
python search.py "USB" --case-sensitive
```

### Advanced Search Options

```bash
# Search with context
python search.py "voltage" --context 2

# Search with regex
python search.py "USB.*PD" --regex

# Search in TOC only
python search.py "introduction" outputs/usb_pd_toc.jsonl
```

## Configuration

### YAML Configuration (`application.yml`)

```yaml
# Processing mode settings
input:
  max_pages:
    mode_1: null  # Full document
    mode_2: 600   # Extended mode
    mode_3: 200   # Standard mode

# OOP features
oop:
  use_abstract_classes: true
  enable_polymorphism: true
  magic_methods: true
  property_decorators: true

# Decorator settings
processing:
  decorators:
    timing: true
    logging: true
    retry: true
    validation: true

# Security settings
security:
  validate_paths: true
  prevent_path_traversal: true
  cwe_compliance: true
```

## Advanced Usage

### Custom Processing

```python
from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

# Initialize with custom config
orchestrator = PipelineOrchestrator("custom_config.yml")

# Run with specific parameters
result = orchestrator.run_full_pipeline(
    mode=3,
    extract_tables=True,
    generate_reports=True
)

print(f"Processed {result['spec_counts']['content_items']} items")
```

### Using Decorators

```python
from src.utils.decorators import timing, log_execution, retry

class CustomProcessor:
    @timing
    @log_execution
    @retry(max_attempts=3)
    def process_document(self, pdf_path):
        # Your processing logic here
        return self._extract_content(pdf_path)
```

### Magic Methods Usage

```python
from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor
from pathlib import Path

# Create extractor
extractor = PDFExtractor(Path("document.pdf"))

# Use magic methods
print(extractor)  # PDFExtractor(document.pdf)
items = extractor(max_pages=100)  # Callable interface
total = len(extractor)  # Get total items
```

## Performance Optimization

### Memory Management

```bash
# For large documents, use extended mode
python main.py --mode 2

# For memory-constrained systems, use standard mode
python main.py --mode 3

# Monitor memory usage
python profile_performance.py
```

### Processing Speed

```bash
# Fastest processing (recommended)
python main.py --mode 3

# Balance speed and coverage
python main.py --mode 2

# Complete but slower
python main.py --mode 1
```

## Error Handling

### Common Issues

#### File Not Found
```bash
ERROR - PDF file not found: assets/missing.pdf
Solution: Ensure PDF file exists in assets/ directory
```

#### Permission Denied
```bash
ERROR - Permission denied: outputs/
Solution: Check write permissions for outputs/ directory
```

#### Memory Issues
```bash
ERROR - Memory limit exceeded
Solution: Use smaller processing mode (--mode 3)
```

### Debug Mode

```bash
# Enable debug logging
python main.py --mode 3 --debug

# Check log file for details
type outputs\parser.log
```

## Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/ -m "unit"        # Unit tests only
pytest tests/ -m "integration" # Integration tests only
pytest tests/ -m "not slow"    # Skip slow tests
```

### Performance Benchmarks

```bash
# Run performance benchmarks
python profile_performance.py

# View results
type benchmark_results.txt
```

## Security Features

### Path Validation
- Automatic path traversal prevention
- Input sanitization
- File type validation

### CWE Compliance
- CWE-22: Path Traversal
- CWE-77: Command Injection
- CWE-78: OS Command Injection
- CWE-88: Argument Injection

### Security Scanning

```bash
# Run security scan
bandit -r src/

# Check dependencies
safety check

# Vulnerability assessment
semgrep --config=auto src/
```

## Troubleshooting

### Common Solutions

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **PDF Processing Errors**: Check PDF file integrity
   ```bash
   python -c "import fitz; doc = fitz.open('assets/your_file.pdf'); print(f'Pages: {len(doc)}')"
   ```

3. **Output File Issues**: Verify write permissions
   ```bash
   mkdir outputs
   chmod 755 outputs
   ```

4. **Memory Issues**: Use smaller processing mode
   ```bash
   python main.py --mode 3
   ```

### Getting Help

- Check the log file: `outputs/parser.log`
- Run with debug mode: `--debug`
- Review error messages for specific guidance
- Consult API documentation: `docs/API.md`