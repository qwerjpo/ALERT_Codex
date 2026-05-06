#!/usr/bin/env python3
"""
World Monitor — quick sanity check.

外部接続なしでも、モジュールのロードと分類器の動作を検証する。
実機での疎通確認は: `python -m backend.main` で起動 → /api/stats を確認。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend import classifier, config, db  # noqa: E402


def main() -> int:
    print(f"World Monitor sanity check\n{'=' * 40}")
    print(f"RSS sources    : {len(config.RSS_SOURCES)}")
    print(f"GDELT queries  : {len(config.GDELT_QUERIES)}")
    print(f"Regions        : {len(config.REGIONS)}")
    print(f"Categories     : {len(config.CATEGORIES)}")
    print(f"Keyword groups : {len(config.KEYWORDS)}")

    db.init_db()
    print(f"DB initialised : {config.DB_PATH}")
    print()
    print("Classifier samples:")

    samples = [
        ("Russia missile strike on Kyiv energy grid", "Drone and cruise missiles target power infrastructure overnight."),
        ("US imposes new sanctions on North Korea over nuclear test", ""),
        ("Critical zero-day in Cisco firewalls — CVE-2025-1111", "CISA warns of active exploitation."),
        ("EU foreign ministers convene emergency summit on Middle East", ""),
    ]
    for title, summary in samples:
        info = classifier.enrich(title, summary, None, [], 1.0)
        print(f"  [{info['importance']:>4.1f}] [{info['region']:>10}] {info['categories']}")
        print(f"         {title}")

    print("\nOK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
