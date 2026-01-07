#!/usr/bin/env python3
"""Lightweight wrapper for table and figure extraction pipeline."""

import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path


class BaseRunner(ABC):
    """Abstract base for command runners."""

    def __init__(self, script_path: Path) -> None:
        self._script_path = script_path

    @abstractmethod
    def execute(self) -> int:
        """Execute the runner."""

    def _validate_script(self) -> bool:
        """Validate script exists."""
        return self._script_path.exists()


class ExtractionRunner(BaseRunner):
    """Run extraction pipeline script."""

    def execute(self) -> int:
        """Execute extraction pipeline."""
        if not self._validate_script():
            print(f"Error: Module not found at {self._script_path}")
            return 1

        try:
            result = subprocess.run(
                [sys.executable, str(self._script_path)],
                cwd=self._script_path.parent.parent.parent,
                check=True
            )
            return result.returncode
        except subprocess.CalledProcessError as e:
            print(f"Extraction failed: exit code {e.returncode}")
            return e.returncode
        except Exception as e:
            print(f"Error: {e}")
            return 1


def main() -> int:
    """Entry point."""
    script = Path(__file__).parent / "src" / "cli" / "run_extraction.py"
    runner = ExtractionRunner(script)
    return runner.execute()


if __name__ == "__main__":
    sys.exit(main())
