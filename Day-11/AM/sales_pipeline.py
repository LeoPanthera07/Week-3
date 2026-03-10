from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


INPUT_PATTERN = "data*.csv"
MERGED_OUTPUT = "merged_sales.csv"
SUMMARY_OUTPUT = "revenue_summary.json"


def read_sales_files(directory: str | Path = ".") -> tuple[list[Path], list[dict]]:
    """Read all matching CSV files and return file paths plus merged rows."""
    base_path = Path(directory)
    files = sorted(base_path.glob(INPUT_PATTERN))

    all_rows: list[dict] = []

    for file_path in files:
        with file_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_rows.append(
                    {
                        "date": row.get("date", "").strip(),
                        "product": row.get("product", "").strip(),
                        "qty": row.get("qty", "").strip(),
                        "price": row.get("price", "").strip(),
                    }
                )

    return files, all_rows


def remove_duplicates(rows: list[dict]) -> list[dict]:
    """Remove duplicate rows where all four fields match."""
    seen = set()
    unique_rows: list[dict] = []

    for row in rows:
        key = (
            row.get("date", ""),
            row.get("product", ""),
            row.get("qty", ""),
            row.get("price", ""),
        )
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    return unique_rows


def sort_rows_by_date(rows: list[dict]) -> list[dict]:
    """Sort rows by date string."""
    return sorted(rows, key=lambda row: row.get("date", ""))


def calculate_revenue(rows: list[dict]) -> dict[str, float]:
    """Compute total revenue per product."""
    revenue = defaultdict(float)

    for row in rows:
        product = row.get("product", "")
        try:
            qty = float(row.get("qty", 0))
            price = float(row.get("price", 0))
        except (TypeError, ValueError):
            continue

        revenue[product] += qty * price

    return {product: round(total, 2) for product, total in revenue.items()}


def write_merged_csv(rows: list[dict], output_file: str | Path = MERGED_OUTPUT) -> None:
    """Write unique rows to merged_sales.csv."""
    fieldnames = ["date", "product", "qty", "price"]

    with Path(output_file).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_revenue_summary(
    files_processed: int,
    rows: list[dict],
    revenue_by_product: dict[str, float],
    output_file: str | Path = SUMMARY_OUTPUT,
) -> None:
    """Write revenue summary JSON with metadata."""
    total_revenue = round(sum(revenue_by_product.values()), 2)

    summary = {
        "metadata": {
            "files_processed": files_processed,
            "total_rows": len(rows),
            "total_revenue": total_revenue,
            "generated_at": datetime.now().isoformat(),
        },
        "revenue_by_product": revenue_by_product,
    }

    with Path(output_file).open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def main() -> None:
    """Run the full CSV merge and reporting pipeline."""
    files, rows = read_sales_files()
    unique_rows = remove_duplicates(rows)
    sorted_rows = sort_rows_by_date(unique_rows)
    revenue_by_product = calculate_revenue(sorted_rows)

    write_merged_csv(sorted_rows)
    write_revenue_summary(len(files), sorted_rows, revenue_by_product)

    print(f"Files processed: {len(files)}")
    print(f"Unique rows written: {len(sorted_rows)}")
    print(f"Total revenue: {sum(revenue_by_product.values()):.2f}")


if __name__ == "__main__":
    main()