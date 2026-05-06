"""定期収集ジョブ — APScheduler + asyncio。"""

from __future__ import annotations

import asyncio
import logging

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from . import db
from .config import HTTP_HEADERS, HTTP_TIMEOUT, REFRESH_INTERVAL_SECONDS
from .sources import cve, gdelt, reliefweb, rss, usgs

log = logging.getLogger(__name__)


async def run_once() -> dict:
    """全ソースを 1 回フェッチして DB に書き込む。"""
    total_inserted = 0
    total_seen = 0

    async with httpx.AsyncClient(headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT) as client:
        # ── RSS (並列) ────────────────────────────────────
        rss_results = await rss.fetch_all(client)
        for src, res in rss_results:
            name = src["name"]
            if isinstance(res, Exception):
                db.update_source_status(name, "error", 0, str(res)[:200])
                continue
            count = db.upsert_events(res)
            db.update_source_status(name, "ok", count)
            total_inserted += count
            total_seen += len(res)

        # ── GDELT ────────────────────────────────────
        try:
            gdelt_results = await gdelt.fetch_all(client)
            for q, res in gdelt_results:
                name = q["name"]
                if isinstance(res, Exception):
                    db.update_source_status(name, "error", 0, str(res)[:200])
                    continue
                count = db.upsert_events(res)
                db.update_source_status(name, "ok", count)
                total_inserted += count
                total_seen += len(res)
        except Exception as e:  # noqa: BLE001
            log.warning("GDELT pipeline failed: %s", e)

        # ── ReliefWeb ────────────────────────────────────
        try:
            rw = await reliefweb.fetch(client)
            count = db.upsert_events(rw)
            db.update_source_status(reliefweb.NAME, "ok", count)
            total_inserted += count
            total_seen += len(rw)
        except Exception as e:  # noqa: BLE001
            db.update_source_status(reliefweb.NAME, "error", 0, str(e)[:200])

        # ── USGS ────────────────────────────────────
        try:
            ev = await usgs.fetch(client)
            count = db.upsert_events(ev)
            db.update_source_status(usgs.NAME, "ok", count)
            total_inserted += count
            total_seen += len(ev)
        except Exception as e:  # noqa: BLE001
            db.update_source_status(usgs.NAME, "error", 0, str(e)[:200])

        # ── NVD CVE ────────────────────────────────────
        try:
            ev = await cve.fetch(client)
            count = db.upsert_events(ev)
            db.update_source_status(cve.NAME, "ok", count)
            total_inserted += count
            total_seen += len(ev)
        except Exception as e:  # noqa: BLE001
            db.update_source_status(cve.NAME, "error", 0, str(e)[:200])

    return {"inserted": total_inserted, "fetched": total_seen}


_scheduler: AsyncIOScheduler | None = None
_running_lock = asyncio.Lock()


async def _safe_run() -> None:
    if _running_lock.locked():
        log.info("Refresh already in progress, skipping tick.")
        return
    async with _running_lock:
        try:
            stats = await run_once()
            log.info("Refresh complete: %s", stats)
        except Exception as e:  # noqa: BLE001
            log.exception("Refresh failed: %s", e)


def start_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler:
        return _scheduler
    sched = AsyncIOScheduler()
    sched.add_job(
        _safe_run,
        "interval",
        seconds=REFRESH_INTERVAL_SECONDS,
        next_run_time=None,
        id="refresh",
        coalesce=True,
        max_instances=1,
    )
    sched.start()
    _scheduler = sched
    return sched


async def trigger_refresh() -> dict:
    """API などから手動で 1 回だけ実行。"""
    return await run_once()
