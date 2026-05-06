"""
ReliefWeb API コレクタ — UN OCHA 公開データ、キー不要。
https://reliefweb.int/help/api
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone

import httpx

from .. import classifier
from ..config import HTTP_HEADERS, HTTP_TIMEOUT, RELIEFWEB_LIMIT

log = logging.getLogger(__name__)

NAME = "ReliefWeb"
ENDPOINT = "https://api.reliefweb.int/v1/reports"


def _make_id(url: str) -> str:
    return hashlib.sha1(f"{NAME}::{url}".encode("utf-8")).hexdigest()


async def fetch(client: httpx.AsyncClient) -> list[dict]:
    payload = {
        "limit": RELIEFWEB_LIMIT,
        "sort": ["date.created:desc"],
        "fields": {
            "include": ["title", "url", "date", "country", "primary_country", "body-html"]
        },
        "filter": {
            "operator": "AND",
            "conditions": [
                {"field": "format.name", "value": ["News and Press Release", "Situation Report"]},
            ],
        },
    }
    resp = await client.post(
        ENDPOINT, json=payload, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT
    )
    resp.raise_for_status()
    data = resp.json()
    items = data.get("data") or []

    now_iso = datetime.now(timezone.utc).isoformat()
    out: list[dict] = []
    for it in items:
        f = it.get("fields") or {}
        url = f.get("url") or ""
        if not url:
            continue
        title = (f.get("title") or "").strip()
        body = (f.get("body-html") or "")[:500]
        # body の HTML を雑に除去
        import re
        body = re.sub(r"<[^>]+>", " ", body).strip()

        date_field = (f.get("date") or {}).get("created")
        country = ""
        pc = f.get("primary_country") or {}
        if isinstance(pc, dict):
            country = (pc.get("name") or "").lower()
        elif isinstance(pc, list) and pc:
            country = (pc[0].get("name") or "").lower()

        # 大雑把な country → region
        region = "global"
        if any(k in country for k in ["ukrain", "europe"]):
            region = "europe"
        elif any(k in country for k in ["syria", "iraq", "yemen", "lebanon", "iran", "israel", "palestin"]):
            region = "middle_east"
        elif any(k in country for k in ["sudan", "ethiopia", "somalia", "nigeria", "mali", "congo", "drc", "libya"]):
            region = "africa"
        elif any(k in country for k in ["myanmar", "afghan", "pakistan", "philippines", "bangladesh", "indonesia"]):
            region = "asia"
        elif any(k in country for k in ["venezuela", "haiti", "colombia", "honduras"]):
            region = "americas"

        info = classifier.enrich(title, body, region, ["disaster", "security"], 1.0)

        out.append(
            {
                "id": _make_id(url),
                "source": NAME,
                "title": title or "(no title)",
                "summary": body,
                "url": url,
                "published_at": date_field,
                "fetched_at": now_iso,
                "region": info["region"],
                "categories": info["categories"],
                "importance": info["importance"],
                "raw_json": None,
            }
        )
    return out
