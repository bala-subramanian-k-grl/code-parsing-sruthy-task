## 4. Data Flow
> This document illustrates how data flows through the system from PDF input
> to structured outputs and reports.

### Complete Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INPUT: PDF File                                          │
│    └─ USB_PD_R3_2 V1.1 2024-10.pdf (1,046 pages)           │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 2. VALIDATION                                               │
│    ├─ File exists?                                          │
│    ├─ Is PDF format?                                        │
│    └─ File size within limits?                              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 3. PARSING (ParserFactory → PDFParser)                      │
│    └─ Extract raw document structure                        │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬────────────┐
        │                         │            │
┌───────▼──────────┐    ┌────────▼──────────┐ │
│ 4a. TOC EXTRACT  │    │ 4b. CONTENT EXTRACT│ │
│                  │    │                    │ │
│ TOCExtractor:    │    │ ContentExtractor:  │ │
│ ├─ Read TOC      │    │ ├─ Iterate pages  │ │
│ ├─ Build tree    │    │ ├─ Extract blocks │ │
│ └─ Generate IDs  │    │ ├─ Normalize text │ │
│                  │    │ └─ Generate items │ │
│ Output:          │    │                    │ │
│ 25,760+ entries  │    │ Output:            │ │
│                  │    │ 25,760+ items     │ │
└───────┬──────────┘    └────────┬──────────┘ │
        │                        │            │
        │    ┌───────────────────▼────────────▼──────────┐
        │    │ 4c. TABLE EXTRACT                         │
        │    │                                           │
        │    │ TableExtractor (via pdfplumber):         │
        │    │ ├─ Extract tables from each page         │
        │    │ ├─ Validate table structure              │
        │    │ └─ Track row/column counts               │
        │    │                                           │
        │    │ Output: 1,431 tables                     │
        │    └───────────────────┬──────────────────────┘
        │                        │
        │    ┌───────────────────▼──────────────────────┐
        │    │ 4d. FIGURE METADATA EXTRACT              │
        │    │                                           │
        │    │ FigureMetadataExtractor:                 │
        │    │ ├─ Parse List of Figures (pages 18-30)  │
        │    │ ├─ Extract figure IDs and titles         │
        │    │ └─ Map to page numbers                   │
        │    │                                           │
        │    │ Output: 362 figures                      │
        │    └───────────────────┬──────────────────────┘
        │                        │
        └────────────┬───────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 5. WRITING                                                  │
│    ├─ JSONLWriter → usb_pd_toc.jsonl                        │
│    ├─ JSONLWriter → usb_pd_spec.jsonl                       │
│    ├─ TableWriter → USB_PD_Spec_table.jsonl                 │
│    └─ FigureWriter → extracted_figures.jsonl                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 6. REPORT GENERATION                                        │
│    ├─ MetadataGenerator → usb_pd_metadata.jsonl             │
│    ├─ JSONReportGenerator → parsing_report.json             │
│    ├─ ExcelReportGenerator → validation_report.xlsx         │
│    └─ FigureSummary → figures_summary.json                  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 7. OUTPUT: Structured Data                                  │
│    ├─ JSONL files (streaming-friendly)                      │
│    ├─ JSON reports (comprehensive)                          │
│    ├─ Excel dashboard (visual analysis)                     │
│    └─ Log file (execution trace)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 8. SEARCH: Query Extracted Data                             │
│                                                              │
│ SearchCLI:                                                   │
│ ├─ Parse arguments (keyword, file_type)                     │
│ └─ Create SearchConfig                                      │
│                                                              │
│ SearchConfig:                                                │
│ ├─ Validate keyword and file type                           │
│ ├─ Map file type to path:                                   │
│ │  ├─ content → usb_pd_spec.jsonl                           │
│ │  ├─ tables → extracted_tables.jsonl                       │
│ │  ├─ figures → extracted_figures.jsonl                     │
│ │  └─ toc → usb_pd_toc.jsonl                                │
│ └─ Return file path                                         │
│                                                              │
│ SearchExecutor:                                              │
│ ├─ Open JSONL file                                          │
│ ├─ Search line by line                                      │
│ ├─ Count matches                                            │
│ └─ Return result count                                      │
│                                                              │
│ Output: Search results with match count                     │
│                                                              │
│ Performance: ~5,000 lines/sec, <50MB memory                 │
└─────────────────────────────────────────────────────────────┘
```