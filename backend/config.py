"""
Configuration for World Monitor.

すべての設定値はここに集約されています。データソースの追加・無効化、
キーワード辞書の調整、収集間隔の変更などはこのファイルで行います。
"""

from __future__ import annotations

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths / runtime
# --------------------------------------------------------------------------- #
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "world_monitor.db"
FRONTEND_DIR = ROOT_DIR / "frontend"

# 収集間隔 (秒)
REFRESH_INTERVAL_SECONDS = int(os.environ.get("WM_REFRESH_INTERVAL", "600"))

# HTTP リクエストのタイムアウト
HTTP_TIMEOUT = 20.0

# UA はブロック回避のためブラウザ風に
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36 WorldMonitor/0.1"
    ),
    "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, application/json;q=0.8, */*;q=0.5",
}

# --------------------------------------------------------------------------- #
# RSS / Atom feeds (完全無料・登録不要)
# --------------------------------------------------------------------------- #
# (name, url, default_region, default_categories, source_weight)
RSS_SOURCES: list[dict] = [
    # ── 軍事・安全保障 ─────────────────────────────────────────────
    {
        "name": "ISW — Ukraine",
        "url": "https://www.understandingwar.org/rss.xml",
        "region": "europe",
        "categories": ["military", "security"],
        "weight": 1.4,
    },
    {
        "name": "Defense News",
        "url": "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml",
        "region": "global",
        "categories": ["military"],
        "weight": 1.2,
    },
    {
        "name": "The War Zone",
        "url": "https://www.twz.com/feed",
        "region": "global",
        "categories": ["military"],
        "weight": 1.1,
    },
    {
        "name": "Bellingcat",
        "url": "https://www.bellingcat.com/feed/",
        "region": "global",
        "categories": ["intelligence", "security"],
        "weight": 1.3,
    },
    {
        "name": "Long War Journal",
        "url": "https://www.longwarjournal.org/feed",
        "region": "global",
        "categories": ["military", "terrorism"],
        "weight": 1.2,
    },
    {
        "name": "Naval News",
        "url": "https://www.navalnews.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 1.0,
    },
    {
        "name": "Breaking Defense",
        "url": "https://breakingdefense.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 1.0,
    },
    # ── 政治・外交 ─────────────────────────────────────────────
    {
        "name": "Reuters — World",
        "url": "https://feeds.reuters.com/Reuters/worldNews",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.2,
    },
    {
        "name": "BBC — World",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.1,
    },
    {
        "name": "BBC — Politics",
        "url": "https://feeds.bbci.co.uk/news/politics/rss.xml",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Al Jazeera English",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.1,
    },
    {
        "name": "NHK World",
        "url": "https://www3.nhk.or.jp/nhkworld/en/news/feeds/",
        "region": "asia",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "France24 — World",
        "url": "https://www.france24.com/en/rss",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "DW — Top Stories",
        "url": "https://rss.dw.com/rdf/rss-en-all",
        "region": "europe",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "UN News",
        "url": "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
        "region": "global",
        "categories": ["diplomacy"],
        "weight": 1.1,
    },
    {
        "name": "U.S. State Department",
        "url": "https://www.state.gov/rss-feed/press-releases/feed/",
        "region": "americas",
        "categories": ["diplomacy"],
        "weight": 1.2,
    },
    {
        "name": "EU External Action",
        "url": "https://www.eeas.europa.eu/eeas/press-material_en/rss.xml",
        "region": "europe",
        "categories": ["diplomacy"],
        "weight": 1.1,
    },
    {
        "name": "NATO News",
        "url": "https://www.nato.int/cps/en/natohq/news.rss",
        "region": "europe",
        "categories": ["military", "diplomacy"],
        "weight": 1.2,
    },
    # ── サイバー ─────────────────────────────────────────────
    {
        "name": "CISA Alerts",
        "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.3,
    },
    {
        "name": "The Record",
        "url": "https://therecord.media/feed",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.1,
    },
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "region": "global",
        "categories": ["cyber"],
        "weight": 0.9,
    },
    # ── アジア・太平洋 ─────────────────────────────────────────────
    {
        "name": "South China Morning Post — China",
        "url": "https://www.scmp.com/rss/4/feed",
        "region": "asia",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "The Diplomat",
        "url": "https://thediplomat.com/feed/",
        "region": "asia",
        "categories": ["politics", "military"],
        "weight": 1.1,
    },
    # ── 中東 ─────────────────────────────────────────────
    {
        "name": "Times of Israel",
        "url": "https://www.timesofisrael.com/feed/",
        "region": "middle_east",
        "categories": ["politics", "military"],
        "weight": 1.0,
    },
    {
        "name": "Middle East Eye",
        "url": "https://www.middleeasteye.net/rss",
        "region": "middle_east",
        "categories": ["politics"],
        "weight": 1.0,
    },
    # ── ロシア・CIS ─────────────────────────────────────────────
    {
        "name": "Meduza — English",
        "url": "https://meduza.io/rss/en/all",
        "region": "russia_cis",
        "categories": ["politics"],
        "weight": 1.1,
    },
    {
        "name": "Kyiv Independent",
        "url": "https://kyivindependent.com/rss/",
        "region": "europe",
        "categories": ["politics", "military"],
        "weight": 1.2,
    },
]

