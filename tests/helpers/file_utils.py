"""File utilities for testing."""

import os
import tempfile
from pathlib import Path
from typing import Any


class TempFileManager:
    """Manage temporary test files."""

    def __init__(self) -> None:
        """Initialize manager."""
        self.__files: list[Path] = []

    def create_temp_file(
        self, content: str = "", suffix: str = ".txt", encoding: str = "utf-8"
    ) -> Path:
        """Create temporary file."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        temp_path = Path(path)
        if content:
            temp_path.write_text(content, encoding=encoding)
        self.__files.append(temp_path)
        return temp_path

    def cleanup(self) -> None:
        """Delete all temporary files."""
        for f in self.__files:
            if f.exists():
                try:
                    f.unlink()
                except OSError:
                    pass
        self.__files.clear()

    def __enter__(self) -> "TempFileManager":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.cleanup()
