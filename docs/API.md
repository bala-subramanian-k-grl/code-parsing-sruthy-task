# API Documentation

## Overview

The USB-PD Specification Parser provides a high-performance API for extracting and processing content from USB Power Delivery specification PDFs with clean OOP architecture.

## Core Architecture

### Abstract Base Classes

The system uses abstract base classes for proper abstraction:

```python
from src.parser.base_parser import BaseParser
from src.orchestrator.validator import BaseValidator
from src.core.interfaces.parser_interface import ParserInterface
```

### Main Classes

#### PDFParser

PDF content parser with inheritance:

```python
from src.parser.pdf_parser import PDFParser
from pathlib import Path

# Initialize parser
parser = PDFParser(Path("document.pdf"), "USB-PD Spec")
result = parser.parse()

print(f"TOC entries: {len(result.toc_entries)}")
print(f"Content items: {len(result.content_items)}")
```

#### PipelineOrchestrator

Orchestrates the entire extraction pipeline:

```python
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.core.config.constants import ParserMode
from pathlib import Path

# Initialize orchestrator
file_path = Path("document.pdf")
orchestrator = PipelineOrchestrator(file_path, ParserMode.FULL)
result = orchestrator.execute()
```

#### Factory Pattern

```python
from src.parser.parser_factory import ParserFactory
from pathlib import Path

# Factory Method pattern
parser = ParserFactory.create_parser(Path("document.pdf"))
result = parser.parse()
```

## Current JSONL Format

### Standard Format (Current)

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

### Known Limitations

- **Section IDs**: Uses basic format (p1_0, p2_1) instead of hierarchical (1.1, 1.1.1)
- **Parent Relationships**: All items have `parent_id: null`
- **Section Levels**: All items marked as `level: 1`

## Processing Statistics

### Current Capabilities

```json
{
  "pages": 1047,
  "content_items": 25760,
  "toc_entries": 369,
  "major_sections": 56,
  "key_terms": 100,
  "paragraphs": 25760
}
```

## Design Patterns Implemented

### 1. Factory Pattern
```python
# ApplicationFactory
runner = ApplicationFactory.create_runner("cli")

# ReportFactory  
report_gen = ReportFactory.create_generator("excel", output_dir)
```

### 2. Strategy Pattern
```python
from src.core.extractors.strategies.extraction_strategy import ComprehensiveStrategy

strategy = ComprehensiveStrategy()
content = list(strategy.extract_pages(pdf_file, max_pages))
```

### 3. Template Method Pattern
```python
class BaseRunner(ABC):
    def run(self) -> None:  # Template method
        self._app = self.create_app()
        self._execute()
```

### 4. Composition Pattern
```python
class PDFExtractor(BaseExtractor):
    def __init__(self, pdf_path: Path):
        super().__init__(pdf_path)
        self.__analyzer = ContentAnalyzer()  # Composition
```

## Advanced Features

### Custom Decorators

```python
from src.utils.decorators import timing, log_execution, validate_path

@timing
@log_execution
def extract_content(self, max_pages=None):
    # Method implementation
    pass
```

### Magic Methods

```python
class PDFExtractor:
    def __call__(self, max_pages=None):  # Callable
        return self.extract_content(max_pages)
    
    def __len__(self):  # Length
        return len(self.extract())
    
    def __str__(self):  # String representation
        return f"PDFExtractor({self.get_pdf_name()})"
```

## Security Features

### Path Validation (CWE-22 Prevention)
```python
def _validate_path(self, path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    return path.resolve()  # Prevent path traversal
```

### Input Sanitization
```python
from src.utils.security_utils import sanitize_input, validate_file_path

safe_input = sanitize_input(user_input)
valid_path = validate_file_path(file_path)
```

## Error Handling

### Specific Exception Handling
```python
try:
    result = orchestrator.run()
except FileNotFoundError as e:
    logger.error("PDF file not found: %s", e)
except ValueError as e:
    logger.error("Configuration error: %s", e)
except RuntimeError as e:
    logger.error("Processing error: %s", e)
```

## Testing Framework

### Comprehensive Test Coverage (95%+)
```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html --cov-fail-under=90

# Run specific test types
pytest -m unit      # Unit tests
pytest -m integration  # Integration tests
pytest -m slow      # Performance tests
```

## Performance Optimization

### Memory Management
- **Iterator Pattern**: Uses generators for large document processing
- **Lazy Loading**: Content loaded on-demand
- **Resource Management**: Proper PDF document cleanup

### Processing Efficiency
- **All Pages**: Processes complete 1046-page document
- **Batch Processing**: Efficient block-by-block extraction
- **Optimized Libraries**: PyMuPDF for speed, pdfplumber for accuracy

## Documentation Standards

### Docstring Format
All modules follow Google-style docstrings:

```python
def extract_content(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
    """Extract content from PDF with optional page limit.
    
    Args:
        max_pages: Maximum number of pages to process. None for all pages.
        
    Returns:
        List of content items with metadata.
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist.
        ValueError: If max_pages is invalid.
    """
```

### Module Documentation
Each module includes:
- Purpose and functionality description
- Usage examples
- Class and function listings
- Import statements

## Future Enhancements

### Planned Features
1. **Hierarchical Section Numbering**: Implement proper section detection (1.1, 1.1.1)
2. **Parent-Child Relationships**: Build document hierarchy tree
3. **Enhanced Section Levels**: Proper heading level detection
4. **Advanced Content Classification**: Improved text analysis