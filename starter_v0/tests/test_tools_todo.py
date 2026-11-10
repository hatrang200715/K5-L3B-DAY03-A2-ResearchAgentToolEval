"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

# ---- hn_search (live API, mocked) ----

def test_hn_search_sends_query_and_maps_hits(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": [
        {"title": "Agents 101", "url": "https://a.dev/agents", "points": 120, "num_comments": 30, "objectID": "1"},
        {"title": "Ask HN: agents?", "url": None, "points": 5, "num_comments": 2, "objectID": "2"},
    ]}))
    result = TOOL_FUNCTIONS["hn_search"](query="  LLM agents ", limit=2)

    assert len(calls) == 1
    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search"
    assert calls[0]["params"] == {"query": "LLM agents", "tags": "story", "hitsPerPage": 2}
    assert result["count"] == 2
    assert result["items"][0]["url"] == "https://a.dev/agents"
    assert result["items"][0]["summary"] == "120 points · 30 comments"
    # story without an external url falls back to the HN discussion page
    assert result["items"][1]["url"] == "https://news.ycombinator.com/item?id=2"


def test_hn_search_empty_query_returns_error_without_network(fake_http) -> None:
    calls = fake_http(FakeResponse({}))
    for bad in ("", "   ", None, 123):
        result = TOOL_FUNCTIONS["hn_search"](query=bad)
        assert result["error"] == "ValueError"
    assert calls == []


def test_hn_search_limit_string_and_out_of_range_are_clamped(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))
    TOOL_FUNCTIONS["hn_search"](query="AI", limit="5")
    TOOL_FUNCTIONS["hn_search"](query="AI", limit=0)
    TOOL_FUNCTIONS["hn_search"](query="AI", limit=999)
    assert [c["params"]["hitsPerPage"] for c in calls] == [5, 1, 20]
    result = TOOL_FUNCTIONS["hn_search"](query="AI", limit="many")
    assert result["error"] == "ValueError"
    assert len(calls) == 3


def test_hn_search_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=429))
    result = TOOL_FUNCTIONS["hn_search"](query="AI")
    assert result["error"] == "HTTPError"
    assert "429" in result["message"]
    assert "items" not in result


def test_hn_search_timeout_returns_error_dict(fake_http) -> None:
    import requests

    fake_http(requests.Timeout("timed out"))
    result = TOOL_FUNCTIONS["hn_search"](query="AI")
    assert result == {"error": "Timeout", "message": "timed out"}


# ---- reading_time (local) ----

def test_reading_time_counts_words_and_rounds_minutes_up() -> None:
    result = TOOL_FUNCTIONS["reading_time"](text="một hai ba " * 150)  # 450 words
    assert result["word_count"] == 450
    assert result["words_per_minute"] == 200
    assert result["minutes"] == 3  # 450 / 200 = 2.25 -> 3


def test_reading_time_short_text_is_at_least_one_minute() -> None:
    result = TOOL_FUNCTIONS["reading_time"](text="Hello world", words_per_minute="100")
    assert result["word_count"] == 2
    assert result["minutes"] == 1


def test_reading_time_bad_input_returns_error_dict() -> None:
    assert TOOL_FUNCTIONS["reading_time"](text="")["error"] == "ValueError"
    assert TOOL_FUNCTIONS["reading_time"](text=None)["error"] == "ValueError"
    assert TOOL_FUNCTIONS["reading_time"](text="abc", words_per_minute=0)["error"] == "ValueError"
    assert TOOL_FUNCTIONS["reading_time"](text="abc", words_per_minute="fast")["error"] == "ValueError"


# ---- extract_links (local) ----

def test_extract_links_keeps_order_dedupes_and_strips_punctuation() -> None:
    text = "Đọc https://a.dev/x, rồi http://b.io/y. Xem lại https://a.dev/x!"
    result = TOOL_FUNCTIONS["extract_links"](text=text)
    assert result == {"links": ["https://a.dev/x", "http://b.io/y"], "count": 2}


def test_extract_links_respects_limit_and_handles_no_links() -> None:
    text = " ".join(f"https://site{i}.com" for i in range(10))
    assert TOOL_FUNCTIONS["extract_links"](text=text, limit=3)["count"] == 3
    assert TOOL_FUNCTIONS["extract_links"](text="không có link nào")["links"] == []


def test_extract_links_bad_input_returns_error_dict() -> None:
    assert TOOL_FUNCTIONS["extract_links"](text=None)["error"] == "ValueError"
    assert TOOL_FUNCTIONS["extract_links"](text=["https://a.dev"])["error"] == "ValueError"
    assert TOOL_FUNCTIONS["extract_links"](text="https://a.dev", limit="x")["error"] == "ValueError"


# ---- dedupe_items (local) ----

def test_dedupe_items_removes_same_url_after_normalization() -> None:
    items = [
        {"title": "A", "url": "https://www.Example.com/post/?utm_source=x#top"},
        {"title": "A copy", "url": "https://example.com/post"},
        {"title": "B", "url": "https://example.com/other"},
    ]
    result = TOOL_FUNCTIONS["dedupe_items"](items=items)
    assert [item["title"] for item in result["items"]] == ["A", "B"]
    assert result["removed"] == 1


def test_dedupe_items_without_url_compares_title_and_keeps_unidentifiable() -> None:
    items = [{"title": "Same"}, {"title": "same "}, {"summary": "no url, no title"}]
    result = TOOL_FUNCTIONS["dedupe_items"](items=items)
    assert result["items"] == [{"title": "Same"}, {"summary": "no url, no title"}]
    assert result["removed"] == 1


def test_dedupe_items_bad_input_returns_error_dict_or_skips() -> None:
    assert TOOL_FUNCTIONS["dedupe_items"](items="not a list")["error"] == "ValueError"
    assert TOOL_FUNCTIONS["dedupe_items"](items=None)["count"] == 0
    result = TOOL_FUNCTIONS["dedupe_items"](items=[{"url": "https://a.dev"}, "junk", 42])
    assert result["count"] == 1
    assert result["skipped_invalid"] == 2
    assert result["removed"] == 0
