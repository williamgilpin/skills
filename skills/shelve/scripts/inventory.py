#!/usr/bin/env python3
"""Inventory project files for a human-reviewed shelving plan."""

import argparse
import csv
import os
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "archive",
}


def inventory(root):
    """Yield regular files outside known generated and archive directories.

    Args:
        root (Path): Project root to inspect.

    Yields:
        tuple[str, int]: Relative path and file size in bytes.
    """
    for directory, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories
            if name not in EXCLUDED_DIRS
            and not (Path(directory) / name).is_symlink()
        )
        for name in sorted(files):
            path = Path(directory) / name
            if path.is_file() and not path.is_symlink():
                yield path.relative_to(root).as_posix(), path.stat().st_size


def main():
    """Write a CSV inventory and report project file counts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--large-mib", type=float, default=100)
    args = parser.parse_args()

    root = args.root.resolve()
    output = (root / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    total_bytes = 0
    count = 0
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["path", "bytes", "mib", "review_hint"])
        for path, size in inventory(root):
            writer.writerow([
                path, size, f"{size / 2**20:.2f}",
                "large-file-review" if size >= args.large_mib * 2**20 else "review",
            ])
            total_bytes += size
            count += 1

    print(f"Wrote {count} files ({total_bytes / 2**20:.1f} MiB) to {output}")
    print("Excluded directories:", ", ".join(sorted(EXCLUDED_DIRS)))


if __name__ == "__main__":
    main()
