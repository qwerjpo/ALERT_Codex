"""GDELT 2.0 DOC API - free, no key."""
from __future__ import annotations
import hashlib, logging
from datetime import datetime, timezone
import httpx
from .. import classifier
from ..config import GDELT_QUERIES, HTTP_HEADERS, HTTP_TIMEOUT

log = logging.getLogger(__name__)
GDELT_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

def _make_id(s, u): return hashlib.sha1(f"{s}::{u}".encode()).hexdigest()
def _parse_date(s):
    if not s: return None
    try:
        from datetime import datetime, timezone
        return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat()
    except: return None

async def fetch_query(qcfg, client):
    name = qcfg["name"]
    params = {"query": qcfg["query"], "mode": "ArtList", "format": "JSON", "maxrecords": qcfg.get("max_records",50), "sort": "DateDesc", "timespan": "1d"}
    resp = await client.get(GDELT_BASE, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    try: data = resp.json()
    except Exception as e: raise RuntimeError(f"GDELT non-JSON: {e}")
    arts = data.get("articles") or []; now_iso = datetime.now(timezone.utc).isoformat(); out = []
    country_map = {"united states":"americas","russia":"russia_cis","china":"asia","japan":"asia","ukraine":"europe","israel":"middle_east","iran":"middle_east"}
    for a in arts:
        url = a.get("url") or ""
        if not url: continue
        title = (a.get("title") or "").strip()
        info = classifier.enrich(title, "", None, qcfg.get("categories") or [], float(qcfg.get("weight",0.9)))
        country = (a.get("sourcecountry") or "").lower()
        if country: info["region"] = country_map.get(country, info["region"])
        out.append({"id": _make_id(name, url), "source": name, "title": title or "(no title)", "summary": "", "url": url, "published_at": _parse_date(a.get("seendate")), "fetched_at": now_iso, "region": info["region"], "categories": info["categories"], "importance": info["importance"], "raw_json": None})
    return out

async def fetch_all(client):
    results = []
    for q in GDELT_QUERIES:
        try: results.append((q, await fetch_query(q, client)))
        except Exception as e: results.append((q, e)); log.warning("GDELT failed: %s - %s", q.get("name"), e)
    return results
