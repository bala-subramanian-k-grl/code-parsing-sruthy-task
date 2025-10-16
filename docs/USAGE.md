# Usage Guide

## Quick Start

### Installation

```bash
git clone https://github.com/sruthypanigrahi/code-parsing.git
cd code-parsing
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run with interactive interface
python main.py

# Process entire document (1046 pages)
python main.py --config application.yml

# Extract only TOC
python main.py --toc-only

# Extract only content
python main.py --content-only
```

## Processing Modes

### Full Document Processing (Recommended)

```bash
python main.py
```

**Output:**
- Processes all 1046 pages
- Generates 6 output files
- Creates comprehensive reports

### Specialized Extraction

```bash
# TOC only
python main.py --toc-only

# Content only  
python main.py --content-only
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
python search.py "Power Delivery"
python search.py "USB" outputs/usb_pd_spec.jsonl
```

## Configuration

### application.yml

```yaml
pdf:
  input_file: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"

output:
  directory: "outputs"

processing:
  max_pages: 1046  # All pages
```

## Advanced Usage

### Programmatic API

```python
from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

# Initialize orchestrator
orchestrator = PipelineOrchestrator("application.yml")

# Run full pipeline
result = orchestrator.run()

# Access results
print(f"TOC entries: {result['toc_entries']}")
print(f"Content items: {result['spec_counts']['content_items']}")
```

### Custom Processing

```python
from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor

# Direct PDF extraction
extractor = PDFExtractor(pdf_path)
content = extractor.extract_content()

# Use magic methods
print(len(extractor))  # Number of items
print(str(extractor))  # String representation
```

## Performance

### Processing Statistics

- **Pages**: 1046/1046 (100% coverage)
- **Content Items**: 25,760+
- **Processing Time**: ~30-60 seconds
- **Memory Usage**: Optimized for large documents

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

## Known Limitations

### Current Issues

1. **Hierarchical Section Numbering**: Uses basic format (p1_0) instead of document structure (1.1, 1.1.1)
2. **Parent-Child Relationships**: All items have null parent_id
3. **Section Level Detection**: All items marked as level 1

### Workarounds

- **Section Analysis**: Use content text to identify section patterns
- **Hierarchy Building**: Post-process JSONL to build relationships
- **Level Detection**: Analyze font sizes and formatting

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
# Check output files
dir outputs\

# Verify content count
python -c "
import json
with open('outputs/usb_pd_spec.jsonl') as f:
    count = sum(1 for line in f)
print(f'Content items: {count}')
"
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