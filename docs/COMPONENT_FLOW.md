# Component Flow

Data flows through: Input → Processing → Output

## Module 1: InputHandler (Parser)

**Purpose:** Validate and preprocess PDF documents

**Input:** PDF file from file system

**Processing:**
1. Validate file exists, size ≤ 100MB, valid PDF
2. Open with PyMuPDF
3. Load into memory

**Output:** `fitz.Document` object with metadata

**Errors:** FileNotFoundError, ValueError, PermissionError, MemoryError

---

## Module 2: DetectionEngine (Extractors)

**Purpose:** Extract structured content from PDF

**Input:** `fitz.Document` object

**Processing:**

**Path A - TOC Extraction:**
```python
raw_toc = doc.get_toc()  # Get native TOC
# Build hierarchy with parent-child relationships
# Extract section IDs (1.2.3)
# Generate full paths
```

**Path B - Content Extraction:**
```python
for page in document:
    for block in page.get_text("dict"):
        extract text
        normalize text
        validate text
        create ContentItem
```

**Path C - Table Extraction:**
```python
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        validate tables
        create TableData
```

**Path D - Figure Metadata Extraction:**
```python
for page in range(18, 30):  # List of Figures section
    text = page.get_text()
    matches = re.findall(pattern, text)
    create FigureMetadata
```

**Output:** `ParserResult` with:
- `toc_entries`: Hierarchical TOC
- `content_items`: Page content
- `tables`: Extracted tables
- `figures`: Figure metadata
- `page_count`: Total pages
- `extraction_time`: Duration

**Performance:**
- TOC: 0.8s
- Content: 3.1s
- Tables: 4.5s (1,431 tables)
- Figures: 0.3s (362 figures)
- Total: ~9s
- Speed: ~1,000 items/sec

**Errors:** ValueError, IndexError, AttributeError, MemoryError

---

## Module 3: OutputHandler (Writers)

**Purpose:** Format and write results to multiple formats

**Input:** `ParserResult` object

**Processing:**

**JSONL Writing:**
```python
for entry in toc_entries:
    write_json_line(entry)  # usb_pd_toc.jsonl

for item in content_items:
    write_json_line(item)   # usb_pd_spec.jsonl
```

**Excel Writing:**
```python
create_workbook()
add_toc_sheet(toc_entries)
add_content_sheet(content_items)
save_file()  # validation_report.xlsx
```

**Output Files:**
- `usb_pd_toc.jsonl` - Table of contents
- `usb_pd_spec.jsonl` - Full content
- `usb_pd_metadata.jsonl` - Document stats
- `parsing_report.json` - Processing report
- `validation_report.xlsx` - Excel dashboard
- `USB_PD_Spec_table.jsonl` - Extracted tables
- `extracted_figures.jsonl` - Figure metadata
- `figures_summary.json` - Figure summary

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
bbox: list              # Bounding box coordinates
```

**TableData:**
```python
page: int               # Page number
table_index: int        # Index on page
data: list[list]        # Table rows and columns
row_count: int          # Number of rows
column_count: int       # Number of columns
```

**FigureMetadata:**
```python
page: int               # Page number
figure_id: str          # "2.1", "5.3"
title: str              # Figure title
```

---

## Module 4: SearchHandler (Search)

**Purpose:** Search through extracted content

**Input:** Search keyword and file type

**Processing:**

**Search Configuration:**
```python
config = SearchConfig(keyword, file_type)
config.validate()  # Validate keyword and file type
file_path = config.file_path  # Map type to file
```

**Search Execution:**
```python
searcher = JSONLSearcher(file_path)
count = searcher.search(keyword)  # Search in JSONL
return count  # Number of matches
```

**Supported File Types:**
- `content` → usb_pd_spec.jsonl
- `tables` → extracted_tables.jsonl
- `figures` → extracted_figures.jsonl
- `toc` → usb_pd_toc.jsonl

**Output:** Match count and search results

**Performance:**
- Search speed: ~5,000 lines/sec
- Memory: <50MB

**Usage:**
```bash
python search.py "keyword"           # Search in content
python search.py voltage tables      # Search in tables
python search.py diagram figures     # Search in figures
```

**Errors:** SearchError, FileNotFoundError, ValueError

---

## Flow Summary

```
PDF File
    ↓
InputHandler (Validate & Load)
    ↓
DetectionEngine (Extract TOC, Content, Tables, Figures)
    ↓
OutputHandler (Write JSONL, JSON, Excel)
    ↓
Output Files
    ↓
SearchHandler (Search in extracted content)
    ↓
Search Results
```
