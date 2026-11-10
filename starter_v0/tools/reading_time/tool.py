from __future__ import annotations

import math
import re
from typing import Any

DEFAULT_WPM = 200


def reading_time(text: str = "", words_per_minute: int = DEFAULT_WPM) -> dict[str, Any]:
    """Count words and estimate reading time of a text. Local, no network."""
    if not isinstance(text, str) or not text.strip():
        return {"error": "ValueError", "message": "text is required"}
    try:
        wpm = int(words_per_minute)
    except (TypeError, ValueError):
        return {"error": "ValueError", "message": "words_per_minute must be an integer"}
    if wpm <= 0:
        return {"error": "ValueError", "message": "words_per_minute must be > 0"}

    word_count = len(re.findall(r"\w+", text))
    minutes = max(1, math.ceil(word_count / wpm)) if word_count else 0
    return {
        "word_count": word_count,
        "char_count": len(text),
        "words_per_minute": wpm,
        "minutes": minutes,
    }
