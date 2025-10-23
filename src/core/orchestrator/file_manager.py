"""USB PD Specification Parser - File Management Module"""

from typing import Any

from src.config.config import Config
from src.config.constants import USB_PD_SPEC_FILE, USB_PD_TOC_FILE
from src.support.output_writer import JSONLWriter


class FileManager:  # Encapsulation + Interface Implementation
    """Manages all file I/O operations."""

    def __init__(self, config: Config, logger: Any):
        """Initialize file manager with dependencies."""
        if not config:
            raise ValueError("Config cannot be None")
        if not logger:
            raise ValueError("Logger cannot be None")

        self.__config = config  # Private
        self.__logger = logger  # Private
        self.__prepare_output_directory()

    def __prepare_output_directory(self) -> None:  # Private method
        """Prepare output directory for file operations."""
        try:
            output_dir = self.__config.output_directory
            output_dir.mkdir(parents=True, exist_ok=True)
            msg = f"Output directory prepared: {output_dir}"
            self.__logger.info(msg)
        except OSError as e:
            msg = f"Cannot create output directory: {e}"
            raise RuntimeError(msg) from e

    def __write_toc_file(
        self, toc: list[Any]
    ) -> None:  # Private - only used internally
        """Write TOC data to JSONL file."""
        if not toc:
            raise ValueError("TOC data cannot be empty")

        output_dir = self.__config.output_directory
        toc_path = output_dir / USB_PD_TOC_FILE
        toc_writer = JSONLWriter(toc_path)
        toc_writer.write(toc)
        self.__logger.info("TOC file written: %s", toc_path)

    def __write_spec_file(
        self, content: list[Any]
    ) -> None:  # Private - only used internally
        """Write specification content to JSONL file."""
        if not content:
            raise ValueError("Content data cannot be empty")

        output_dir = self.__config.output_directory
        spec_path = output_dir / USB_PD_SPEC_FILE
        spec_writer = JSONLWriter(spec_path)
        spec_writer.write(content)
        self.__logger.info("Spec file written: %s", spec_path)

    def write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write all JSONL output files."""
        self.__logger.info("Writing JSONL output files...")
        self.__write_toc_file(toc)
        self.__write_spec_file(content)
        self.__logger.info("JSONL files written successfully")
