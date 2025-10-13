# API Documentation



The USB PD Specification Parser provides a comprehensive API for extracting content from PDF documents with professional OOP design, advanced Python features, and security hardening.

## Core Classes

### Abstract Base Classes

#### `BaseExtractor`
Abstract base class for all extractors implementing the Template Method pattern.

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

class BaseExtractor(ABC):
    def __init__(self, config: dict[str, Any]):
        self._config = config  # Encapsulation
    
    @abstractmethod
    def extract(self, file_path: Path) -> list[dict[str, Any]]:
        """Abstract extraction method."""
        pass
```

#### `BaseWriter`
Abstract base class for output writers with path validation.

```python
class BaseWriter(ABC):
    def __init__(self, output_path: Path):
        self._output_path = self._validate_path(output_path)
    
    @abstractmethod
    def write(self, data: Any) -> None:
        """Abstract write method."""
        pass
```

### Concrete Implementations

#### `PDFExtractor`
Main PDF content extraction class with magic methods and decorators.

```python
from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor

# Initialize extractor
extractor = PDFExtractor(Path("document.pdf"))

# Magic methods
print(extractor)  # PDFExtractor(document.pdf)
print(len(extractor))  # Number of extracted items
items = extractor(max_pages=200)  # Callable interface

# Decorated methods
@timing
@log_execution
def extract_content(self, max_pages=None):
    return list(self.extract_structured_content(max_pages))
```

#### `TOCExtractor`
Table of Contents extraction with Pydantic validation.

```python
from src.core.extractors.tocextractor.toc_extractor import TOCExtractor
from src.core.models import TOCEntry

extractor = TOCExtractor()
entries: list[TOCEntry] = extractor.extract_toc(pdf_path)

# TOCEntry with magic methods
entry = TOCEntry(
    doc_title="USB PD Spec",
    section_id="1.1",
    title="Introduction",
    page=1,
    level=1
)
print(entry)  # TOCEntry(1.1: Introduction)
print(hash(entry))  # Hash for set operations
```

## Decorators

### Custom Decorators

#### `@timing`
Measures and logs execution time.

```python
from src.utils.decorators import timing

@timing
def process_document(self):
    # Function implementation
    pass
# Logs: "process_document took 2.34 seconds"
```

#### `@log_execution`
Logs function entry, success, and errors.

```python
from src.utils.decorators import log_execution

@log_execution
def extract_content(self):
    # Function implementation
    pass
# Logs: "Executing extract_content"
# Logs: "Completed extract_content successfully"
```

#### `@validate_path`
Validates Path arguments before execution.

```python
from src.utils.decorators import validate_path

@validate_path
def process_file(self, file_path: Path):
    # Automatically validates file_path exists
    pass
```

#### `@retry`
Retries function on failure with configurable attempts.

```python
from src.utils.decorators import retry

@retry(max_attempts=3)
def unstable_operation(self):
    # Will retry up to 3 times on failure
    pass
```

## Data Models

### Pydantic Models with Validation

#### `TOCEntry`
Table of Contents entry with field validation and magic methods.

```python
from src.core.models import TOCEntry

class TOCEntry(BaseModel):
    doc_title: str = Field()
    section_id: str = Field()
    title: str = Field()
    page: int = Field(gt=0)
    level: int = Field(gt=0)
    parent_id: Optional[str] = Field(default=None)
    
    # Magic methods
    def __str__(self) -> str:
        return f"TOCEntry({self.section_id}: {self.title})"
    
    def __hash__(self) -> int:
        return hash((self.section_id, self.page))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TOCEntry):
            return False
        return self.section_id == other.section_id
    
    # Field validators
    @field_validator("section_id")
    @classmethod
    def validate_section_id(cls, v: str) -> str:
        if not re.match(r"^[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*$", v.strip()):
            raise ValueError(f"Invalid format: {v}")
        return v.strip()
```

#### `ContentItem`
Content item with inheritance from BaseContent.

```python
from src.core.models import ContentItem, BaseContent

