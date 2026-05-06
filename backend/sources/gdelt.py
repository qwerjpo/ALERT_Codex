"""
GDELT 2.0 DOC API コレクタ。

完全に無料・キー不要・登録不要。
https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from .. import classifier
from ..config import GDELT_QUERIES, HTTP_HEADERS, HTTP_TIMEOUT

log = logging.getLogger(__name__)

GDELT_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"


def _make_id(source: str, url: str) -> str:
    return hashlib.sha1(f"{source}::{url}".encode("utf-8")).hexdigest()


def _parse_date(s: str | None) -> str | None:
    if not s:
        return None
    # GDELT 返却例: "20251004T123000Z"
    try:
        dt = datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except Exception:
        return None


async def fetch_query(
    qcfg: dict, client: httpx.AsyncClient
) -> list[dict]:
    name = qcfg["name"]
    params = {
        "query": qcfg["query"],
        "mode": "ArtList",
        "format": "JSON",
        "maxrecords": qcfg.get("max_records", 50),
        "sort": "DateDesc",
        "timespan": "1d",  # 直近 24 時間
    }
    weight = float(qcfg.get("weight", 0.9))
    base_cats = qcfg.get("categories") or []

    resp = await client.get(GDELT_BASE, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()

    try:
        data = resp.json()
    except Exception as e:  # GDELT は時々 HTML を返す
        raise RuntimeError(f"GDELT non-JSON response: {e}")

    arts = data.get("articles") or []
    now_iso = datetime.now(timezone.utc).isoformat()
    out: list[dict] = []
    for a in arts:
        url = a.get("url") or ""
        if not url:
            continue
        title = (a.get("title") or "").strip()
        seendate = _parse_date(a.get("seendate"))
        domain = a.get("domain", "")
        country = (a.get("sourcecountry") or "").lower()

        info = classifier.enrich(title, "", None, base_cats, weight)
        # GDELT は country code 風の語を持つので region を弱く補正
        if country:
            country_map = {
                "united states": "americas",
                "russia": "russia_cis",
                "china": "asia",
                "japan": "asia",
                "ukraine": "europe",
                "israel": "middle_east",
                "iran": "middle_east",
            }
            info["region"] = country_map.get(country, info["region"])

        out.append(
            {
                "id": _make_id(name, url),
                "source": f"{name} [{domain}]" if domain else name,
                "title": title or "(no title)",
                "summary": "",
                "url": url,
                "published_at": seendate,
                "fetched_at": now_iso,
                "region": info["region"],
                "categories": info["categories"],
                "importance": info["importance"],
                "raw_json": None,
            }
        )
    return out


async def fetch_all(client: httpx.AsyncClient) -> list[tuple[dict, list[dict] | Exception]]:
    results: list[tuple[dict, list[dict] | Exception]] = []
    for q in GDELT_QUERIES:
        try:
            evs = await fetch_query(q, client)
            results.append((q, evs))
        except Exception as e:  # noqa: BLE001
            results.append((q, e))
            log.warning("GDELT fetch failed: %s — %s", q.get("name"), e)
    return results
