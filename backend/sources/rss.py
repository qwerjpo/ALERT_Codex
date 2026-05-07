"""汎用 RSS / Atom コレクタ。"""

from __future__ import annotations

import asyncio
import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx

from .. import classifier
from ..config import HTTP_HEADERS, HTTP_TIMEOUT, RSS_SOURCES

log = logging.getLogger(__name__)


def _make_id(source: str, url: str) -> str:
    h = hashlib.sha1(f"{source}::{url}".encode("utf-8")).hexdigest()
    return h


def _parse_entry_date(entry: Any) -> str | None:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        v = getattr(entry, key, None) or entry.get(key)
        if v:
            try:
                return datetime(*v[:6], tzinfo=timezone.utc).isoformat()
            except Exception:
                pass
    return None


def _strip_html(text: str | None) -> str:
    if not text:
        return ""
    # 軽量にタグを除去 (lxml/bs4 を使うと安全だが速度優先)
    import re
    return re.sub(r"<[^>]+>", " ", text).strip()


async def fetch_one(source: dict, client: httpx.AsyncClient) -> list[dict]:
    """1 ソースをフェッチして正規化済みイベント list を返す。"""
    name = source["name"]
    url = source["url"]
    region = source.get("region", "global")
    base_cats = source.get("categories") or []
    weight = float(source.get("weight", 1.0))

    try:
        resp = await client.get(url, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except Exception as e:
        log.warning("RSS fetch failed: %s — %s", name, e)
        raise

    now_iso = datetime.now(timezone.utc).isoformat()
    events: list[dict] = []
    for entry in feed.entries[:80]:
        link = entry.get("link") or ""
        if not link:
            continue
        title = (entry.get("title") or "").strip()
        summary = _strip_html(entry.get("summary") or entry.get("description") or "")[:600]
        published = _parse_entry_date(entry)

        info = classifier.enrich(title, summary, region, base_cats, weight)

        events.append(
            {
                "id": _make_id(name, link),
                "source": name,
                "title": title or "(no title)",
                "summary": summary,
                "url": link,
                "published_at": published,
                "fetched_at": now_iso,
                "region": info["region"],
                "categories": info["categories"],
                "importance": info["importance"],
                "raw_json": None,
            }
        )

    return events


async def fetch_all(client: httpx.AsyncClient) -> list[tuple[dict, list[dict] | Exception]]:
    """設定済み RSS を並列フェッチ (同時最大20接続)。例外もタプルで返す。"""
    sem = asyncio.Semaphore(20)

    async def _fetch_guarded(src: dict) -> tuple[dict, list[dict] | Exception]:
        async with sem:
            try:
                return (src, await fetch_one(src, client))
            except Exception as e:  # noqa: BLE001
                return (src, e)

    return list(await asyncio.gather(*[_fetch_guarded(s) for s in RSS_SOURCES]))