class ContentItem(BaseContent):  # Inheritance
    doc_title: str = Field()
    content_id: str = Field()
    type: str = Field()
    block_id: str = Field()
    bbox: list[float] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
```

## Pipeline Orchestration

### `PipelineOrchestrator`
Main coordination class implementing the Facade pattern.

```python
from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

# Initialize with configuration
orchestrator = PipelineOrchestrator("application.yml")

# Run different processing modes
result = orchestrator.run_full_pipeline(mode=3)  # Standard mode
toc_result = orchestrator.run_toc_only()
content_result = orchestrator.run_content_only()

# Results structure
{
    "toc_entries": 369,
    "spec_counts": {
        "content_items": 4403,
        "pages_processed": 200
    },
    "processing_time": 8.45,
    "files_generated": [
        "outputs/usb_pd_toc.jsonl",
        "outputs/usb_pd_spec.jsonl",
        "outputs/parsing_report.json",
        "outputs/validation_report.xlsx"
    ]
}
```

## CLI Interface

### `CLIApp`
Command-line interface with inheritance and polymorphism.

```python
from src.interfaces.app import CLIApp

class CLIApp(BaseApp):  # Inheritance
    def run(self) -> None:  # Polymorphism
        args = self._parser.parse_args()
        self._execute_pipeline(args)

# Usage
app = CLIApp()
app.run()  # Polymorphic method call
```

## Security Features

### Path Validation
Prevents path traversal attacks (CWE-22).

```python
def _validate_path(self, path: Path) -> Path:
    safe_path = path.resolve()  # Prevent path traversal
    if not safe_path.is_relative_to(Path.cwd()):
        raise SecurityError("Path traversal detected")
    return safe_path
```

### Input Sanitization
Sanitizes user input to prevent injection attacks.

```python
from src.utils.security_utils import sanitize_input

def process_user_input(self, user_data: str) -> str:
    return sanitize_input(user_data)  # Removes dangerous characters
```

## Error Handling

### Specific Exception Handling
No broad exception catches, specific error types.

```python
try:
    result = self.extract_content()
except FileNotFoundError as e:
    self._logger.error(f"PDF file not found: {e}")
    raise
except PermissionError as e:
    self._logger.error(f"Permission denied: {e}")
    raise
except Exception as e:
    self._logger.error(f"Unexpected error: {e}")
    raise RuntimeError(f"Content extraction failed: {e}") from e
```

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

# Initialize and run
orchestrator = PipelineOrchestrator("application.yml")
result = orchestrator.run_full_pipeline(mode=3)

print(f"Processed {result['spec_counts']['content_items']} items")
print(f"Generated {len(result['files_generated'])} output files")
```

### Advanced Usage with Decorators

```python
from src.utils.decorators import timing, log_execution, retry

class CustomProcessor:
    @timing
    @log_execution
    @retry(max_attempts=3)
    def process_with_decorators(self, data):
        # Processing logic with automatic timing, logging, and retry
        return self._complex_processing(data)
```

### Magic Methods Usage

```python
# Create extractor with magic methods
extractor = PDFExtractor(Path("document.pdf"))

# Use as callable
items = extractor(max_pages=100)

# Get length
total_items = len(extractor)

# String representation
print(f"Using {extractor}")  # Uses __str__

# TOC entries with magic methods
entry1 = TOCEntry(section_id="1.1", title="Intro", page=1, level=1)
entry2 = TOCEntry(section_id="1.1", title="Intro", page=1, level=1)

# Equality and hashing
assert entry1 == entry2  # Uses __eq__
entry_set = {entry1, entry2}  # Uses __hash__
print(len(entry_set))  # 1 (deduplicated)
```

## Configuration

### YAML Configuration
Comprehensive configuration with OOP and security settings.

```yaml
# OOP Configuration
oop:
  use_abstract_classes: true
  enable_polymorphism: true
  encapsulation_level: "strict"
  magic_methods: true
  property_decorators: true

# Processing with decorators
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
  command_injection_protection: true
  cwe_compliance: true
```