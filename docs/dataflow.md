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
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼──────────┐
│ 4a. TOC EXTRACT  │    │ 4b. CONTENT EXTRACT│
│                  │    │                    │
│ TOCExtractor:    │    │ ContentExtractor:  │
│ ├─ Read TOC      │    │ ├─ Iterate pages  │
│ ├─ Build tree    │    │ ├─ Extract blocks │
│ └─ Generate IDs  │    │ ├─ Normalize text │
│                  │    │ └─ Generate items │
│ Output:          │    │                    │
│ 25,760+ entries  │    │ Output:            │
│                  │    │ 25,760+ items     │
└───────┬──────────┘    └────────┬──────────┘
        │                        │
        └────────────┬───────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 5. WRITING (JSONLWriter)                                    │
│    ├─ usb_pd_toc.jsonl (TOC entries)                        │
│    └─ usb_pd_spec.jsonl (Content items)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 6. REPORT GENERATION                                        │
│    ├─ MetadataGenerator → usb_pd_metadata.jsonl             │
│    ├─ JSONReportGenerator → parsing_report.json             │
│    └─ ExcelReportGenerator → validation_report.xlsx         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 7. OUTPUT: Structured Data                                  │
│    ├─ JSONL files (streaming-friendly)                      │
│    ├─ JSON report (comprehensive)                           │
│    ├─ Excel dashboard (visual analysis)                     │
│    └─ Log file (execution trace)                            │
└─────────────────────────────────────────────────────────────┘
```