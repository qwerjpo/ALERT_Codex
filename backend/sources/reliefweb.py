"""ReliefWeb API - UN OCHA open data, no key."""
from __future__ import annotations
import hashlib, logging, re
from datetime import datetime, timezone
import httpx
from .. import classifier
from ..config import HTTP_HEADERS, HTTP_TIMEOUT, RELIEFWEB_LIMIT

log = logging.getLogger(__name__)
NAME = "ReliefWeb"
ENDPOINT = "https://api.reliefweb.int/v1/reports"

def _make_id(url): return hashlib.sha1(f"{NAME}::{url}".encode()).hexdigest()

async def fetch(client: httpx.AsyncClient):
    payload = {"limit": RELIEFWEB_LIMIT, "sort": ["date.created:desc"], "fields": {"include": ["title","url","date","primary_country","body-html"]}, "filter": {"operator": "AND", "conditions": [{"field": "format.name", "value": ["News and Press Release","Situation Report"]}]}}
    resp = await client.post(ENDPOINT, json=payload, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    items = resp.json().get("data") or []
    now_iso = datetime.now(timezone.utc).isoformat(); out = []
    for it in items:
        f = it.get("fields") or {}; url = f.get("url") or ""
        if not url: continue
        title = (f.get("title") or "").strip()
        body = re.sub(r"<[^>]+>", " ", (f.get("body-html") or "")[:500]).strip()
        pc = f.get("primary_country") or {}; country = (pc.get("name") or "").lower() if isinstance(pc, dict) else ""
        region = "global"
        if any(k in country for k in ["ukrain","europe"]): region = "europe"
        elif any(k in country for k in ["syria","iraq","yemen","lebanon","iran","israel","palestin"]): region = "middle_east"
        elif any(k in country for k in ["sudan","ethiopia","somalia","nigeria","mali","congo","drc","libya"]): region = "africa"
        elif any(k in country for k in ["myanmar","afghan","pakistan","philippines","bangladesh","indonesia"]): region = "asia"
        elif any(k in country for k in ["venezuela","haiti","colombia","honduras"]): region = "americas"
        info = classifier.enrich(title, body, region, ["disaster","security"], 1.0)
        out.append({"id": _make_id(url), "source": NAME, "title": title or "(no title)", "summary": body, "url": url, "published_at": (f.get("date") or {}).get("created"), "fetched_at": now_iso, "region": info["region"], "categories": info["categories"], "importance": info["importance"], "raw_json": None})
    return out
