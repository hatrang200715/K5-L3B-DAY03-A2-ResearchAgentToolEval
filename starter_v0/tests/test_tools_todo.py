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

clarify_tool = TOOL_FUNCTIONS["clarify"]
format_tool = TOOL_FUNCTIONS["format"]
send_tool = TOOL_FUNCTIONS["send"]
lookup_tool = TOOL_FUNCTIONS["lookup"]
fetch_tool = TOOL_FUNCTIONS["fetch"]
timeline_tool = TOOL_FUNCTIONS["timeline"]
social_search_tool = TOOL_FUNCTIONS["social_search"]
policy_tool = TOOL_FUNCTIONS["policy"]


def test_clarify_choice_returns_options_and_awaits_user() -> None:
    options = ["Sam Altman", "Elon Musk"]
    result = clarify_tool(question="Bạn muốn xem tweet của ai?", response_type="choice", options=options)

    assert result["options"] == ["Sam Altman", "Elon Musk"]
    assert result["response_type"] == "choice"
    assert result["question"] == "Bạn muốn xem tweet của ai?"
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "a1", "url": "https://a.com/1", "section": "A"},
        {"title": "b1", "url": "https://b.com/1", "section": "B"},
        {"title": "a2", "url": "https://a.com/2", "section": "A"},
    ]
    markdown = format_tool(items=items, template="sections")["markdown"]

    assert markdown.count("## A") == 1
    assert markdown.count("## B") == 1
    # Both A items sit under the single "## A" heading, before "## B".
    assert markdown.index("a1") < markdown.index("a2") < markdown.index("## B")


def test_format_thread_numbers_items() -> None:
    items = [{"title": f"Tin {i}", "url": f"https://example.com/{i}"} for i in range(3)]
    lines = format_tool(items=items, template="thread")["markdown"].split("\n\n")

    assert [line[:2] for line in lines] == ["1/", "2/", "3/"]
    assert lines[0].startswith("1/ Tin 0")


@pytest.mark.parametrize("items", [None, []])
def test_format_empty_items_does_not_crash(items) -> None:
    result = format_tool(items=items, template="sections")

    assert result["item_count"] == 0
    assert result["markdown"] == ""


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="Bản tin AI", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert calls[0]["url"] == "https://api.telegram.org/botbot-token/sendMessage"
    assert calls[0]["json"]["chat_id"] == "-100123"
    assert calls[0]["json"]["text"] == "Bản tin AI"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="Bản tin AI", confirmed=True)

    assert calls == []
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    result = lookup_tool(query="AI", topic="news", timeframe=None)

    assert "time_range" not in calls[0]["json"]
    assert calls[0]["json"]["query"] == "AI"
    assert calls[0]["json"]["topic"] == "news"
    assert result["items"] == []


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    calls = fake_http(FakeResponse({"data": {
        "markdown": "# Hello\nBody",
        "metadata": {"title": "T", "sourceURL": "https://www.example.com/post"},
    }}))

    result = fetch_tool(url="https://www.example.com/post")

    assert calls[0]["url"] == "https://api.firecrawl.dev/v1/scrape"
    assert calls[0]["json"] == {"url": "https://www.example.com/post", "formats": ["markdown"]}
    assert calls[0]["headers"]["Authorization"] == "Bearer fc-test"
    assert result["items"][0] == {
        "title": "T",
        "url": "https://www.example.com/post",
        "source": "example.com",
        "summary": "# Hello\nBody",
    }


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000, "metadata": {}}}))

    summary = fetch_tool(url="https://example.com")["items"][0]["summary"]

    assert len(summary) == 4000


# ---------------- timeline / social_search ----------------

