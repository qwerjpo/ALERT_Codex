# World Monitor — Personal OSINT Dashboard

世界の **軍事・安全保障の兆候** および **政治・外交の動向** を、リアルタイムで収集・表示するパーソナル OSINT ダッシュボードです。
完全に **無料** な公開ソース (RSS / 公的 API) のみを使用し、API キーや課金サービスは一切不要です。

> ALERT_Codex プロジェクトの一部として開発されています。

---

## 主な特徴

- **完全無料** — 認証不要・課金不要の公開ソースのみを利用
- **ローカル動作** — SQLite + FastAPI でホスティング不要・PC 1 台で完結
- **マルチソース統合** — RSS / GDELT / ReliefWeb / USGS / NASA FIRMS など 30+ 公開ソースを統合
- **自動タグ付け** — キーワードベースで「軍事」「安全保障」「外交」「災害」「サイバー」「経済制裁」等を自動分類
- **地域別フィルタ** — 中東 / 東アジア / 欧州 / ロシア・CIS / アフリカ / 米州 で絞り込み
- **重要度スコア** — タイトル・本文・ソース信頼度から自動算出
- **ダークテーマ・ダッシュボード UI** — リアルタイム更新、検索、絞り込み

---

## 統合データソース (全て無料・登録不要)

### 軍事・安全保障
- **ISW (Institute for the Study of War)** — ウクライナ戦況評価
- **Defense News** — 防衛産業・装備動向
- **The War Zone** — 戦術・戦闘機動向
- **Bellingcat** — OSINT 調査報道
- **Long War Journal** — テロ・対反乱作戦
- **Janes** — 防衛関連ヘッドライン (RSS 公開分)

### 政治・外交
- **Reuters World News**
- **BBC World / Politics**
- **Al Jazeera English**
- **NHK World**
- **EU External Action Service**
- **U.S. State Department Press Releases**
- **UN News**

### イベント・データセット系 API
- **GDELT 2.0 DOC API** — 全世界のニュースイベントを 15 分間隔で集計 (無料・キー不要)
- **ReliefWeb API** — UN OCHA の人道危機データ (無料・キー不要)
- **USGS Earthquake Feed** — リアルタイム地震 (M4.5+)
- **NASA FIRMS** — 衛星熱源検知 (爆発・大規模火災の兆候)
- **NOAA Tsunami / Weather Alerts**

### サイバー・情報
- **CISA Alerts** — 米サイバーセキュリティ庁公式アラート
- **NVD CVE Feed** — 重大脆弱性
- **The Record (Recorded Future)** — サイバー脅威ニュース

> ソースは `backend/config.py` で自由に追加・無効化できます。

---

## クイックスタート

### 必要環境
- Python 3.10+ (推奨 3.11)
- インターネット接続のみ

### インストール

```bash
git clone <this-repo>
cd ALERT_Codex
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 起動

```bash
# 初回データ取得 + サーバ起動 (推奨)
python -m backend.main

# または uvicorn で直接
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

ブラウザで <http://127.0.0.1:8000> を開きます。

データはバックグラウンドで自動更新されます (デフォルト 10 分間隔)。

---

## 構成

```
ALERT_Codex/
├── backend/
│   ├── main.py            # FastAPI エントリ
│   ├── config.py          # ソース定義・キーワード辞書
│   ├── db.py              # SQLite ストレージ
│   ├── classifier.py      # タグ付け・スコア算出
│   ├── scheduler.py       # 定期収集ジョブ
│   └── sources/
│       ├── rss.py         # 汎用 RSS コレクター
│       ├── gdelt.py       # GDELT DOC API
│       ├── reliefweb.py   # ReliefWeb API
│       ├── usgs.py        # USGS 地震
│       └── nasa_firms.py  # NASA FIRMS 火災
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/                  # SQLite DB (自動生成)
├── requirements.txt
└── README.md
```

---

## API

| Endpoint | 説明 |
|---|---|
| `GET /api/events` | 最新イベント一覧 (?region, ?category, ?q, ?limit) |
| `GET /api/stats` | カテゴリ別 / 地域別の集計 |
| `GET /api/sources` | 有効ソース一覧と最終取得時刻 |
| `POST /api/refresh` | 手動更新トリガー |

---

## ライセンス

MIT.

OSINT 用のパーソナル・ダッシュボードです。報道情報の二次利用はそれぞれの提供元の規約に従ってください。
