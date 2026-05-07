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

REFRESH_INTERVAL_SECONDS = int(os.environ.get("WM_REFRESH_INTERVAL", "600"))

HTTP_TIMEOUT = 25.0

HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36 WorldMonitor/0.1"
    ),
    "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, application/json;q=0.8, */*;q=0.5",
}

# --------------------------------------------------------------------------- #
# RSS / Atom feeds
# --------------------------------------------------------------------------- #
RSS_SOURCES: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════ #
    # 軍事・安全保障・防衛
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "ISW — Ukraine",
        "url": "https://www.understandingwar.org/rss.xml",
        "region": "europe",
        "categories": ["military", "security"],
        "weight": 1.5,
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
        "weight": 1.2,
    },
    {
        "name": "Breaking Defense",
        "url": "https://breakingdefense.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 1.1,
    },
    {
        "name": "Naval News",
        "url": "https://www.navalnews.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 1.1,
    },
    {
        "name": "USNI News",
        "url": "https://news.usni.org/feed",
        "region": "global",
        "categories": ["military"],
        "weight": 1.2,
    },
    {
        "name": "Defense One",
        "url": "https://www.defenseone.com/rss/all/",
        "region": "global",
        "categories": ["military", "politics"],
        "weight": 1.1,
    },
    {
        "name": "UK Defence Journal",
        "url": "https://ukdefencejournal.org.uk/feed/",
        "region": "europe",
        "categories": ["military"],
        "weight": 1.0,
    },
    {
        "name": "EurAsian Times",
        "url": "https://eurasiantimes.com/feed/",
        "region": "global",
        "categories": ["military", "politics"],
        "weight": 1.0,
    },
    {
        "name": "Army Recognition",
        "url": "https://www.armyrecognition.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 0.9,
    },
    {
        "name": "Military Times",
        "url": "https://www.militarytimes.com/rss/",
        "region": "americas",
        "categories": ["military"],
        "weight": 1.0,
    },
    {
        "name": "Task & Purpose",
        "url": "https://taskandpurpose.com/feed/",
        "region": "americas",
        "categories": ["military"],
        "weight": 0.9,
    },
    {
        "name": "Small Wars Journal",
        "url": "https://smallwarsjournal.com/rss.xml",
        "region": "global",
        "categories": ["military", "security"],
        "weight": 1.0,
    },
    {
        "name": "Air Wars",
        "url": "https://airwars.org/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 1.1,
    },
    {
        "name": "Defence Blog",
        "url": "https://defence-blog.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 0.9,
    },
    {
        "name": "The National Interest",
        "url": "https://nationalinterest.org/rss.xml",
        "region": "global",
        "categories": ["military", "politics"],
        "weight": 1.0,
    },
    {
        "name": "MilitaryWatch Magazine",
        "url": "https://militarywatchmagazine.com/feed/",
        "region": "global",
        "categories": ["military"],
        "weight": 0.9,
    },
    {
        "name": "DefenseWorld",
        "url": "https://www.defenseworld.net/rss",
        "region": "global",
        "categories": ["military"],
        "weight": 0.9,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # OSINT・インテリジェンス
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "Bellingcat",
        "url": "https://www.bellingcat.com/feed/",
        "region": "global",
        "categories": ["intelligence", "security"],
        "weight": 1.4,
    },
    {
        "name": "Long War Journal",
        "url": "https://www.longwarjournal.org/feed",
        "region": "global",
        "categories": ["military", "terrorism"],
        "weight": 1.3,
    },
    {
        "name": "Spy Talk",
        "url": "https://spytalk.co/feed/",
        "region": "global",
        "categories": ["intelligence"],
        "weight": 1.1,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # シンクタンク・政策分析
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "RUSI",
        "url": "https://rusi.org/rss/all",
        "region": "global",
        "categories": ["military", "security", "politics"],
        "weight": 1.2,
    },
    {
        "name": "RAND Corporation",
        "url": "https://www.rand.org/rss/research.xml",
        "region": "global",
        "categories": ["military", "politics", "security"],
        "weight": 1.1,
    },
    {
        "name": "CSIS",
        "url": "https://www.csis.org/rss",
        "region": "global",
        "categories": ["military", "politics"],
        "weight": 1.1,
    },
    {
        "name": "CFR — Council on Foreign Relations",
        "url": "https://www.cfr.org/rss/all",
        "region": "global",
        "categories": ["diplomacy", "politics"],
        "weight": 1.1,
    },
    {
        "name": "Atlantic Council",
        "url": "https://www.atlanticcouncil.org/feed/",
        "region": "global",
        "categories": ["politics", "security"],
        "weight": 1.0,
    },
    {
        "name": "Brookings Institution",
        "url": "https://www.brookings.edu/feed/",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Carnegie Endowment",
        "url": "https://carnegieendowment.org/rss/pubs",
        "region": "global",
        "categories": ["politics", "nuclear"],
        "weight": 1.0,
    },
    {
        "name": "ICG CrisisWatch",
        "url": "https://www.crisisgroup.org/crisiswatch/rss.xml",
        "region": "global",
        "categories": ["security", "politics"],
        "weight": 1.3,
    },
    {
        "name": "Stimson Center",
        "url": "https://www.stimson.org/feed/",
        "region": "global",
        "categories": ["nuclear", "security"],
        "weight": 1.0,
    },
    {
        "name": "SIPRI",
        "url": "https://www.sipri.org/rss",
        "region": "global",
        "categories": ["military", "nuclear"],
        "weight": 1.0,
    },
    {
        "name": "Foreign Policy",
        "url": "https://foreignpolicy.com/feed/",
        "region": "global",
        "categories": ["politics", "diplomacy"],
        "weight": 1.1,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # 核・大量破壊兵器
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "Bulletin of Atomic Scientists",
        "url": "https://thebulletin.org/feed/",
        "region": "global",
        "categories": ["nuclear"],
        "weight": 1.3,
    },
    {
        "name": "Arms Control Association",
        "url": "https://www.armscontrol.org/rss.xml",
        "region": "global",
        "categories": ["nuclear", "military"],
        "weight": 1.2,
    },
    {
        "name": "38North — North Korea",
        "url": "https://www.38north.org/feed/",
        "region": "asia",
        "categories": ["nuclear", "military"],
        "weight": 1.4,
    },
    {
        "name": "NTI — Nuclear Threat Initiative",
        "url": "https://www.nti.org/feed/",
        "region": "global",
        "categories": ["nuclear", "security"],
        "weight": 1.2,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # 国際政治・外交（グローバル）
    # ═══════════════════════════════════════════════════════════════════════ #
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
        "name": "Al Jazeera English",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "region": "global",
        "categories": ["politics"],
        "weight": 1.1,
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
        "region": "global",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "NHK World",
        "url": "https://www3.nhk.or.jp/nhkworld/en/news/feeds/",
        "region": "asia",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "RFI English",
        "url": "https://www.rfi.fr/en/rss",
        "region": "global",
        "categories": ["politics"],
        "weight": 0.9,
    },
    {
        "name": "Euronews — World",
        "url": "https://feeds.feedburner.com/euronews/en/news/",
        "region": "europe",
        "categories": ["politics"],
        "weight": 0.9,
    },
    {
        "name": "Politico Europe",
        "url": "https://www.politico.eu/feed/",
        "region": "europe",
        "categories": ["politics"],
        "weight": 1.0,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # 国際機関・外交
    # ═══════════════════════════════════════════════════════════════════════ #
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
        "name": "U.S. DoD News",
        "url": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=400&Site=945&max=10",
        "region": "americas",
        "categories": ["military", "diplomacy"],
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
    {
        "name": "Radio Free Europe / RFL",
        "url": "https://www.rferl.org/api/zgyipiieei/rss",
        "region": "europe",
        "categories": ["politics"],
        "weight": 1.1,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # ロシア・CIS・ウクライナ
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "Meduza — English",
        "url": "https://meduza.io/rss/en/all",
        "region": "russia_cis",
        "categories": ["politics"],
        "weight": 1.2,
    },
    {
        "name": "Kyiv Independent",
        "url": "https://kyivindependent.com/rss/",
        "region": "europe",
        "categories": ["politics", "military"],
        "weight": 1.3,
    },
    {
        "name": "The Moscow Times",
        "url": "https://www.themoscowtimes.com/rss/news",
        "region": "russia_cis",
        "categories": ["politics"],
        "weight": 1.1,
    },
    {
        "name": "Euromaidan Press",
        "url": "https://euromaidanpress.com/feed/",
        "region": "europe",
        "categories": ["politics", "military"],
        "weight": 1.2,
    },
    {
        "name": "Ukrinform",
        "url": "https://www.ukrinform.net/rss/block-lastnews",
        "region": "europe",
        "categories": ["politics", "military"],
        "weight": 1.1,
    },
    {
        "name": "UAWire",
        "url": "https://uawire.org/feed",
        "region": "europe",
        "categories": ["military", "politics"],
        "weight": 1.1,
    },
    {
        "name": "Kyiv Post",
        "url": "https://www.kyivpost.com/rss",
        "region": "europe",
        "categories": ["politics", "military"],
        "weight": 1.1,
    },
    {
        "name": "DW — Russia / Ukraine",
        "url": "https://rss.dw.com/rdf/rss-en-eu",
        "region": "europe",
        "categories": ["politics"],
        "weight": 1.0,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # 中東・北アフリカ
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "Times of Israel",
        "url": "https://www.timesofisrael.com/feed/",
        "region": "middle_east",
        "categories": ["politics", "military"],
        "weight": 1.1,
    },
    {
        "name": "Middle East Eye",
        "url": "https://www.middleeasteye.net/rss",
        "region": "middle_east",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Jerusalem Post",
        "url": "https://www.jpost.com/Rss/RssFeedsHeadlines.aspx",
        "region": "middle_east",
        "categories": ["politics", "military"],
        "weight": 1.0,
    },
    {
        "name": "Arab News",
        "url": "https://www.arabnews.com/rss.xml",
        "region": "middle_east",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Iran International",
        "url": "https://www.iranintl.com/en/rss",
        "region": "middle_east",
        "categories": ["politics", "military"],
        "weight": 1.2,
    },
    {
        "name": "Kurdistan 24",
        "url": "https://www.kurdistan24.net/rss",
        "region": "middle_east",
        "categories": ["politics", "security"],
        "weight": 1.0,
    },
    {
        "name": "Middle East Monitor",
        "url": "https://www.middleeastmonitor.com/feed/",
        "region": "middle_east",
        "categories": ["politics"],
        "weight": 0.9,
    },
    {
        "name": "Rudaw",
        "url": "https://www.rudaw.net/english/rss",
        "region": "middle_east",
        "categories": ["politics", "security"],
        "weight": 1.0,
    },
    {
        "name": "Anadolu Agency",
        "url": "https://www.aa.com.tr/en/rss/default?cat=world",
        "region": "middle_east",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Al-Monitor",
        "url": "https://www.al-monitor.com/rss",
        "region": "middle_east",
        "categories": ["politics"],
        "weight": 1.0,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # アジア・太平洋
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "South China Morning Post",
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
        "weight": 1.2,
    },
    {
        "name": "Asia Times",
        "url": "https://asiatimes.com/feed/",
        "region": "asia",
        "categories": ["politics", "military"],
        "weight": 1.0,
    },
    {
        "name": "East Asia Forum",
        "url": "https://www.eastasiaforum.org/feed/",
        "region": "asia",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Japan Times — World",
        "url": "https://www.japantimes.co.jp/feed/topstories/",
        "region": "asia",
        "categories": ["politics"],
        "weight": 1.0,
    },
    {
        "name": "Radio Free Asia",
        "url": "https://www.rfa.org/english/rss2.xml",
        "region": "asia",
        "categories": ["politics"],
        "weight": 1.1,
    },
    {
        "name": "Taiwan News",
        "url": "https://www.taiwannews.com.tw/rss",
        "region": "asia",
        "categories": ["politics", "military"],
        "weight": 1.1,
    },
    {
        "name": "Korea Times",
        "url": "https://www.koreatimes.co.kr/www/rss/rss.xml",
        "region": "asia",
        "categories": ["politics"],
        "weight": 0.9,
    },
    {
        "name": "Global Times",
        "url": "https://www.globaltimes.cn/rss/outboundfeeds/rss.xml",
        "region": "asia",
        "categories": ["politics"],
        "weight": 0.8,
    },
    {
        "name": "DW — Asia",
        "url": "https://rss.dw.com/rdf/rss-en-asia",
        "region": "asia",
        "categories": ["politics"],
        "weight": 0.9,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # アフリカ・サブサハラ
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "AllAfrica",
        "url": "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf",
        "region": "africa",
        "categories": ["politics", "security"],
        "weight": 0.9,
    },
    {
        "name": "Africa News",
        "url": "https://www.africanews.com/feed/",
        "region": "africa",
        "categories": ["politics"],
        "weight": 0.9,
    },
    {
        "name": "The Africa Report",
        "url": "https://www.theafricareport.com/feed/",
        "region": "africa",
        "categories": ["politics"],
        "weight": 0.9,
    },
    {
        "name": "The New Humanitarian",
        "url": "https://www.thenewhumanitarian.org/rss.xml",
        "region": "africa",
        "categories": ["security", "politics"],
        "weight": 1.1,
    },
    {
        "name": "DW — Africa",
        "url": "https://rss.dw.com/rdf/rss-en-africa",
        "region": "africa",
        "categories": ["politics"],
        "weight": 0.9,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # サイバーセキュリティ
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "CISA Alerts",
        "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.4,
    },
    {
        "name": "The Record — Cyber",
        "url": "https://therecord.media/feed",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.2,
    },
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.0,
    },
    {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.2,
    },
    {
        "name": "SecurityWeek",
        "url": "https://feeds.feedburner.com/Securityweek",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.0,
    },
    {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com/rss.xml",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.0,
    },
    {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.0,
    },
    {
        "name": "Ars Technica — Security",
        "url": "https://feeds.arstechnica.com/arstechnica/security",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.0,
    },
    {
        "name": "SANS Internet Storm Center",
        "url": "https://isc.sans.edu/rssfeed_full.xml",
        "region": "global",
        "categories": ["cyber"],
        "weight": 1.1,
    },
    {
        "name": "Infosecurity Magazine",
        "url": "https://www.infosecurity-magazine.com/rss/news/",
        "region": "global",
        "categories": ["cyber"],
        "weight": 0.9,
    },
    {
        "name": "Cybersecurity Insiders",
        "url": "https://www.cybersecurity-insiders.com/feed/",
        "region": "global",
        "categories": ["cyber"],
        "weight": 0.9,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # 経済制裁・輸出規制
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "U.S. Treasury — Press Releases",
        "url": "https://home.treasury.gov/news/press-releases/rss.xml",
        "region": "americas",
        "categories": ["economic"],
        "weight": 1.3,
    },

    # ═══════════════════════════════════════════════════════════════════════ #
    # 人道支援・難民
    # ═══════════════════════════════════════════════════════════════════════ #
    {
        "name": "ICRC — Red Cross",
        "url": "https://www.icrc.org/en/rss",
        "region": "global",
        "categories": ["security"],
        "weight": 1.0,
    },
    {
        "name": "MSF — Doctors Without Borders",
        "url": "https://www.msf.org/rss/all",
        "region": "global",
        "categories": ["security"],
        "weight": 1.0,
    },
]

