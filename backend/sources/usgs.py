"""
USGS Earthquake feed — 完全無料・キー不要。
M4.5+ の直近 24 時間を取得。
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone

import httpx

from ..config import HTTP_HEADERS, HTTP_TIMEOUT, USGS_FEED_URL

log = logging.getLogger(__name__)

NAME = "USGS Earthquakes"


def _make_id(eid: str) -> str:
    return hashlib.sha1(f"{NAME}::{eid}".encode("utf-8")).hexdigest()


def _region_from_place(place: str) -> str:
    p = (place or "").lower()
    if any(k in p for k in ["japan", "korea", "china", "taiwan", "philippines", "indonesia", "papua"]):
        return "asia"
    if any(k in p for k in ["alaska", "california", "hawaii", "mexico", "puerto rico", "chile", "peru"]):
        return "americas"
    if any(k in p for k in ["turkey", "iran", "syria", "iraq"]):
        return "middle_east"
    if any(k in p for k in ["italy", "greece", "spain", "iceland", "portugal"]):
        return "europe"
    if any(k in p for k in ["africa", "morocco", "algeria"]):
        return "africa"
    return "global"


async def fetch(client: httpx.AsyncClient) -> list[dict]:
    resp = await client.get(USGS_FEED_URL, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    feats = data.get("features") or []

    now_iso = datetime.now(timezone.utc).isoformat()
    out: list[dict] = []
    for f in feats:
        props = f.get("properties") or {}
        eid = f.get("id") or props.get("code") or ""
        if not eid:
            continue
        mag = props.get("mag") or 0
        place = props.get("place") or ""
        url = props.get("url") or ""
        time_ms = props.get("time")
        coords = (f.get("geometry") or {}).get("coordinates") or []
        lat = float(coords[1]) if len(coords) >= 2 else None
        lon = float(coords[0]) if len(coords) >= 1 else None
        published = (
            datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc).isoformat()
            if time_ms else None
        )

        title = f"M{mag:.1f} earthquake — {place}"
        importance = min(10.0, max(0.0, (mag - 4.0) * 2.0))

        out.append(
            {
                "id": _make_id(str(eid)),
                "source": NAME,
                "title": title,
                "summary": f"Magnitude {mag} earthquake reported near {place}.",
                "url": url,
                "published_at": published,
                "fetched_at": now_iso,
                "region": _region_from_place(place),
                "categories": ["disaster"],
                "importance": importance,
                "raw_json": None,
                "lat": lat,
                "lon": lon,
            }
        )
    return out
