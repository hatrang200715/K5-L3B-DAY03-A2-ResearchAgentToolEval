from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    """Normalize a URL so trivially different links compare equal."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith("utm_")])
    path = parts.path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), host, path, query, ""))


def dedupe_items(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Remove items that point to the same URL (or, without URL, the same title). Keeps first occurrence."""
    if items is None:
        items = []
    if not isinstance(items, list):
        return {"error": "ValueError", "message": "items must be a list of objects"}

    seen: set[str] = set()
    kept: list[dict[str, Any]] = []
    skipped_invalid = 0
    for item in items:
        if not isinstance(item, dict):
            skipped_invalid += 1
            continue
        url = item.get("url")
        if isinstance(url, str) and url.strip():
            key = "url:" + normalize_url(url)
        else:
            title = str(item.get("title") or "").strip().lower()
            if not title:
                kept.append(item)  # nothing to compare on: keep it
                continue
            key = "title:" + title
        if key in seen:
            continue
        seen.add(key)
        kept.append(item)

    return {
        "items": kept,
        "count": len(kept),
        "removed": len(items) - len(kept) - skipped_invalid,
        "skipped_invalid": skipped_invalid,
    }