# --------------------------------------------------------------------------- #
# 構造化 API ソース
# --------------------------------------------------------------------------- #
# GDELT DOC API — 完全無料・キー不要
# https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
GDELT_QUERIES: list[dict] = [
    {
        "name": "GDELT — Military Conflict",
        "query": '(military OR conflict OR offensive OR ceasefire OR sanctions) sourcelang:eng',
        "categories": ["military", "politics"],
        "max_records": 50,
        "weight": 0.9,
    },
    {
        "name": "GDELT — Diplomatic Crisis",
        "query": '(summit OR ambassador OR treaty OR diplomatic OR \"foreign minister\") sourcelang:eng',
        "categories": ["diplomacy"],
        "max_records": 30,
        "weight": 0.9,
    },
]

# ReliefWeb API — UN OCHA 公開、キー不要
# https://reliefweb.int/help/api
RELIEFWEB_LIMIT = 30

# USGS — 地震
USGS_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"

# NASA FIRMS Active Fire — VIIRS NRT (登録なしの公開 CSV)
# 注意: 戦闘・爆発の二次的兆候として収集 (火災と区別はできない)
NASA_FIRMS_URL = (
    "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    # MAP_KEY は不要のデモエンドポイント版を使う場合は alternate を `config.local.py` で上書き
)

# --------------------------------------------------------------------------- #
# 地域・カテゴリ定義
# --------------------------------------------------------------------------- #
REGIONS = {
    "global": "Global",
    "europe": "Europe",
    "russia_cis": "Russia / CIS",
    "middle_east": "Middle East",
    "asia": "Asia-Pacific",
    "americas": "Americas",
    "africa": "Africa",
}

CATEGORIES = {
    "military": "Military",
    "security": "Security",
    "politics": "Politics",
    "diplomacy": "Diplomacy",
    "cyber": "Cyber",
    "terrorism": "Terrorism",
    "intelligence": "Intelligence",
    "disaster": "Disaster",
    "economic": "Economic / Sanctions",
    "nuclear": "Nuclear / WMD",
}

