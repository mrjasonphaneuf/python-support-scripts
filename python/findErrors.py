#!/usr/bin/env python3
"""
System Utility: Search for various error strings in log files within a given 
                directory.
Author:         Jason Phaneuf
Created:        July 2026
GitHub:         ://github.com/mrjasonphaneuf/support-tools/python/findErrors.py

Description:
    This script will scan a directory for log files and search for occurrences 
    of various error strings as defined in errors.cfg (in the log files that
    were found).

Usage:
    python findErrors.py /path/to/logs
""" 

import argparse
import os
import sys
from pathlib import Path


def normalize_extension(file_type: str) -> str:
    """Ensure the supplied extension starts with a dot."""
    if not file_type:
        return ".json"
    return file_type if file_type.startswith(".") else f".{file_type}"


def count_write_failures(log_directory: str, file_type: str) -> list[tuple[Path, int]]:
    """Search files in the directory tree and count 'write failure' lines."""
    root = Path(log_directory)
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {log_directory}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {log_directory}")

    extension = normalize_extension(file_type)
    matches: list[tuple[Path, int]] = []

    # Walk the directory tree to find matching files.
    for current_root, _, files in os.walk(root):
        for filename in files:
            file_path = Path(current_root) / filename

            # Skip files that do not match the requested extension.
            if file_path.suffix.lower() != extension.lower():
                continue

            try:
                with file_path.open("r", encoding="utf-8", errors="replace") as handle:
                    count = sum(1 for line in handle if "write failure" in line.lower())
            except OSError as exc:
                print(f"Could not read {file_path}: {exc}", file=sys.stderr)
                continue

            if count > 0:
                matches.append((file_path, count))

    return matches


def main() -> int:
    """Parse command-line arguments and print the results."""
    parser = argparse.ArgumentParser(description="Find 'write failure' lines in log files")
    parser.add_argument("log_directory", help="Directory to scan for log files")
    parser.add_argument(
        "file_type",
        nargs="?",
        default=".json",
        help="File extension to scan (default: .json)",
    )
    args = parser.parse_args()

    try:
        matches = count_write_failures(args.log_directory, args.file_type)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

# Load target errors from errors.txt into a list
    with open("errors.cfg", "r") as f:
        target_errors = [line.strip().lower() for line in f if line.strip()]       
    # Initialize a dictionary tracking counter initialized to 0 for each error type
    # This acts like building a bucket for each item in errors.txt   

    error_breakdown = {}
    for error in target_errors:
        error_breakdown[error] = 0

    # Loop through file matches
    for file_path, _ in matches:
        with open(file_path, "r", encoding="utf-8", errors="replace") as handle:
            log_content = handle.read().lower()

            # Count occurrence of each target error inside the file text
            for error in target_errors:
                occurrences = log_content.count(error)
                error_breakdown[error] += occurrences

    # Print the exact breakdown of each error type and its count
    for error, count in error_breakdown.items():
        print(f"{error}: {count}")  

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
