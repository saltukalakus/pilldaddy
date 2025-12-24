#!/usr/bin/env python3
"""Compare line counts of privacy.html against all privacy-*.html files.

Usage:
    python3 check_privacy_line_counts.py
"""

from pathlib import Path


def count_lines(file_path: Path) -> int:
    try:
        with file_path.open('r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return -1


def main() -> None:
    root = Path(__file__).resolve().parent
    base_file = root / "privacy.html"
    base_count = count_lines(base_file)

    if base_count < 0:
        print(f"Base file not found: {base_file}")
        return

    print(f"Base: {base_file.name} -> {base_count} lines")

    mismatches = []
    for file_path in sorted(root.glob("privacy-*.html")):
        count = count_lines(file_path)
        status = "OK" if count == base_count else "MISMATCH"
        print(f"{file_path.name}: {count} lines [{status}]")
        if count != base_count:
            mismatches.append((file_path.name, count))

    if mismatches:
        print("\nFiles with mismatched line counts:")
        for name, count in mismatches:
            diff = count - base_count
            print(f"- {name}: {count} lines (diff {diff:+d})")
    else:
        print("\nAll privacy-*.html files match the base line count.")


if __name__ == "__main__":
    main()
