# USB PD Specification Parser - Constants Module
"""Application constants."""

# Document constants
DEFAULT_DOC_TITLE = "USB Power Delivery Specification"

# File constants
DEFAULT_PDF_PATH = "assets/USB_PD_R3_2 V1.1 2024-10.pdf"
DEFAULT_OUTPUT_DIR = "outputs"

# Processing constants
DEFAULT_MAX_PAGES_EXTENDED = 600
DEFAULT_MAX_PAGES_STANDARD = 200
MIN_TEXT_LENGTH = 5
MAX_TOC_PAGES = 20

# Search constants
DEFAULT_SEARCH_FILE = "outputs/usb_pd_spec.jsonl"
LOG_FILE_NAME = "parser.log"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_TERM_LENGTH = 100
