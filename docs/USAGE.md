# Usage Guide

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/usb-pd-parser.git
cd usb-pd-parser

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Interactive mode - guided setup
python main.py

# Direct parsing with CLI
python -m src.cli.app --file documents/usb_pd_spec.pdf --mode full

# Extract table of contents only
python -m src.cli.app --file documents/usb_pd_spec.pdf --mode toc

# Extract content without TOC
python -m src.cli.app --file documents/usb_pd_spec.pdf --mode content
```

## Processing Modes

### Full Document Processing (Recommended)

```bash
python main.py
```

**Output:**
- Processes all 1,046 pages
- Generates 6 output files
- Creates 25,760+ JSONL records
- 75.2% content coverage
- Comprehensive reports

### Mode Options

```bash
# Full mode (TOC + Content)
python -m src.cli.app --file document.pdf --mode full

# TOC only
python -m src.cli.app --file document.pdf --mode toc

# Content only  
python -m src.cli.app --file document.pdf --mode content
```

## Output Files

### Generated Files (6 total)

1. **`usb_pd_toc.jsonl`** - Table of Contents (369 entries)
2. **`usb_pd_spec.jsonl`** - Full content (25,760+ items)
3. **`usb_pd_metadata.jsonl`** - Content statistics
4. **`parsing_report.json`** - Processing metadata
5. **`validation_report.xlsx`** - Excel validation report
6. **`parser.log`** - Execution logs

### JSONL Format

```json
{
  "doc_title": "USB PD Specification",
  "section_id": "p1_0",
  "title": "Universal Serial Bus",
  "content": "Universal Serial Bus",
  "page": 1,
  "level": 1,
  "parent_id": null,
  "full_path": "Universal Serial Bus",
  "type": "paragraph",
  "block_id": "p1_0",
  "bbox": [171.33, 62.91, 423.95, 95.74]
}
```

## Search Functionality

### Content Search

```bash
# Search in extracted content
python search.py "Power Delivery" outputs/usb_pd_spec.jsonl
python search.py "voltage" outputs/usb_pd_spec.jsonl
```

## Configuration

### application.yml

```yaml
input:
  pdf_path: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"

output:
  base_dir: "outputs"

metadata:
  doc_title: "USB Power Delivery Specification v3.2"
  keywords:
    - power delivery
    - voltage
    - current
    - protocol
    - charging
```

## Advanced Usage

### Programmatic API

```python
from pathlib import Path
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.core.config.constants import ParserMode

# Initialize the parsing pipeline
file_path = Path("documents/usb_pd_specification.pdf")
orchestrator = PipelineOrchestrator(file_path, ParserMode.FULL)

# Execute parsing with error handling
try:
    result = orchestrator.execute()
    print(f"Successfully extracted:")
    print(f"   TOC entries: {len(result.toc_entries)}")
    print(f"   Content items: {len(result.content_items)}")
except FileNotFoundError:
    print("PDF file not found")
except ValueError as e:
    print(f"Configuration error: {e}")
```

### Custom Configuration

```python
from src.core.config.config_loader import ConfigLoader

# Custom configuration
config = ConfigLoader()
config.set_output_dir(Path("custom_output"))
config.set_doc_title("Custom Document Title")

orchestrator = PipelineOrchestrator(
    file_path, 
    ParserMode.FULL, 
    config=config
)
```

## Performance

### Processing Statistics

- **Pages**: 1,046/1,046 (100% coverage)
- **Content Items**: 25,760+ JSONL records
- **TOC Entries**: 369 entries
- **Content Coverage**: 75.2% of specification
- **Processing Time**: ~20-30 seconds
- **Memory Usage**: <500MB for large documents
- **Documentation**: 93.47% docstring coverage
- **Code Quality**: 99.79% PEP8 compliance

### Optimization Tips

1. **Memory**: Use default settings for optimal memory usage
2. **Speed**: All modes process full document efficiently
3. **Storage**: Ensure sufficient disk space for outputs

## Troubleshooting

### Common Issues

#### File Not Found
```bash
FileNotFoundError: PDF not found: assets/USB_PD_R3_2 V1.1 2024-10.pdf
```
**Solution**: Ensure PDF file exists in assets/ directory

#### Permission Error
```bash
PermissionError: Cannot write to outputs/
```
**Solution**: Check write permissions for outputs/ directory

#### Memory Error
```bash
MemoryError: Cannot allocate memory
```
**Solution**: Close other applications, use 64-bit Python

### Logging

Check `outputs/parser.log` for detailed execution information:

```
2024-10-17 02:29:58 [INFO] PipelineOrchestrator - Configuration loaded successfully
2024-10-17 02:29:58 [INFO] PipelineOrchestrator - Starting pipeline execution
2024-10-17 02:30:45 [INFO] PipelineOrchestrator - TOC extraction completed: 369 entries
2024-10-17 02:31:30 [INFO] PipelineOrchestrator - Content extraction completed: 25760 items
```

## Quality Assurance

### Code Quality Metrics

- **Syntax Errors**: 0 (target: 0) ✅
- **Code Smells**: 0.04% (target: <10%) ✅
- **Complexity**: 1.34 avg (A-rated) ✅
- **Maintainability**: 56.4 (A-rated) ✅
- **Naming**: 99.79% PEP8 (target: >90%) ✅

### Testing

```bash
# Run complete test suite
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html --cov-fail-under=90

# Run specific test categories
pytest tests/functional_tests/     # Core functionality
pytest tests/performance_tests/    # Performance benchmarks
pytest tests/oop_tests/           # Object-oriented design
```

## Examples

### View Results

```bash
# Windows - View first 3 lines of content
type outputs\usb_pd_spec.jsonl | findstr /n "." | findstr "^[1-3]:"

# Search for specific content
python search.py "USB Power Delivery"
```

### Validation

```bash
# Check output files (Windows)
dir outputs

# Check output files (Unix/Linux/macOS)
ls -lh outputs/

# Verify content count
python -c "with open('outputs/usb_pd_spec.jsonl') as f: print(f'Content items: {sum(1 for _ in f)}')"

# Run quality checks
python check_code_quality.py
python check_modularity.py
```

## Best Practices

### File Management

1. **Backup**: Keep original PDF safe
2. **Cleanup**: Remove old outputs before new runs
3. **Validation**: Check all 6 output files are generated

### Performance

1. **Resources**: Ensure adequate RAM (4GB+ recommended)
2. **Storage**: Reserve 100MB+ for outputs
3. **Processing**: Run during low system usage

### Integration

1. **Automation**: Use in CI/CD pipelines
2. **Monitoring**: Check parser.log for issues
3. **Validation**: Verify output file completeness