from __future__ import annotations

import re
from typing import Any

URL_RE = re.compile(r"https?://[^\s<>\"'()\[\]]+", re.IGNORECASE)
TRAILING_PUNCT = ".,;:!?"
MAX_LIMIT = 100


def extract_links(text: str = "", limit: int = 20) -> dict[str, Any]:
    """Extract unique http(s) URLs from a text, in order of appearance. Local, no network."""
    if not isinstance(text, str):
        return {"error": "ValueError", "message": "text must be a string"}
    try:
        limit = max(1, min(int(limit), MAX_LIMIT))
    except (TypeError, ValueError):
        return {"error": "ValueError", "message": "limit must be an integer"}

    links: list[str] = []
    for match in URL_RE.findall(text):
        url = match.rstrip(TRAILING_PUNCT)
        if url and url not in links:
            links.append(url)
        if len(links) >= limit:
            break
    return {"links": links, "count": len(links)}
