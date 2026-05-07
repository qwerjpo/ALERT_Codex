"""SQLite ストレージ — 軽量・依存ゼロ。"""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterable, Iterator

from .config import DB_PATH


_LOCK = threading.Lock()


SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,             -- 安定 ID = sha1(source||url)
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    url TEXT NOT NULL,
    published_at TEXT,               -- ISO 8601 UTC
    fetched_at TEXT NOT NULL,
    region TEXT,
    categories TEXT,                 -- カンマ区切り
    importance REAL DEFAULT 0,
    raw_json TEXT,
    lat REAL,
    lon REAL
);

CREATE INDEX IF NOT EXISTS idx_events_published_at ON events(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_region ON events(region);
CREATE INDEX IF NOT EXISTS idx_events_importance ON events(importance DESC);

CREATE TABLE IF NOT EXISTS source_status (
    name TEXT PRIMARY KEY,
    last_fetched_at TEXT,
    last_status TEXT,
    last_error TEXT,
    item_count INTEGER DEFAULT 0
);
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


@contextmanager
def transaction() -> Iterator[sqlite3.Connection]:
    conn = _connect()
    try:
        with _LOCK:
            yield conn
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with transaction() as conn:
        conn.executescript(SCHEMA)
        for col_def in ("lat REAL", "lon REAL"):
            try:
                conn.execute(f"ALTER TABLE events ADD COLUMN {col_def}")
            except sqlite3.OperationalError:
                pass


def upsert_events(events: Iterable[dict[str, Any]]) -> int:
    """Insert events, ignoring duplicates by primary key. Returns insert count."""
    inserted = 0
    rows = list(events)
    if not rows:
        return 0
    with transaction() as conn:
        for ev in rows:
            try:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO events
                    (id, source, title, summary, url, published_at, fetched_at,
                     region, categories, importance, raw_json, lat, lon)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        ev["id"],
                        ev["source"],
                        ev["title"],
                        ev.get("summary", ""),
                        ev["url"],
                        ev.get("published_at"),
                        ev.get("fetched_at") or datetime.now(timezone.utc).isoformat(),
                        ev.get("region", "global"),
                        ",".join(ev.get("categories") or []),
                        float(ev.get("importance") or 0.0),
                        ev.get("raw_json"),
                        ev.get("lat"),
                        ev.get("lon"),
                    ),
                )
                if conn.total_changes:
                    inserted += conn.total_changes
            except sqlite3.Error:
                continue
    return inserted


def query_events(
    region: str | None = None,
    category: str | None = None,
    q: str | None = None,
    limit: int = 200,
    min_importance: float = 0.0,
) -> list[dict[str, Any]]:
    sql = "SELECT * FROM events WHERE 1=1"
    args: list[Any] = []
    if region and region != "all":
        sql += " AND region = ?"
        args.append(region)
    if category and category != "all":
        sql += " AND categories LIKE ?"
        args.append(f"%{category}%")
    if q:
        sql += " AND (title LIKE ? OR summary LIKE ?)"
        args.extend([f"%{q}%", f"%{q}%"])
    if min_importance > 0:
        sql += " AND importance >= ?"
        args.append(min_importance)
    sql += " ORDER BY COALESCE(published_at, fetched_at) DESC LIMIT ?"
    args.append(int(limit))

    with transaction() as conn:
        rows = conn.execute(sql, args).fetchall()
    return [
        {
            **dict(r),
            "categories": [c for c in (r["categories"] or "").split(",") if c],
        }
        for r in rows
    ]


def stats() -> dict[str, Any]:
    with transaction() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"]
        by_region = {
            r["region"] or "unknown": r["n"]
            for r in conn.execute(
                "SELECT region, COUNT(*) AS n FROM events GROUP BY region"
            ).fetchall()
        }
        # categories はカンマ区切りなので Python 側で展開
        rows = conn.execute("SELECT categories FROM events").fetchall()
    by_cat: dict[str, int] = {}
    for r in rows:
        for c in (r["categories"] or "").split(","):
            if c:
                by_cat[c] = by_cat.get(c, 0) + 1
    return {"total": total, "by_region": by_region, "by_category": by_cat}


def update_source_status(
    name: str, status: str, item_count: int = 0, error: str | None = None
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO source_status (name, last_fetched_at, last_status, last_error, item_count)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                last_fetched_at=excluded.last_fetched_at,
                last_status=excluded.last_status,
                last_error=excluded.last_error,
                item_count=excluded.item_count
            """,
            (name, now, status, error, item_count),
        )


def get_source_statuses() -> list[dict[str, Any]]:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT * FROM source_status ORDER BY name"
        ).fetchall()
    return [dict(r) for r in rows]
