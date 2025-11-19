"""Search CLI entry points."""

import os
import sys
from pathlib import Path

from src.search.jsonl_searcher import JSONLSearcher
from src.utils.logger import logger
from src.utils.timer import timer


@timer
def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        logger.error("Usage: python search.py <keyword> [file_path]")
        sys.exit(1)

    keyword = sys.argv[1]
    default_path = os.environ.get(
        "SEARCH_FILE_PATH", "outputs/usb_pd_spec.jsonl"
    )
    file_path = Path(sys.argv[2] if len(sys.argv) > 2 else default_path)

    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        sys.exit(1)

    logger.info(f"Searching for '{keyword}' in {file_path.name}")
    try:
        searcher = JSONLSearcher()
        count = searcher.search(keyword, file_path)
        logger.info(f"Found '{keyword}' {count} times in {file_path.name}")
    except (OSError, ValueError) as e:
        logger.error(f"Search failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
