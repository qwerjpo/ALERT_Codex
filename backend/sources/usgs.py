"""USGS Earthquake feed - free, no key. M4.5+ last 24h."""
from __future__ import annotations
import hashlib, logging
from datetime import datetime, timezone
import httpx
from ..config import HTTP_HEADERS, HTTP_TIMEOUT, USGS_FEED_URL

log = logging.getLogger(__name__)
NAME = "USGS Earthquakes"

def _make_id(eid): return hashlib.sha1(f"{NAME}::{eid}".encode()).hexdigest()
def _region_from_place(place):
    p = (place or "").lower()
    if any(k in p for k in ["japan","korea","china","taiwan","philippines","indonesia","papua"]): return "asia"
    if any(k in p for k in ["alaska","california","hawaii","mexico","puerto rico","chile","peru"]): return "americas"
    if any(k in p for k in ["turkey","iran","syria","iraq"]): return "middle_east"
    if any(k in p for k in ["italy","greece","spain","iceland","portugal"]): return "europe"
    if any(k in p for k in ["africa","morocco","algeria"]): return "africa"
    return "global"

async def fetch(client: httpx.AsyncClient):
    resp = await client.get(USGS_FEED_URL, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status(); feats = resp.json().get("features") or []
    now_iso = datetime.now(timezone.utc).isoformat(); out = []
    for f in feats:
        props = f.get("properties") or {}; eid = f.get("id") or props.get("code") or ""
        if not eid: continue
        mag = props.get("mag") or 0; place = props.get("place") or ""; url = props.get("url") or ""
        time_ms = props.get("time")
        published = datetime.fromtimestamp(time_ms/1000, tz=timezone.utc).isoformat() if time_ms else None
        out.append({"id": _make_id(str(eid)), "source": NAME, "title": f"M{mag:.1f} earthquake - {place}", "summary": f"Magnitude {mag} earthquake near {place}.", "url": url, "published_at": published, "fetched_at": now_iso, "region": _region_from_place(place), "categories": ["disaster"], "importance": min(10.0, max(0.0,(mag-4.0)*2.0)), "raw_json": None})
    return out