def _raw_tweets(n: int, handle: str = "sama") -> list[dict]:
    return [{"tweet_id": str(100 + i), "screen_name": handle, "text": f"tweet {i}"} for i in range(n)]


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rk")
    raw = [{"screen_name": "sama", "text": "no id"}] + _raw_tweets(6)
    calls = fake_http(FakeResponse({"timeline": raw}))

    result = timeline_tool(screenname="sama", limit=3)

    assert calls[0]["params"] == {"screenname": "sama"}
    assert len(result["items"]) == 3
    assert [item["url"] for item in result["items"]] == [
        "https://x.com/sama/status/100",
        "https://x.com/sama/status/101",
        "https://x.com/sama/status/102",
    ]


@pytest.mark.parametrize("search_type", ["Top", "Latest"])
def test_social_search_passes_search_type(monkeypatch, fake_http, search_type) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rk")
    calls = fake_http(FakeResponse({"timeline": []}))

    result = social_search_tool(query="OpenAI", search_type=search_type)

    assert calls[0]["url"].endswith("/search.php")
    assert calls[0]["params"] == {"query": "OpenAI", "search_type": search_type}
    assert calls[0]["headers"]["x-rapidapi-key"] == "rk"
    assert result["search_type"] == search_type


# ---------------- policy (local knowledge + trust boundary) ----------------

@pytest.mark.parametrize("query", ["", "   ", "là gì"])
def test_policy_empty_query_returns_no_results(query) -> None:
    # "là gì" folds to stopwords only, so it has no search terms either.
    result = policy_tool(query=query)

    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = policy_tool(query="data API key transcript", policy_area="data_privacy", top_k=5)

    assert result["results"], "expected at least one data_privacy section"
    assert {hit["policy_area"] for hit in result["results"]} == {"data_privacy"}


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = policy_tool(query="injection probe citation", policy_area="source_citation", top_k=5)

    probe = [hit for hit in result["results"] if hit["section"] == "Injection probe"]
    assert len(probe) == 1
    untrusted = " ".join(probe[0]["untrusted_text"])
    assert "ignore the citation policy" in untrusted
    assert "ignore the citation policy" not in probe[0]["facts"]
    assert "untrusted" in result["trust_boundary"]


# ---------------- Regression tests: bugs found in existing tools (C, bug hunt) ----------------
# Each test failed on the original starter code and passes after the fix.

@pytest.mark.parametrize("confirmed", ["false", "no", "true", 1])
def test_send_non_boolean_confirmed_does_not_send(monkeypatch, fake_http, confirmed) -> None:
    # Bug 1: `if not confirmed` let the truthy string "false" through and posted to Telegram.
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="Bản tin", confirmed=confirmed)

    assert calls == []
    assert result["status"] == "needs_confirmation"


def test_format_skips_non_dict_items_instead_of_raising() -> None:
    # Bug 2: items=["a", ...] raised AttributeError ('str' has no .get) instead of returning a dict.
    result = format_tool(items=["plain string", {"title": "Tin thật", "url": "https://a.com"}], template="bullets")

    assert result["item_count"] == 1
    assert result["markdown"] == "- Tin thật - [a.com](https://a.com)"


def test_format_item_without_source_has_no_dangling_dash() -> None:
    # Bug 3: an item with no url/source rendered as "- T - " with a trailing separator.
    markdown = format_tool(items=[{"title": "T"}], template="bullets")["markdown"]

    assert markdown == "- T"


@pytest.mark.parametrize("tool_name, kwargs", [
    ("timeline", {"screenname": "sama"}),
    ("social_search", {"query": "AI"}),
])
def test_tweet_tools_negative_limit_falls_back_to_default(monkeypatch, fake_http, tool_name, kwargs) -> None:
    # Bug 4: limit=-1 became items[:-1], returning all but one tweet (19 of 20).
    monkeypatch.setenv("RAPIDAPI_KEY", "rk")
    fake_http(FakeResponse({"timeline": _raw_tweets(20)}))

    result = TOOL_FUNCTIONS[tool_name](limit=-1, **kwargs)

    assert len(result["items"]) == 5


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
