from __future__ import annotations

import csv
import json
import logging
import traceback
import time
from collections import defaultdict
from pathlib import Path


logging.basicConfig(
    filename="file_processor_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

INPUT_PATTERN = "*.csv"
REPORT_FILE = "processing_report.json"


class FileProcessingError(Exception):
    """Raised when a CSV file cannot be processed correctly."""


def read_csv_with_retry(file_path: Path, max_attempts: int = 3) -> list[dict]:
    """Read a CSV file with retry logic for PermissionError only."""
    for attempt in range(1, max_attempts + 1):
        try:
            with file_path.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                if not reader.fieldnames:
                    raise FileProcessingError("Empty CSV file or missing header")

                expected = {"date", "product", "qty", "price"}
                if set(reader.fieldnames) != expected:
                    raise FileProcessingError(
                        f"Wrong format. Expected columns {expected}, got {reader.fieldnames}"
                    )

                rows = [row for row in reader]
                return rows

        except PermissionError:
            if attempt == max_attempts:
                raise
            time.sleep(1)


def process_file(file_path: Path) -> dict:
    """Process one CSV file and calculate basic aggregates."""
    rows = read_csv_with_retry(file_path)

    if not rows:
        raise FileProcessingError("CSV file has header but no data rows")

    total_qty = 0
    total_revenue = 0.0
    product_totals = defaultdict(float)

    for row in rows:
        try:
            qty = float(row["qty"])
            price = float(row["price"])
            product = row["product"]
        except (KeyError, TypeError, ValueError) as e:
            raise FileProcessingError(f"Invalid row data: {row}") from e

        total_qty += qty
        total_revenue += qty * price
        product_totals[product] += qty * price

    return {
        "file": file_path.name,
        "rows": len(rows),
        "total_qty": total_qty,
        "total_revenue": round(total_revenue, 2),
        "revenue_by_product": {
            product: round(value, 2) for product, value in product_totals.items()
        },
    }


def build_report(directory: str | Path = ".") -> dict:
    """Process all CSV files in a directory and build a JSON report."""
    base_path = Path(directory)
    files = sorted(base_path.glob(INPUT_PATTERN))

    processed = []
    failed = []
    error_details = {}

    for file_path in files:
        try:
            result = process_file(file_path)
        except (PermissionError, FileProcessingError, csv.Error, OSError) as e:
            failed.append(file_path.name)
            error_details[file_path.name] = {
                "error_type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
            logging.error("Failed processing %s\n%s", file_path.name, traceback.format_exc())
            continue
        else:
            processed.append(result)

    return {
        "files_processed": len(processed),
        "files_failed": len(failed),
        "processed_files": processed,
        "failed_files": failed,
        "error_details": error_details,
    }


def write_report(report: dict, output_file: str | Path = REPORT_FILE) -> None:
    """Write the processing report to JSON."""
    output_path = Path(output_file)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def main() -> None:
    """Run resilient file processing."""
    report = build_report()
    write_report(report)
    print("Processing completed.")
    print("Files processed:", report["files_processed"])
    print("Files failed:", report["files_failed"])


if __name__ == "__main__":
    main()