from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path


ALLOWED_EXTENSIONS = {".csv", ".json"}
LOG_FILE = "backup_log.txt"
MAX_BACKUPS = 5


def log_message(backup_directory: Path, message: str) -> None:
    """Append a log entry to backup_log.txt."""
    log_path = backup_directory / LOG_FILE
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def make_backup_name(file_path: Path) -> str:
    """Return backup filename with timestamp suffix."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{file_path.stem}_{timestamp}{file_path.suffix}"


def copy_supported_files(source_directory: Path, backup_directory: Path) -> None:
    """Copy .csv and .json files from source to backup directory."""
    for item in source_directory.iterdir():
        if not item.is_file():
            continue
        if item.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        backup_name = make_backup_name(item)
        destination = backup_directory / backup_name
        shutil.copy2(item, destination)
        log_message(backup_directory, f"Copied {item.name} -> {destination.name}")


def rotate_backups(backup_directory: Path) -> None:
    """Keep only the latest 5 backups per original file."""
    grouped: dict[tuple[str, str], list[Path]] = {}

    for item in backup_directory.iterdir():
        if not item.is_file():
            continue
        if item.name == LOG_FILE:
            continue
        if item.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        stem_parts = item.stem.rsplit("_", 2)
        if len(stem_parts) < 3:
            continue

        original_stem = stem_parts[0]
        key = (original_stem, item.suffix.lower())
        grouped.setdefault(key, []).append(item)

    for (_, _), files in grouped.items():
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        old_files = files[MAX_BACKUPS:]

        for old_file in old_files:
            old_file.unlink()
            log_message(backup_directory, f"Deleted old backup {old_file.name}")


def main() -> None:
    """Run the backup manager with CLI arguments."""
    if len(sys.argv) != 3:
        print("Usage: python backup_manager.py <source_directory> <backup_directory>")
        return

    source_directory = Path(sys.argv[1])
    backup_directory = Path(sys.argv[2])

    if not source_directory.exists() or not source_directory.is_dir():
        print("Source directory does not exist or is not a directory.")
        return

    backup_directory.mkdir(parents=True, exist_ok=True)

    copy_supported_files(source_directory, backup_directory)
    rotate_backups(backup_directory)

    print("Backup completed.")


if __name__ == "__main__":
    main()