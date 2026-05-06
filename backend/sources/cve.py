"""
NIST NVD 最新 CVE を JSON API で取得 — 公開・キー不要 (rate limit ゆるめ)。
https://nvd.nist.gov/developers/vulnerabilities
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timedelta, timezone

import httpx

from ..config import HTTP_HEADERS, HTTP_TIMEOUT

log = logging.getLogger(__name__)

NAME = "NVD CVE"
ENDPOINT = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def _make_id(cve_id: str) -> str:
    return hashlib.sha1(f"{NAME}::{cve_id}".encode("utf-8")).hexdigest()


async def fetch(client: httpx.AsyncClient) -> list[dict]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=2)
    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": 50,
    }
    resp = await client.get(ENDPOINT, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("vulnerabilities") or []

    now_iso = datetime.now(timezone.utc).isoformat()
    out: list[dict] = []
    for it in items:
        cve = it.get("cve") or {}
        cve_id = cve.get("id") or ""
        if not cve_id:
            continue
        descs = cve.get("descriptions") or []
        desc = next((d.get("value", "") for d in descs if d.get("lang") == "en"), "")[:500]
        metrics = cve.get("metrics") or {}
        cvss_score = 0.0
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            arr = metrics.get(key) or []
            if arr:
                try:
                    cvss_score = float(arr[0].get("cvssData", {}).get("baseScore") or 0.0)
                except Exception:
                    pass
                break

        # CVSS が低いものはノイズなのでフィルタ
        if cvss_score < 7.0:
            continue

        url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        published = cve.get("published")

        out.append(
            {
                "id": _make_id(cve_id),
                "source": NAME,
                "title": f"{cve_id} — CVSS {cvss_score}",
                "summary": desc,
                "url": url,
                "published_at": published,
                "fetched_at": now_iso,
                "region": "global",
                "categories": ["cyber"],
                "importance": min(10.0, cvss_score),
                "raw_json": None,
            }
        )
    return out
