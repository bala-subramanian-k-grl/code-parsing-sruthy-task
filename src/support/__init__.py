"""Support module for report generation and metadata processing.

Provides:
- ExcelReportGenerator: Generate Excel validation reports
- JSONReportGenerator: Generate JSON summary reports
- MetadataGenerator: Generate metadata from parser results
"""

from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.support.metadata_generator import MetadataGenerator

__version__ = "1.0.0"
__all__ = [
    "ExcelReportGenerator",
    "JSONReportGenerator",
    "MetadataGenerator"
]
