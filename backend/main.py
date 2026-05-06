"""
World Monitor — FastAPI エントリポイント。

`python -m backend.main` で起動するとブラウザで <http://127.0.0.1:8000> に
ダッシュボードが表示されます。
"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import db, scheduler
from .config import CATEGORIES, FRONTEND_DIR, REFRESH_INTERVAL_SECONDS, REGIONS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("world_monitor")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    log.info("DB ready at %s", db.DB_PATH if hasattr(db, "DB_PATH") else "(default)")

    # 起動時に 1 回バックグラウンドで取得
    asyncio.create_task(scheduler._safe_run())
    scheduler.start_scheduler()
    log.info("Scheduler running (every %ss)", REFRESH_INTERVAL_SECONDS)
    yield
    log.info("Shutting down.")


app = FastAPI(
    title="World Monitor",
    version="0.1.0",
    description="Personal OSINT dashboard — military / security / political signals.",
    lifespan=lifespan,
)


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #
@app.get("/api/events")
async def api_events(
    region: str = Query("all"),
    category: str = Query("all"),
    q: str | None = Query(None),
    limit: int = Query(200, ge=1, le=1000),
    min_importance: float = Query(0.0, ge=0.0, le=10.0),
):
    return {
        "events": db.query_events(
            region=region,
            category=category,
            q=q,
            limit=limit,
            min_importance=min_importance,
        )
    }


@app.get("/api/stats")
async def api_stats():
    return db.stats()


@app.get("/api/sources")
async def api_sources():
    return {"sources": db.get_source_statuses()}


@app.get("/api/meta")
async def api_meta():
    return {
        "regions": REGIONS,
        "categories": CATEGORIES,
        "refresh_interval_seconds": REFRESH_INTERVAL_SECONDS,
    }


@app.post("/api/refresh")
async def api_refresh():
    try:
        stats = await scheduler.trigger_refresh()
        return JSONResponse({"status": "ok", **stats})
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            {"status": "error", "error": str(e)}, status_code=500
        )


# --------------------------------------------------------------------------- #
# Static frontend
# --------------------------------------------------------------------------- #
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def index():
    return FileResponse(FRONTEND_DIR / "index.html")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _run() -> None:
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    _run()
