"""NIST NVD CVE feed - free, no key."""
from __future__ import annotations
import hashlib, logging
from datetime import datetime, timedelta, timezone
import httpx
from ..config import HTTP_HEADERS, HTTP_TIMEOUT

log = logging.getLogger(__name__)
NAME = "NVD CVE"
ENDPOINT = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def _make_id(cve_id): return hashlib.sha1(f"{NAME}::{cve_id}".encode()).hexdigest()

async def fetch(client: httpx.AsyncClient):
    end = datetime.now(timezone.utc); start = end - timedelta(days=2)
    params = {"pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"), "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"), "resultsPerPage": 50}
    resp = await client.get(ENDPOINT, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    items = resp.json().get("vulnerabilities") or []
    now_iso = datetime.now(timezone.utc).isoformat(); out = []
    for it in items:
        cve = it.get("cve") or {}; cve_id = cve.get("id") or ""
        if not cve_id: continue
        desc = next((d.get("value","") for d in (cve.get("descriptions") or []) if d.get("lang")=="en"), "")[:500]
        cvss = 0.0
        for key in ("cvssMetricV31","cvssMetricV30","cvssMetricV2"):
            arr = (cve.get("metrics") or {}).get(key) or []
            if arr:
                try: cvss = float(arr[0].get("cvssData",{}).get("baseScore") or 0.0)
                except: pass
                break
        if cvss < 7.0: continue
        out.append({"id": _make_id(cve_id), "source": NAME, "title": f"{cve_id} - CVSS {cvss}", "summary": desc, "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}", "published_at": cve.get("published"), "fetched_at": now_iso, "region": "global", "categories": ["cyber"], "importance": min(10.0, cvss), "raw_json": None})
    return out
