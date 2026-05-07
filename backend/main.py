"""World Monitor - FastAPI entry point."""
from __future__ import annotations
import asyncio, logging, os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from . import db, scheduler
from .config import CATEGORIES, FRONTEND_DIR, REFRESH_INTERVAL_SECONDS, REGIONS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("world_monitor")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    asyncio.create_task(scheduler._safe_run())
    scheduler.start_scheduler()
    log.info("Scheduler running (every %ss)", REFRESH_INTERVAL_SECONDS)
    yield
    log.info("Shutting down.")

app = FastAPI(title="World Monitor", version="0.1.0", lifespan=lifespan)

@app.get("/api/events")
async def api_events(region: str = Query("all"), category: str = Query("all"), q: str | None = Query(None), limit: int = Query(200, ge=1, le=1000), min_importance: float = Query(0.0, ge=0.0, le=10.0)):
    return {"events": db.query_events(region=region, category=category, q=q, limit=limit, min_importance=min_importance)}

@app.get("/api/stats")
async def api_stats(): return db.stats()

@app.get("/api/sources")
async def api_sources(): return {"sources": db.get_source_statuses()}

@app.get("/api/meta")
async def api_meta(): return {"regions": REGIONS, "categories": CATEGORIES, "refresh_interval_seconds": REFRESH_INTERVAL_SECONDS}

@app.post("/api/refresh")
async def api_refresh():
    try:
        s = await scheduler.trigger_refresh()
        return JSONResponse({"status": "ok", **s})
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def index(): return FileResponse(FRONTEND_DIR / "index.html")

def _run():
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    uvicorn.run("backend.main:app", host=host, port=port, reload=False, log_level="info")

if __name__ == "__main__":
    _run()
