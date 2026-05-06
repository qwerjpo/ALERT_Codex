"""
シンプルなキーワードベースの分類器とスコアリング。

機械学習を使わずに、辞書ルールだけで:
  - カテゴリ (軍事/政治/サイバー...) のタグ付け
  - 地域 (中東/東アジア...) の推定
  - 重要度スコア (0.0-10.0) の算出
を行います。完全にオフライン・依存ゼロ。
"""

from __future__ import annotations

from .config import KEYWORDS, REGION_KEYWORDS


def _norm(text: str | None) -> str:
    return (text or "").lower()


def classify_categories(
    title: str,
    summary: str = "",
    base_categories: list[str] | None = None,
) -> tuple[list[str], float]:
    """
    タイトル+サマリからカテゴリを推定し、寄与スコアの合計も返す。

    base_categories はソース固有の事前タグ (例: Defense News → ["military"])。
    """
    text = _norm(title) + " " + _norm(summary)
    matched: dict[str, float] = {c: 0.0 for c in (base_categories or [])}

    for category, kws in KEYWORDS.items():
        for kw, weight in kws:
            if kw in text:
                matched[category] = matched.get(category, 0.0) + weight

    # 弱いマッチ (0.5 未満) は除外
    cats = [c for c, s in matched.items() if s >= 0.5 or c in (base_categories or [])]
    score = sum(matched.values())
    return cats, score


def classify_region(
    title: str,
    summary: str = "",
    fallback: str = "global",
) -> str:
    """
    タイトル+サマリから地域を推定。最初に強くマッチした地域を返す。
    """
    text = _norm(title) + " " + _norm(summary)
    best_region = fallback
    best_hits = 0
    for region, kws in REGION_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in text)
        if hits > best_hits:
            best_hits = hits
            best_region = region
    return best_region


def importance_score(
    title: str,
    summary: str = "",
    keyword_score: float = 0.0,
    source_weight: float = 1.0,
) -> float:
    """
    最終的な重要度を 0-10 でクリップして返す。
      - キーワードスコア (主要因子)
      - ソース信頼度
      - タイトル中の「警報」語の追加ブースト
    """
    score = keyword_score * source_weight

    title_lower = _norm(title)
    boost_terms = (
        ("breaking", 1.5),
        ("urgent", 1.5),
        ("alert", 1.0),
        ("declares war", 4.0),
        ("ceasefire", 1.5),
        ("nuclear", 2.0),
        ("airstrike", 2.0),
        ("killed", 0.5),
        ("dead", 0.4),
    )
    for term, b in boost_terms:
        if term in title_lower:
            score += b

    if score < 0:
        score = 0.0
    if score > 10:
        score = 10.0
    return round(score, 2)


def enrich(
    title: str,
    summary: str,
    base_region: str | None,
    base_categories: list[str] | None,
    source_weight: float = 1.0,
) -> dict:
    """
    タイトル/サマリ/ソース情報を入力に、分類+スコアを一括で返す。
    """
    cats, kw_score = classify_categories(title, summary, base_categories)
    region = base_region if base_region and base_region != "global" else classify_region(
        title, summary, fallback=base_region or "global"
    )
    importance = importance_score(title, summary, kw_score, source_weight)
    return {
        "region": region,
        "categories": cats or (base_categories or ["politics"]),
        "importance": importance,
    }