# --------------------------------------------------------------------------- #
# GDELT DOC API クエリ（完全無料・キー不要）
# --------------------------------------------------------------------------- #
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
        "query": '(summit OR ambassador OR treaty OR diplomatic OR "foreign minister") sourcelang:eng',
        "categories": ["diplomacy"],
        "max_records": 30,
        "weight": 0.9,
    },
    {
        "name": "GDELT — Cyber Warfare",
        "query": '(cyberattack OR ransomware OR "cyber espionage" OR hacker OR "data breach") sourcelang:eng',
        "categories": ["cyber"],
        "max_records": 30,
        "weight": 0.9,
    },
    {
        "name": "GDELT — Nuclear / WMD",
        "query": '(nuclear OR "ballistic missile" OR "chemical weapon" OR ICBM OR warhead) sourcelang:eng',
        "categories": ["nuclear", "military"],
        "max_records": 30,
        "weight": 1.0,
    },
    {
        "name": "GDELT — Terrorism / Extremism",
        "query": '(terrorism OR ISIS OR jihadist OR "suicide bomb" OR extremist OR insurgency) sourcelang:eng',
        "categories": ["terrorism", "security"],
        "max_records": 30,
        "weight": 0.9,
    },
    {
        "name": "GDELT — Economic / Sanctions",
        "query": '(sanctions OR embargo OR "export control" OR "frozen assets" OR OFAC) sourcelang:eng',
        "categories": ["economic"],
        "max_records": 30,
        "weight": 0.9,
    },
    {
        "name": "GDELT — Africa / Sahel",
        "query": '(Sahel OR Mali OR Niger OR "Burkina Faso" OR Sudan OR Somalia OR jihadist) sourcelang:eng',
        "categories": ["security", "military"],
        "max_records": 30,
        "weight": 0.9,
        "region": "africa",
    },
    {
        "name": "GDELT — Indo-Pacific / Taiwan",
        "query": '(Taiwan OR "South China Sea" OR AUKUS OR "Indo-Pacific" OR Strait) sourcelang:eng',
        "categories": ["military", "politics"],
        "max_records": 30,
        "weight": 1.0,
        "region": "asia",
    },
]

