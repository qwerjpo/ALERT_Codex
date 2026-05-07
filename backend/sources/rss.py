"""Generic RSS/Atom feed collector."""
from __future__ import annotations
import hashlib, logging, re
from datetime import datetime, timezone
from typing import Any
import feedparser, httpx
from .. import classifier
from ..config import HTTP_HEADERS, HTTP_TIMEOUT, RSS_SOURCES

log = logging.getLogger(__name__)

def _make_id(source, url): return hashlib.sha1(f"{source}::{url}".encode()).hexdigest()
def _parse_entry_date(entry):
    for key in ("published_parsed","updated_parsed","created_parsed"):
        v = getattr(entry, key, None) or entry.get(key)
        if v:
            try: return datetime(*v[:6], tzinfo=timezone.utc).isoformat()
            except: pass
    return None
def _strip_html(text): return re.sub(r"<[^>]+>", " ", text or "").strip()

async def fetch_one(source, client):
    name = source["name"]; url = source["url"]
    region = source.get("region","global"); base_cats = source.get("categories") or []; weight = float(source.get("weight",1.0))
    try:
        resp = await client.get(url, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT, follow_redirects=True)
        resp.raise_for_status(); feed = feedparser.parse(resp.content)
    except Exception as e: log.warning("RSS fetch failed: %s - %s", name, e); raise
    now_iso = datetime.now(timezone.utc).isoformat(); events = []
    for entry in feed.entries[:80]:
        link = entry.get("link") or ""
        if not link: continue
        title = (entry.get("title") or "").strip()
        summary = _strip_html(entry.get("summary") or entry.get("description") or "")[:600]
        info = classifier.enrich(title, summary, region, base_cats, weight)
        events.append({"id": _make_id(name, link), "source": name, "title": title or "(no title)", "summary": summary, "url": link, "published_at": _parse_entry_date(entry), "fetched_at": now_iso, "region": info["region"], "categories": info["categories"], "importance": info["importance"], "raw_json": None})
    return events

async def fetch_all(client):
    results = []
    for src in RSS_SOURCES:
        try: results.append((src, await fetch_one(src, client)))
        except Exception as e: results.append((src, e))
    return results
