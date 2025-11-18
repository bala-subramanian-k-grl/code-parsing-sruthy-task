"""Project grading utility using Gemini AI for code analysis."""

import json
import os
from pathlib import Path
from typing import Any

try:
    from google import genai  # type: ignore
except ImportError:
    genai = None  # type: ignore

MODEL = "gemini-2.5-flash-lite"
PER_FILE_LIMIT = 2000
EXTS = {".py", ".json", ".jsonl", ".md", ".txt", ".yaml", ".yml"}

RUBRIC = """
Your full rubric here...
"""

def extract_text(resp: Any) -> str:
    """Extract text safely using new SDK."""
    parts: list[str] = []
    for c in resp.candidates:
        for p in c.content.parts:
            if hasattr(p, "text"):
                parts.append(p.text)
    return "\n".join(parts).strip()

def collect_files(root: Path) -> list[Path]:
    files = []
    for folder in ["src", "tests", "docs"]:
        p = root / folder
        if p.exists():
            for f in p.rglob("*"):
                if f.suffix.lower() in EXTS:
                    files.append(f)
    for f in root.iterdir():
        if f.suffix.lower() in EXTS:
            files.append(f)
    return list(dict.fromkeys(files))

def analyze_file(client: Any, f: Path) -> str:
    try:
        text = f.read_text(errors="ignore")[:PER_FILE_LIMIT]
    except:
        text = ""
    resp = client.models.generate_content(
        model=MODEL,
        contents=[
            {"role": "user", "parts": [{"text":
                f"Analyze issues, OOP, quality:\n=== FILE "
                f"{f.name} ===\n{text}"
            }]}
        ],
        config={"temperature": 0.1}
    )
    return extract_text(resp)

def final_grade(client: Any, combined: str) -> dict[str, Any]:
    resp = client.models.generate_content(
        model=MODEL,
        contents=[
            {"role": "user", "parts": [{"text": RUBRIC}]},
            {"role": "user", "parts": [{"text": combined}]}
        ],
        config={"temperature": 0.1}
    )
    raw = extract_text(resp)

    print("\n=== RAW RESPONSE ===")
    print(raw[:500])  # Print first 500 chars
    print("\n")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print("Full response:")
        print(raw)
        raise

def grade_project(project_path: str) -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    if genai is None:
        raise RuntimeError(
            "google-genai package not installed. "
            "Install with: pip install google-genai"
        )

    client = genai.Client(api_key=api_key)

    root = Path(project_path)
    files = collect_files(root)
    print(f"Collected {len(files)} files")

    summaries = []
    for i, f in enumerate(files, 1):
        print(f"Analyzing {i}/{len(files)}:", f.name)
        summaries.append(analyze_file(client, f))

    combined = "\n".join(summaries)

    print("\nRunning final grading pass...")
    try:
        result = final_grade(client, combined)

        out = root / "gemini_grade_report.json"
        out.write_text(json.dumps(result, indent=2))

        print("\nSaved:", out)
        print("\n=== OVERALL SCORE ===")
        if "overall" in result:
            print(json.dumps(result["overall"], indent=2))
    except Exception as e:
        print(f"\nError during grading: {e}")
        # Save the combined summary for debugging
        debug_file = root / "debug_combined_summary.txt"
        debug_file.write_text(combined)
        print(f"Saved combined summary to: {debug_file}")
        raise


if __name__ == "__main__":
    import sys
    grade_project(sys.argv[1])
