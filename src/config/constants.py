# USB PD Specification Parser - Constants Module
"""Application constants."""


DEFAULT_DOC_TITLE = "USB Power Delivery Specification"

# File constants
DEFAULT_PDF_PATH = "assets/USB_PD_R3_2 V1.1 2024-10.pdf"
DEFAULT_OUTPUT_DIR = "outputs"

# Processing constants - Dynamic detection with fallbacks
DEFAULT_MAX_PAGES_FALLBACK = 1000  # Fallback if detection fails
USB_PD_TOTAL_PAGES = 1046  # Specific to USB PD spec
MIN_TEXT_LENGTH = 5
MAX_TOC_PAGES = 20
PROCESS_ALL_PAGES = -1  # Flag to process entire PDF

# Search constants
DEFAULT_SEARCH_FILE = "outputs/usb_pd_spec.jsonl"
LOG_FILE_NAME = "parser.log"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_TERM_LENGTH = 100

# Magic number constants for better encapsulation
MIN_ARGS_COUNT = 2
MIN_LINE_LENGTH = 10
MAX_TITLE_LENGTH = 50
MIN_TOC_GROUPS = 2
MAX_TOC_GROUPS = 3
MAX_PAGE_NUMBER = 2000
MIN_TITLE_LENGTH = 3
CONTENT_PREVIEW_LENGTH = 100
MIN_CONTENT_THRESHOLD = 1000

# File name constants
USB_PD_TOC_FILE = "usb_pd_toc.jsonl"
USB_PD_SPEC_FILE = "usb_pd_spec.jsonl"