# --------------------------------------------------------------------------- #
# 構造化 API ソース
# --------------------------------------------------------------------------- #
RELIEFWEB_LIMIT = 30

USGS_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"

# --------------------------------------------------------------------------- #
# 地域・カテゴリ定義
# --------------------------------------------------------------------------- #
REGIONS = {
    "global":      "Global",
    "europe":      "Europe",
    "russia_cis":  "Russia / CIS",
    "middle_east": "Middle East",
    "asia":        "Asia-Pacific",
    "americas":    "Americas",
    "africa":      "Africa",
}

CATEGORIES = {
    "military":    "Military",
    "security":    "Security",
    "politics":    "Politics",
    "diplomacy":   "Diplomacy",
    "cyber":       "Cyber",
    "terrorism":   "Terrorism",
    "intelligence":"Intelligence",
    "disaster":    "Disaster",
    "economic":    "Economic / Sanctions",
    "nuclear":     "Nuclear / WMD",
}

# --------------------------------------------------------------------------- #
# 分類用キーワード辞書
# --------------------------------------------------------------------------- #
KEYWORDS: dict[str, list[tuple[str, float]]] = {
    "military": [
        ("airstrike", 1.5), ("air strike", 1.5), ("missile", 1.4), ("drone strike", 1.6),
        ("drone attack", 1.5), ("kamikaze drone", 1.5),
        ("offensive", 1.3), ("counteroffensive", 1.4), ("ceasefire", 1.2),
        ("troops", 1.0), ("battalion", 1.1), ("brigade", 1.0), ("division", 0.9),
        ("warship", 1.2), ("submarine", 1.2), ("fighter jet", 1.2), ("artillery", 1.3),
        ("invasion", 1.6), ("occupied territory", 1.2), ("frontline", 1.2),
        ("mobilization", 1.3), ("conscription", 1.2), ("deployment", 1.0),
        ("casualties", 1.2), ("killed in action", 1.3), ("wounded", 1.0),
        ("amphibious", 1.2), ("carrier strike group", 1.3), ("naval blockade", 1.4),
        ("tank", 1.0), ("armor", 0.9), ("armored vehicle", 1.0),
        ("special forces", 1.2), ("paratrooper", 1.1), ("commando", 1.1),
        ("military exercise", 1.1), ("war games", 1.1), ("drill", 0.8),
        ("fighter", 1.0), ("bomber", 1.2), ("stealth", 1.1), ("hypersonic", 1.4),
        ("long-range strike", 1.3), ("precision strike", 1.2),
        ("siege", 1.3), ("encirclement", 1.3), ("withdrawal", 1.1),
        ("escalation", 1.2), ("de-escalation", 1.0),
    ],
    "nuclear": [
        ("nuclear", 1.6), ("warhead", 1.7), ("icbm", 1.7), ("hypersonic missile", 1.5),
        ("uranium enrichment", 1.7), ("plutonium", 1.6), ("iaea", 1.3),
        ("strategic forces", 1.4), ("nuclear test", 1.9), ("nuclear weapon", 1.8),
        ("dirty bomb", 1.7), ("radiological", 1.5), ("reactor sabotage", 1.6),
        ("nuclear deal", 1.3), ("non-proliferation", 1.2), ("npt", 1.2),
        ("tactical nuclear", 1.6), ("first strike", 1.5), ("nuclear alert", 1.7),
        ("start treaty", 1.3), ("new start", 1.3),
    ],
    "diplomacy": [
        ("ambassador", 1.2), ("expel ambassador", 1.5), ("foreign minister", 1.2),
        ("summit", 1.3), ("bilateral", 1.0), ("multilateral", 1.0),
        ("treaty", 1.2), ("signed agreement", 1.1), ("memorandum", 0.9),
        ("united nations", 1.1), ("security council", 1.4), ("veto", 1.3),
        ("g7", 1.1), ("g20", 1.1), ("nato", 1.2), ("eu council", 1.1),
        ("asean", 1.0), ("quad", 1.1), ("aukus", 1.2), ("five eyes", 1.2),
        ("sanctions imposed", 1.4), ("diplomatic incident", 1.3),
        ("persona non grata", 1.4), ("consulate", 0.9),
    ],
    "politics": [
        ("president", 0.8), ("prime minister", 0.8), ("parliament", 0.8),
        ("election", 1.0), ("coup", 1.7), ("coup attempt", 1.8),
        ("protest", 1.0), ("uprising", 1.3), ("government collapse", 1.4),
        ("martial law", 1.6), ("state of emergency", 1.4),
        ("assassination", 1.7), ("political crisis", 1.3),
        ("referendum", 1.1), ("regime change", 1.4),
    ],
    "cyber": [
        ("cyber", 1.4), ("cyberattack", 1.5), ("ransomware", 1.5), ("malware", 1.3),
        ("apt", 1.4), ("advanced persistent threat", 1.4),
        ("zero-day", 1.6), ("zero day", 1.6), ("cve-", 1.3), ("ddos", 1.4),
        ("data breach", 1.4), ("phishing", 1.1), ("supply chain attack", 1.6),
        ("critical infrastructure attack", 1.6), ("power grid attack", 1.7),
        ("espionage malware", 1.5), ("state-sponsored hack", 1.5),
        ("backdoor", 1.3), ("trojan", 1.2), ("botnet", 1.2),
        ("sandworm", 1.4), ("lazarus group", 1.4), ("cozy bear", 1.4),
        ("fancy bear", 1.4), ("volt typhoon", 1.5), ("salt typhoon", 1.5),
    ],
    "terrorism": [
        ("terror", 1.5), ("terrorist attack", 1.7), ("isis", 1.5), ("isil", 1.5),
        ("islamic state", 1.5), ("al-qaeda", 1.5), ("al qaeda", 1.5),
        ("suicide bomb", 1.8), ("car bomb", 1.7), ("iied", 1.6), ("ied", 1.4),
        ("hostage", 1.5), ("kidnapped", 1.3), ("abduction", 1.2),
        ("boko haram", 1.4), ("al-shabaab", 1.4), ("taliban", 1.3),
        ("hamas", 1.4), ("hezbollah", 1.4), ("houthi", 1.3),
        ("jihadist", 1.4), ("extremist", 1.2), ("radicalization", 1.1),
        ("mass shooting", 1.4), ("mass casualty", 1.5),
    ],
    "intelligence": [
        ("intelligence", 1.0), ("espionage", 1.5), ("spy", 1.3),
        ("classified", 1.1), ("leak", 1.1), ("whistleblower", 1.1),
        ("cia", 1.2), ("nsa", 1.2), ("mi6", 1.2), ("mossad", 1.2), ("fsb", 1.3),
        ("gru", 1.3), ("svr", 1.2), ("counterintelligence", 1.3),
        ("surveillance", 1.0), ("intercept", 1.0), ("signals intelligence", 1.2),
        ("defect", 1.3), ("double agent", 1.4),
    ],
    "economic": [
        ("sanction", 1.4), ("sanctioned", 1.4), ("embargo", 1.4),
        ("tariff", 1.1), ("trade war", 1.3), ("frozen assets", 1.3),
        ("export control", 1.3), ("chip ban", 1.3), ("semiconductor", 1.0),
        ("energy crisis", 1.2), ("oil embargo", 1.3), ("gas supply", 1.1),
        ("dollar weaponization", 1.2), ("swift", 1.2), ("central bank", 0.9),
        ("currency crisis", 1.1), ("inflation crisis", 0.9), ("debt default", 1.2),
    ],
    "disaster": [
        ("earthquake", 1.3), ("magnitude", 1.0), ("tsunami", 1.6),
        ("flood", 1.0), ("wildfire", 1.0), ("hurricane", 1.2),
        ("typhoon", 1.2), ("cyclone", 1.1), ("famine", 1.3),
        ("humanitarian crisis", 1.2), ("mass displacement", 1.2),
    ],
    "security": [
        ("border clash", 1.5), ("cross-border", 1.2), ("security forces", 1.0),
        ("paramilitary", 1.3), ("militia", 1.2), ("insurgent", 1.3), ("rebel", 1.2),
        ("warlord", 1.2), ("armed group", 1.1), ("convoy attack", 1.3),
        ("peacekeeping", 1.0), ("un mission", 1.0), ("nato mission", 1.1),
    ],
}

