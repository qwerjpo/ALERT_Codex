from __future__ import annotations
from .config import KEYWORDS, REGION_KEYWORDS

def _norm(text):
    return (text or "").lower()

def classify_categories(title, summary="", base_categories=None):
    text = _norm(title) + " " + _norm(summary)
    matched = {c: 0.0 for c in (base_categories or [])}
    for category, kws in KEYWORDS.items():
        for kw, weight in kws:
            if kw in text:
                matched[category] = matched.get(category, 0.0) + weight
    cats = [c for c, s in matched.items() if s >= 0.5 or c in (base_categories or [])]
    score = sum(matched.values())
    return cats, score

def classify_region(title, summary="", fallback="global"):
    text = _norm(title) + " " + _norm(summary)
    best_region = fallback
    best_hits = 0
    for region, kws in REGION_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in text)
        if hits > best_hits:
            best_hits = hits
            best_region = region
    return best_region

def importance_score(title, summary="", keyword_score=0.0, source_weight=1.0):
    score = keyword_score * source_weight
    title_lower = _norm(title)
    boost_terms = [
        ("breaking", 1.5), ("urgent", 1.5), ("alert", 1.0),
        ("declares war", 4.0), ("ceasefire", 1.5), ("nuclear", 2.0),
        ("airstrike", 2.0), ("killed", 0.5), ("dead", 0.4),
    ]
    for term, b in boost_terms:
        if term in title_lower:
            score += b
    return round(min(10.0, max(0.0, score)), 2)

def enrich(title, summary, base_region, base_categories, source_weight=1.0):
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
