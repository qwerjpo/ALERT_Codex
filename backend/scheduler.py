"""Background refresh scheduler."""
from __future__ import annotations
import asyncio, logging
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from . import db
from .config import HTTP_HEADERS, HTTP_TIMEOUT, REFRESH_INTERVAL_SECONDS
from .sources import cve, gdelt, reliefweb, rss, usgs

log = logging.getLogger(__name__)

async def run_once():
    total_inserted = total_seen = 0
    async with httpx.AsyncClient(headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT) as client:
        for src, res in await rss.fetch_all(client):
            name = src["name"]
            if isinstance(res, Exception): db.update_source_status(name, "error", 0, str(res)[:200]); continue
            c = db.upsert_events(res); db.update_source_status(name, "ok", c); total_inserted += c; total_seen += len(res)
        try:
            for q, res in await gdelt.fetch_all(client):
                name = q["name"]
                if isinstance(res, Exception): db.update_source_status(name, "error", 0, str(res)[:200]); continue
                c = db.upsert_events(res); db.update_source_status(name, "ok", c); total_inserted += c; total_seen += len(res)
        except Exception as e: log.warning("GDELT failed: %s", e)
        for fetcher, name_attr in [(reliefweb, reliefweb.NAME), (usgs, usgs.NAME), (cve, cve.NAME)]:
            try:
                ev = await fetcher.fetch(client); c = db.upsert_events(ev); db.update_source_status(name_attr, "ok", c); total_inserted += c; total_seen += len(ev)
            except Exception as e: db.update_source_status(name_attr, "error", 0, str(e)[:200])
    return {"inserted": total_inserted, "fetched": total_seen}

_scheduler = None
_running_lock = asyncio.Lock()

async def _safe_run():
    if _running_lock.locked(): return
    async with _running_lock:
        try:
            s = await run_once(); log.info("Refresh complete: %s", s)
        except Exception as e: log.exception("Refresh failed: %s", e)

def start_scheduler():
    global _scheduler
    if _scheduler: return _scheduler
    sched = AsyncIOScheduler()
    sched.add_job(_safe_run, "interval", seconds=REFRESH_INTERVAL_SECONDS, next_run_time=None, id="refresh", coalesce=True, max_instances=1)
    sched.start(); _scheduler = sched; return sched

async def trigger_refresh(): return await run_once()
