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
import requests

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


# ---------------- YOUR NEW TOOL(S): github_repo ----------------

def test_github_repo_zero_releases_fetches_repo_only_and_maps_fields(monkeypatch, fake_http) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    calls = fake_http(FakeResponse({
        "full_name": "openai/whisper",
        "html_url": "https://github.com/openai/whisper",
        "description": "Robust Speech Recognition",
        "stargazers_count": 75000,
        "forks_count": 9000,
        "language": "Python",
        "license": {"spdx_id": "MIT", "name": "MIT License"},
        "pushed_at": "2026-11-01T10:00:00Z",
    }))

    result = TOOL_FUNCTIONS["github_repo"](repo="openai/whisper", max_releases=0)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://api.github.com/repos/openai/whisper"
    assert calls[0]["headers"]["Accept"] == "application/vnd.github+json"
    assert "Authorization" not in calls[0]["headers"]
    assert result["tool"] == "github_repo"
    assert result["repo"] == "openai/whisper"
    assert result["stars"] == 75000
    assert result["forks"] == 9000
    assert result["language"] == "Python"
    assert result["license"] == "MIT"
    assert result["pushed_at"] == "2026-11-01T10:00:00Z"
    assert result["releases"] == []
    assert result["items"][0]["source"] == "github.com"


def test_github_repo_with_max_releases_fetches_releases_and_handles_null_license(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test_token")
    calls: list[dict] = []

    def fake_get(url: str, **kwargs):
        calls.append({"url": url, **kwargs})
        if url.endswith("/releases"):
            return FakeResponse([
                {
                    "tag_name": "v20240930",
                    "name": "v20240930",
                    "published_at": "2024-09-30T00:00:00Z",
                    "html_url": "https://github.com/openai/whisper/releases/tag/v20240930",
                    "prerelease": False,
                },
                {
                    "tag_name": "v20231117",
                    "name": "v20231117",
                    "published_at": "2023-11-17T00:00:00Z",
                    "html_url": "https://github.com/openai/whisper/releases/tag/v20231117",
                    "prerelease": False,
                },
            ])
        return FakeResponse({
            "full_name": "openai/whisper",
            "html_url": "https://github.com/openai/whisper",
            "description": None,
            "stargazers_count": 100,
            "forks_count": 20,
            "language": "Python",
            "license": None,
            "pushed_at": "2026-11-02T12:00:00Z",
        })

    monkeypatch.setattr(requests, "get", fake_get)

    result = TOOL_FUNCTIONS["github_repo"](repo="openai/whisper", max_releases=2)

    assert len(calls) == 2
    assert calls[0]["url"] == "https://api.github.com/repos/openai/whisper"
    assert calls[0]["headers"]["Authorization"] == "Bearer ghp_test_token"
    assert calls[1]["url"] == "https://api.github.com/repos/openai/whisper/releases"
    assert calls[1]["params"] == {"per_page": 2}
    assert result["license"] is None
    assert len(result["releases"]) == 2
    assert result["releases"][0]["tag_name"] == "v20240930"
    assert "Latest release: v20240930" in result["items"][0]["summary"]


@pytest.mark.parametrize(
    "bad_repo",
    [
        "",
        "   ",
        "https://github.com/openai/whisper",
        "github.com/openai/whisper",
        "@openai/whisper",
        "openai/whisper.git",
        "openai",
        "a/b/c",
        123,
    ],
)
def test_github_repo_rejects_invalid_repo_without_network_call(fake_http, bad_repo) -> None:
    calls = fake_http(FakeResponse({}))
    result = TOOL_FUNCTIONS["github_repo"](repo=bad_repo, max_releases=3)

    assert result["tool"] == "github_repo"
    assert result["error"] == "ValueError"
    assert calls == []


@pytest.mark.parametrize("bad_limit", [-1, 11, "3", True, None, 1.5])
def test_github_repo_rejects_invalid_max_releases_without_network_call(fake_http, bad_limit) -> None:
    calls = fake_http(FakeResponse({}))
    result = TOOL_FUNCTIONS["github_repo"](repo="openai/whisper", max_releases=bad_limit)

    assert result["tool"] == "github_repo"
    assert result["error"] == "ValueError"
    assert calls == []


@pytest.mark.parametrize(
    ("mock_outcome", "expected_error"),
    [
        (FakeResponse(status_code=404), "HTTPError"),
        (FakeResponse(status_code=403), "HTTPError"),
        (requests.Timeout("request timed out"), "Timeout"),
    ],
)
def test_github_repo_http_error_or_timeout_returns_error_dict(fake_http, mock_outcome, expected_error) -> None:
    fake_http(mock_outcome)
    result = TOOL_FUNCTIONS["github_repo"](repo="openai/whisper", max_releases=0)

    assert result["tool"] == "github_repo"
    assert result["error"] == expected_error
    assert result["message"]

