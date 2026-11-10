from __future__ import annotations

from typing import Any

import requests

# Free public API, no key required: https://hn.algolia.com/api
API_URL = "https://hn.algolia.com/api/v1/search"
MAX_LIMIT = 20


def hn_search(query: str = "", limit: int = 5) -> dict[str, Any]:
    """Search Hacker News stories by keyword. Returns an error dict instead of raising."""
    if not isinstance(query, str) or not query.strip():
        return {"error": "ValueError", "message": "query is required"}
    try:
        limit = max(1, min(int(limit), MAX_LIMIT))  # model may send "5", 0 or 100
    except (TypeError, ValueError):
        return {"error": "ValueError", "message": "limit must be an integer"}

    params = {"query": query.strip(), "tags": "story", "hitsPerPage": limit}
    try:
        resp = requests.get(API_URL, params=params, timeout=15)
        resp.raise_for_status()
        hits = resp.json().get("hits", []) or []
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}

    items = []
    for hit in hits[:limit]:
        story_id = hit.get("objectID")
        discussion = f"https://news.ycombinator.com/item?id={story_id}" if story_id else ""
        items.append({
            "title": hit.get("title") or "",
            "url": hit.get("url") or discussion,
            "discussion_url": discussion,
            "source": "Hacker News",
            "summary": f"{hit.get('points') or 0} points · {hit.get('num_comments') or 0} comments",
            "created_at": hit.get("created_at") or "",
        })
    return {"query": query.strip(), "items": items, "count": len(items)}
