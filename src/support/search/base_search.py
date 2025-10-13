
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseSearcher(ABC):  # Abstraction
    def __init__(self, file_path: str):
        self._file_path = self._validate_path(file_path)  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)  # Encapsulation
        self._logger.info(f"Initialized searcher for file: {self._file_path.name}")

    def _validate_path(self, file_path: str) -> Path:  # Encapsulation
        try:
            # Sanitize input to prevent path traversal
            clean_path = Path(str(file_path).replace("..", "").replace("~", ""))
            resolved_path = clean_path.resolve(strict=False)
            working_dir = Path.cwd().resolve()

            # Prevent path traversal attacks
            if not resolved_path.is_relative_to(working_dir):
                raise ValueError(f"Path traversal detected: {file_path}")

            # Additional security check for file extension
            if resolved_path.suffix not in [".jsonl", ".json"]:
                raise ValueError(f"Invalid file type: {file_path}")

            return resolved_path
        except (OSError, ValueError) as e:
            raise ValueError(f"Invalid file path: {file_path} - {e}") from e

    @abstractmethod  # Abstraction
    def search(self, term: str) -> list[dict[str, Any]]:
        pass
