# Logging Guide
> This document explains the logging strategy used across the project for debugging,
> performance tracking, and reliability.
Records what your program is doing - successes, failures, timing, and locations.

## Log Levels

| Level | Use Case |
|-------|----------|
| DEBUG | Detailed developer info |
| INFO | Important milestones |
| WARNING | Unexpected but handled |
| ERROR | Something broke |
| CRITICAL | System failure |

## Basic Usage

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("Checking permissions")
logger.info("Starting extraction")
logger.warning("Page 5 is empty")
logger.error("Failed to parse PDF")
logger.critical("Out of memory")
```

## With Data

```python
logger.info(f"Processing page {page_num} of {total_pages}")
logger.error(f"Failed: {file_path} - {error_message}")
```

## Common Patterns

**Function Entry/Exit:**
```python
def extract_toc(pdf_path):
    logger = get_logger(__name__)
    logger.info(f"Starting: {pdf_path}")
    try:
        result = process_pdf(pdf_path)
        logger.info(f"Success: {len(result)} entries")
        return result
    except Exception as e:
        logger.error(f"Failed: {str(e)}")
        raise
```

**Progress Tracking:**
```python
for page_num in range(total_pages):
    if page_num % 100 == 0:
        logger.info(f"Processing page {page_num}/{total_pages}")
```

## Viewing Logs

**Console:**
```bash
python main.py
```

**Log File:**
```bash
cat outputs/parser.log
tail -20 outputs/parser.log
grep ERROR outputs/parser.log
grep -E "WARNING|ERROR" outputs/parser.log
```

## Configuration

**Default:**
```python
LOG_LEVEL = "INFO"
LOG_FILE = "outputs/parser.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
```

**Change Level:**
```python
logger.setLevel(logging.DEBUG)
```

Or via environment:
```bash
export LOG_LEVEL=DEBUG
python main.py
```

## Best Practices

**Good:**
```python
logger.info(f"Extracted {count} items from page {page_num}")
logger.error(f"Failed to parse {file_path}: {error_type}")
```

**Bad:**
```python
logger.info("Done")
logger.error("Error")
```

## Quick Reference

| Task | Command |
|------|---------|
| View all | `cat outputs/parser.log` |
| Last 20 lines | `tail -20 outputs/parser.log` |
| Find errors | `grep ERROR outputs/parser.log` |
| Count warnings | `grep -c WARNING outputs/parser.log` |
| Clear | `rm outputs/parser.log` |

## Example

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Application started")
logger.info("Processing: documents/usb_pd.pdf")
logger.info("Success: Extracted 25760 items")
logger.info("Successfully extracted 1431 tables")
logger.info("Extracted 362 figures metadata")
```

Output:
```
2024-01-15 14:32:45,123 | INFO | __main__ | Application started
2024-01-15 14:32:45,234 | INFO | __main__ | Processing: documents/usb_pd.pdf
2024-01-15 14:32:49,567 | INFO | __main__ | Success: Extracted 25760 items
2024-01-15 14:32:54,123 | INFO | __main__ | Successfully extracted 1431 tables
2024-01-15 14:32:54,456 | INFO | __main__ | Extracted 362 figures metadata
```

## Summary

- Logs record program activity
- Five levels for different urgency
- Output to console and file
- Easy to search and debug
- Use consistently throughout code
