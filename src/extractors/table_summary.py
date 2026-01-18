#!/usr/bin/env python3
"""
Table Summary Generator for USB PD Specification
Creates a summary of table structure analysis from extracted tables.
"""

import json
from pathlib import Path
from typing import Any

from src.utils.logger import logger


def analyze_tables() -> None:
    """Analyze extracted tables and create summary."""
    tables_file = Path("d:/code parsing/outputs/extracted_tables.jsonl")

    if not tables_file.exists():
        logger.error("extracted_tables.jsonl not found")
        return

    tables: list[dict[str, Any]] = []
    with open(tables_file, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                tables.append(json.loads(line))

    summary_data: list[dict[str, int | str]] = []

    for i, table in enumerate(tables, 1):
        row_count: int = table.get('row_count', 0)
        column_count: int = table.get('column_count', 0)
        expected_cells: int = row_count * column_count

        data: list[list[Any]] = table.get('data', [])
        actual_cells = 0
        for row in data:
            actual_cells += len([
                cell for cell in row
                if cell is not None and cell != ""
            ])

        summary_data.append({
            'table_no': i,
            'page': table.get('page', 'Unknown'),
            'table_index': table.get('table_index', 0),
            'rows': row_count,
            'columns': column_count,
            'expected_cells': expected_cells,
            'actual_cells': actual_cells
        })

    _write_summary_file(summary_data)
    logger.info(f"Analyzed {len(summary_data)} tables")


def _write_summary_file(summary_data: list[dict[str, int | str]]) -> None:
    """Write summary data to file."""
    output_file = Path("d:/code parsing/outputs/table_summary.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USB PD Specification - Table Structure Summary\n")
        f.write("=" * 50 + "\n\n")

        header = (
            f"{'Table No.':<10} {'Page':<6} {'Rows':<6} "
            f"{'Columns':<8} {'Expected Cells':<15} {'Actual Cells':<15}\n"
        )
        f.write(header)
        f.write("-" * 70 + "\n")

        for table in summary_data:
            row = (
                f"{table['table_no']:<10} {table['page']:<6} "
                f"{table['rows']:<6} {table['columns']:<8} "
                f"{table['expected_cells']:<15} "
                f"{table['actual_cells']:<15}\n"
            )
            f.write(row)

        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Total Tables: {len(summary_data)}\n")

        total_expected = sum(int(t['expected_cells']) for t in summary_data)
        total_actual = sum(int(t['actual_cells']) for t in summary_data)

        f.write(f"Total Expected Cells: {total_expected}\n")
        f.write(f"Total Actual Cells: {total_actual}\n")

        efficiency = (
            (total_actual / total_expected * 100)
            if total_expected > 0 else 0
        )
        f.write(f"Extraction Efficiency: {efficiency:.1f}%\n")

    logger.info(f"Table summary created: {output_file}")


if __name__ == "__main__":
    analyze_tables()
