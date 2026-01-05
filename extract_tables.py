#!/usr/bin/env python3
"""Convenience script to run table extraction."""

import subprocess
import sys
from pathlib import Path

def main():
    """Run table extraction CLI."""
    cli_script = Path("src/cli/run_table_extraction.py")
    
    if not cli_script.exists():
        print(f"Error: CLI script not found at {cli_script}")
        return 1
    
    try:
        result = subprocess.run([sys.executable, str(cli_script)], 
                              cwd=Path(__file__).parent,
                              check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Table extraction failed with exit code {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"Failed to run table extraction: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())