"""Application constants."""

from enum import Enum
from pathlib import Path


class ParserMode(str, Enum):
    """Parser processing modes."""

    TOC = "toc"
    CONTENT = "content"
    FULL = "full"


# File paths
DEFAULT_PDF_PATH = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
DEFAULT_OUTPUT_DIR = Path("outputs")
