"""Fetching degrades to an outcome, and state keeps the next run incremental."""

from __future__ import annotations

import urllib.error
from pathlib import Path

from rss_digest.fetch import fetch_source
from rss_digest.models import FeedSource
from rss_digest.store import load_state, save_state

SOURCE = FeedSource(name="example", url="https://example.com/feed")
FEED = """<?xml version="1.0"?>
<rss version="2.0"><channel><item>
  <title>Post</title><link>https://example.com/1</link>
  <pubDate>Mon, 01 Sep 2025 10:00:00 +0000</pubDate>
</item></channel></rss>
"""


def test_conditional_headers_are_sent_and_304_keeps_validators() -> None:
    seen: dict[str, str | None] = {}

    def reader(
        source: FeedSource, etag: str | None, last_modified: str | None
    ) -> tuple[int, str, dict[str, str]]:
        seen["etag"] = etag
        seen["last_modified"] = last_modified
        return 304, "", {}

    result = fetch_source(SOURCE, etag='W/"abc"', last_modified="Mon, 01 Sep 2025", reader=reader)
    assert seen == {"etag": 'W/"abc"', "last_modified": "Mon, 01 Sep 2025"}
    assert result.status == "not-modified"
    assert result.entries == []
    assert result.etag == 'W/"abc"'


def test_success_captures_entries_and_new_validators() -> None:
    result = fetch_source(
        SOURCE, reader=lambda *_: (200, FEED, {"etag": '"v2"', "last-modified": "today"})
    )
    assert result.status == "ok"
    assert [entry.title for entry in result.entries] == ["Post"]
    assert result.etag == '"v2"'
    assert result.last_modified == "today"


def test_network_parse_and_status_failures_become_outcomes() -> None:
    def raiser(*_: object) -> tuple[int, str, dict[str, str]]:
        raise urllib.error.URLError("dns failure")

    assert fetch_source(SOURCE, reader=raiser).status == "error"
    assert fetch_source(SOURCE, reader=lambda *_: (500, "", {})).error == "HTTP 500"
    broken = fetch_source(SOURCE, reader=lambda *_: (200, "<rss>", {}))
    assert broken.status == "error"
    assert broken.error is not None


def test_state_round_trips_and_survives_a_corrupt_file(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "state.json"
    state = load_state(path)
    state.remember_validators("example", '"v1"', None)
    state.remember_keys(["a", "b", "a"])
    save_state(path, state)

    reloaded = load_state(path)
    assert reloaded.validators_for("example") == ('"v1"', None)
    assert reloaded.seen == ["a", "b"]
    assert reloaded.is_new("c")
    assert not reloaded.is_new("a")

    path.write_text("{ not json", encoding="utf-8")
    assert load_state(path).seen == []


def test_clearing_validators_drops_the_entry(tmp_path: Path) -> None:
    state = load_state(tmp_path / "state.json")
    state.remember_validators("example", '"v1"', None)
    state.remember_validators("example", None, None)
    assert state.validators_for("example") == (None, None)