REGION_KEYWORDS: dict[str, list[str]] = {
    "europe": [
        "ukraine", "russia", "kyiv", "moscow", "poland", "germany", "france",
        "uk", "britain", "european union", "eu ", "nato", "balkan", "moldova",
        "belarus", "baltic", "finland", "sweden", "italy", "spain", "czechia",
        "hungary", "romania", "slovakia", "estonia", "latvia", "lithuania",
        "donbas", "zaporizhzhia", "kherson", "kharkiv", "mariupol",
    ],
    "russia_cis": [
        "kremlin", "putin", "russia", "belarus", "kazakhstan", "armenia",
        "azerbaijan", "uzbekistan", "kyrgyzstan", "tajikistan", "georgia",
        "minsk", "almaty", "tashkent", "yerevan", "baku",
    ],
    "middle_east": [
        "israel", "palestin", "gaza", "west bank", "hamas", "hezbollah",
        "lebanon", "beirut", "syria", "damascus", "iraq", "baghdad",
        "iran", "tehran", "saudi", "riyadh", "yemen", "sanaa", "houthi",
        "uae", "dubai", "abu dhabi", "qatar", "doha", "jordan", "amman",
        "egypt", "cairo", "turkey", "ankara", "kurdish", "sinai",
    ],
    "asia": [
        "china", "beijing", "taiwan", "taipei", "japan", "tokyo", "osaka",
        "north korea", "pyongyang", "south korea", "seoul",
        "philippines", "manila", "vietnam", "hanoi", "indonesia", "jakarta",
        "myanmar", "yangon", "thailand", "bangkok", "india", "new delhi",
        "pakistan", "islamabad", "afghanistan", "kabul",
        "australia", "canberra", "south china sea", "taiwan strait",
        "senkaku", "diaoyu", "quad", "aukus", "indopacific",
    ],
    "americas": [
        "united states", "u.s.", "usa", "washington", "pentagon", "white house",
        "congress", "senate", "mexico", "mexico city", "canada", "ottawa",
        "venezuela", "caracas", "colombia", "bogota", "brazil", "brasilia",
        "argentina", "buenos aires", "cuba", "havana", "haiti",
        "central america", "latin america", "caribbean",
    ],
    "africa": [
        "sudan", "khartoum", "ethiopia", "addis ababa", "somalia", "mogadishu",
        "nigeria", "abuja", "mali", "bamako", "niger", "niamey",
        "burkina faso", "ouagadougou", "libya", "tripoli", "morocco", "rabat",
        "algeria", "algiers", "tunisia", "south africa", "pretoria",
        "kenya", "nairobi", "drc", "congo", "kinshasa", "sahel",
        "mozambique", "chad", "cameroon", "central african republic",
        "al-shabaab", "boko haram", "aqim", "jnim",
    ],
}
