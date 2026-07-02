"""SHL catalog loader with semantic search using sentence-transformers."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Globals populated by load_catalog()
# ---------------------------------------------------------------------------
_catalog: list[dict] = []
_embeddings: Optional[np.ndarray] = None
_model = None  # SentenceTransformer instance


def _catalog_path() -> Path:
    """Resolve path to shl_catalog.json relative to project root."""
    # Try multiple locations
    candidates = [
        Path(__file__).resolve().parent.parent / "shl_catalog.json",
        Path("shl_catalog.json"),
        Path(os.getenv("CATALOG_PATH", "shl_catalog.json")),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "shl_catalog.json not found. Searched: "
        + ", ".join(str(c) for c in candidates)
    )


def load_catalog() -> None:
    """Load the JSON catalog and build the semantic search index.

    Call once at application startup.
    """
    global _catalog, _embeddings, _model

    path = _catalog_path()
    with open(path, "r", encoding="utf-8") as f:
        _catalog = json.load(f)

    logger.info("Loaded %d assessments from %s", len(_catalog), path)

    # Build search corpus: combine name + description + keywords + test_type
    corpus = []
    for item in _catalog:
        text = " | ".join(
            filter(
                None,
                [
                    item.get("name", ""),
                    item.get("description", ""),
                    ", ".join(item.get("keywords", [])) if isinstance(item.get("keywords"), list) else item.get("keywords", ""),
                    item.get("test_type", ""),
                ],
            )
        )
        corpus.append(text)

    # Load sentence-transformers model
    try:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")
        _embeddings = _model.encode(corpus, convert_to_numpy=True, show_progress_bar=False)
        _embeddings = _embeddings / np.linalg.norm(_embeddings, axis=1, keepdims=True)
        logger.info("Semantic index built – %d vectors of dim %d", *_embeddings.shape)
    except Exception as exc:
        logger.warning("sentence-transformers unavailable (%s); falling back to keyword search", exc)
        _model = None
        _embeddings = None


def _keyword_score(query: str, item: dict) -> float:
    """Simple keyword-overlap score used as fallback with field weights."""
    query_tokens = set(query.lower().split())
    if not query_tokens:
        return 0.0

    score = 0.0

    # Check name match (highest weight)
    name_tokens = set(item.get("name", "").lower().split())
    name_match = len(query_tokens & name_tokens)
    score += name_match * 5.0

    # Check keywords match (high weight)
    raw_keywords = item.get("keywords", [])
    if isinstance(raw_keywords, list):
        keyword_tokens = set(" ".join(raw_keywords).lower().split())
    else:
        keyword_tokens = set(str(raw_keywords).lower().split())
    keyword_match = len(query_tokens & keyword_tokens)
    score += keyword_match * 3.0

    # Check test_type match
    test_type_tokens = set(item.get("test_type", "").lower().split())
    test_type_match = len(query_tokens & test_type_tokens)
    score += test_type_match * 2.0

    # Check description match (lower weight)
    desc_tokens = set(item.get("description", "").lower().split())
    desc_match = len(query_tokens & desc_tokens)
    score += desc_match * 1.0

    # Normalise by total query tokens
    return score / len(query_tokens)



def search_catalog(
    query: str,
    top_k: int = 10,
    filters: dict | None = None,
) -> list[dict]:
    """Search the catalog semantically (or by keywords as fallback).

    Parameters
    ----------
    query : str
        Free-text search query.
    top_k : int
        Maximum results to return (capped at 10).
    filters : dict, optional
        Optional filters, e.g. ``{"test_type": "Ability & Aptitude"}``,
        ``{"remote_testing": True}``, ``{"adaptive_irt": True}``.

    Returns
    -------
    list[dict]
        Matched catalog items sorted by relevance, each augmented with a
        ``"score"`` key.
    """
    top_k = min(top_k, 10)
    pool = _catalog

    # Apply hard filters first
    if filters:
        for key, value in filters.items():
            pool = [
                item for item in pool
                if str(item.get(key, "")).lower() == str(value).lower()
            ]

    if not pool:
        return []

    if _model is not None and _embeddings is not None:
        # Semantic search
        q_emb = _model.encode([query], convert_to_numpy=True)
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)

        # If filters narrowed the pool, only consider those indices
        if filters:
            indices = [i for i, item in enumerate(_catalog) if item in pool]
            sub_emb = _embeddings[indices]
            scores = (sub_emb @ q_emb.T).flatten()
            ranked = np.argsort(-scores)[:top_k]
            results = []
            for idx in ranked:
                item = dict(pool[idx])
                item["score"] = round(float(scores[idx]), 4)
                results.append(item)
        else:
            scores = (_embeddings @ q_emb.T).flatten()
            ranked = np.argsort(-scores)[:top_k]
            results = []
            for idx in ranked:
                item = dict(_catalog[idx])
                item["score"] = round(float(scores[idx]), 4)
                results.append(item)
    else:
        # Keyword fallback
        scored = [(item, _keyword_score(query, item)) for item in pool]
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for item, score in scored[:top_k]:
            item_copy = dict(item)
            item_copy["score"] = round(score, 4)
            results.append(item_copy)

    return results


def get_all_categories() -> list[str]:
    """Return sorted list of unique test_type values in the catalog."""
    return sorted({item.get("test_type", "") for item in _catalog if item.get("test_type")})


def get_by_test_type(test_type: str) -> list[dict]:
    """Return all assessments matching a test_type (case-insensitive)."""
    t_lower = test_type.lower()
    return [item for item in _catalog if item.get("test_type", "").lower() == t_lower]


def compare_assessments(names: list[str]) -> list[dict]:
    """Return catalog entries matching the given assessment names.

    Matching is case-insensitive and supports partial matches.
    """
    results = []
    for name in names:
        name_lower = name.lower()
        for item in _catalog:
            if name_lower in item.get("name", "").lower():
                results.append(item)
                break
    return results


def get_catalog_summary() -> str:
    """Return a compact text summary of the catalog for the LLM prompt."""
    lines = []
    for item in _catalog:
        lines.append(
            f"- {item['name']} | Type: {item.get('test_type', 'N/A')} | "
            f"Remote: {item.get('remote_testing', 'N/A')} | "
            f"Adaptive: {item.get('adaptive_irt', 'N/A')} | "
            f"URL: {item.get('url', 'N/A')}"
        )
    return "\n".join(lines)


def get_catalog() -> list[dict]:
    """Return the raw catalog list."""
    return _catalog
