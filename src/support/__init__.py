"""
Support Module for Report & Metadata Generation
"""

from __future__ import annotations

from src.support.excel_report_generator import ExcelReportGenerator
from src.support.json_report_generator import JSONReportGenerator
from src.support.metadata_generator import MetadataGenerator

__version__ = "1.1.0"
__author__ = "USB PD Parser Framework"
__package_name__ = "support"
__description__ = "Helpers for metadata and report generation."

__all__ = [
    "ExcelReportGenerator",
    "JSONReportGenerator",
    "MetadataGenerator",
]