# --------------------------------------------------------------------------- #
# 分類用キーワード辞書 — 簡易ルールベース
# --------------------------------------------------------------------------- #
# (lower-case substring → category, score boost)
KEYWORDS: dict[str, list[tuple[str, float]]] = {
    "military": [
        ("airstrike", 1.5), ("air strike", 1.5), ("missile", 1.4), ("drone strike", 1.6),
        ("offensive", 1.3), ("counteroffensive", 1.4), ("ceasefire", 1.2),
        ("troops", 1.0), ("battalion", 1.1), ("brigade", 1.0), ("division", 0.9),
        ("warship", 1.2), ("submarine", 1.2), ("fighter jet", 1.2), ("artillery", 1.3),
        ("invasion", 1.6), ("occupied", 1.0), ("frontline", 1.2), ("mobilization", 1.3),
        ("conscription", 1.2), ("deployment", 1.0), ("casualties", 1.2),
    ],
    "nuclear": [
        ("nuclear", 1.6), ("warhead", 1.7), ("icbm", 1.7), ("hypersonic", 1.4),
        ("uranium enrichment", 1.6), ("plutonium", 1.5), ("iaea", 1.2),
        ("strategic forces", 1.3), ("nuclear test", 1.8),
    ],
    "diplomacy": [
        ("ambassador", 1.2), ("foreign minister", 1.2), ("summit", 1.3),
        ("bilateral", 1.0), ("multilateral", 1.0), ("treaty", 1.2),
        ("united nations", 1.1), ("security council", 1.4), ("g7", 1.1), ("g20", 1.1),
        ("nato", 1.2), ("eu council", 1.1), ("asean", 1.0),
    ],
    "politics": [
        ("president", 0.8), ("prime minister", 0.8), ("parliament", 0.8),
        ("election", 1.0), ("coup", 1.6), ("protest", 1.0), ("government", 0.6),
    ],
    "cyber": [
        ("cyber", 1.4), ("ransomware", 1.4), ("malware", 1.3), ("apt", 1.3),
        ("zero-day", 1.5), ("zero day", 1.5), ("cve-", 1.2), ("ddos", 1.3),
        ("data breach", 1.3), ("phishing", 1.0), ("supply chain attack", 1.5),
    ],
    "terrorism": [
        ("terror", 1.5), ("isis", 1.4), ("isil", 1.4), ("al-qaeda", 1.4),
        ("al qaeda", 1.4), ("suicide bomb", 1.7), ("car bomb", 1.6),
        ("hostage", 1.5), ("kidnapped", 1.3),
    ],
    "intelligence": [
        ("intelligence", 1.0), ("espionage", 1.4), ("spy", 1.2),
        ("classified", 1.0), ("leak", 1.0), ("whistleblower", 1.0),
    ],
    "economic": [
        ("sanction", 1.3), ("embargo", 1.3), ("tariff", 1.0),
        ("frozen assets", 1.2), ("export control", 1.2), ("oil price", 0.8),
    ],
    "disaster": [
        ("earthquake", 1.2), ("tsunami", 1.5), ("flood", 1.0),
        ("wildfire", 1.0), ("hurricane", 1.1), ("typhoon", 1.1),
    ],
    "security": [
        ("border clash", 1.5), ("security forces", 1.0), ("paramilitary", 1.2),
        ("militia", 1.2), ("insurgent", 1.3), ("rebel", 1.2),
    ],
}

# 地域判定キーワード (大文字小文字無視)
REGION_KEYWORDS: dict[str, list[str]] = {
    "europe": [
        "ukraine", "russia", "kyiv", "moscow", "poland", "germany", "france",
        "uk", "britain", "european union", "eu ", "nato", "balkan", "moldova",
        "belarus", "baltic", "finland", "sweden", "italy", "spain",
    ],
    "russia_cis": [
        "kremlin", "putin", "russia", "belarus", "kazakhstan", "armenia",
        "azerbaijan", "uzbekistan", "kyrgyzstan", "tajikistan", "georgia",
    ],
    "middle_east": [
        "israel", "palestin", "gaza", "hamas", "hezbollah", "lebanon", "syria",
        "iraq", "iran", "tehran", "saudi", "yemen", "houthi", "uae", "qatar",
        "jordan", "egypt", "turkey", "ankara",
    ],
    "asia": [
        "china", "beijing", "taiwan", "japan", "tokyo", "north korea", "pyongyang",
        "south korea", "seoul", "philippines", "vietnam", "indonesia",
        "myanmar", "thailand", "india", "pakistan", "afghanistan",
        "australia", "south china sea",
    ],
    "americas": [
        "united states", "u.s.", "usa", "washington", "pentagon", "white house",
        "mexico", "canada", "venezuela", "colombia", "brazil", "argentina",
        "cuba", "haiti",
    ],
    "africa": [
        "sudan", "ethiopia", "somalia", "nigeria", "mali", "niger",
        "burkina faso", "libya", "morocco", "algeria", "tunisia",
        "south africa", "kenya", "drc", "congo", "sahel",
    ],
}
