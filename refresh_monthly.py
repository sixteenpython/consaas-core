"""One-command monthly refresh for all Decision Studio Foundation assets."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from core.refresh import refresh_all


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--effective-date", type=date.fromisoformat, default=date.today())
    parser.add_argument(
        "--release-tag",
        help="Optional lowercase slug for a corrected or methodology release on the same date",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    for result in refresh_all(root, args.effective_date, args.release_tag):
        print(
            f"{result.product_id}: {result.status}; rows={result.row_count}; "
            f"sha256={result.content_sha256[:12]}"
        )


if __name__ == "__main__":
    main()
