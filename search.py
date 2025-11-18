"""Search entry point - wrapper for search_cli.py."""

import subprocess
import sys

if __name__ == "__main__":
    # Redirect to search_cli.py to avoid module name conflicts
    subprocess.run([sys.executable, "search_cli.py"] + sys.argv[1:])