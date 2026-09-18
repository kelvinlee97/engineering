"""Parsing covers both feed dialects and the date formats they use."""

from __future__ import annotations

import pytest

from rss_digest.models import FeedSource
from rss_digest.parse import ParseError, clean, parse_date, parse_feed

SOURCE = FeedSource(name="example", url="https://example.com/feed", topic="infra")

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>Example</title>
  <item>
    <title>Older post</title>
    <link>https://example.com/1</link>
    <guid>tag:example,1</guid>
    <description>&lt;p&gt;First   body&lt;/p&gt;</description>
    <pubDate>Mon, 01 Sep 2025 10:00:00 +0000</pubDate>
  </item>
  <item>
    <title>Newer post</title>
    <link>https://example.com/2</link>
    <pubDate>Tue, 02 Sep 2025 10:00:00 +0000</pubDate>
  </item>
</channel></rss>
"""

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Atom post</title>
    <link rel="edit" href="https://example.com/edit"/>
    <link rel="alternate" href="https://example.com/atom-1"/>
    <id>urn:uuid:1</id>
    <updated>2025-09-03T08:30:00Z</updated>
    <summary>Atom summary</summary>
  </entry>
</feed>
"""


def test_rss_entries_are_normalised_newest_first() -> None:
    entries = parse_feed(RSS, SOURCE)
    assert [entry.title for entry in entries] == ["Newer post", "Older post"]
    older = entries[1]
    assert older.link == "https://example.com/1"
    assert older.guid == "tag:example,1"
    assert older.summary == "First body"
    assert older.topic == "infra"


def test_atom_prefers_the_alternate_link() -> None:
    (entry,) = parse_feed(ATOM, SOURCE)
    assert entry.link == "https://example.com/atom-1"
    assert entry.guid == "urn:uuid:1"
    assert entry.published is not None
    assert entry.published.hour == 8


def test_missing_guid_falls_back_to_the_link_for_identity() -> None:
    entries = parse_feed(RSS, SOURCE)
    assert entries[0].guid == "https://example.com/2"
    assert entries[0].key != entries[1].key


@pytest.mark.parametrize(
    "raw",
    ["Mon, 01 Sep 2025 10:00:00 +0000", "2025-09-01T10:00:00Z", "2025-09-01T18:00:00+08:00"],
)
def test_parse_date_returns_utc(raw: str) -> None:
    parsed = parse_date(raw)
    assert parsed is not None
    assert parsed.utcoffset() is not None
    assert parsed.utcoffset().total_seconds() == 0  # type: ignore[union-attr]


def test_parse_date_rejects_garbage() -> None:
    assert parse_date("not a date") is None
    assert parse_date("") is None


def test_clean_truncates_long_bodies() -> None:
    assert clean("x" * 500, limit=10).endswith("…")


def test_malformed_and_empty_documents_raise() -> None:
    with pytest.raises(ParseError):
        parse_feed("<rss><channel>", SOURCE)
    with pytest.raises(ParseError):
        parse_feed("<rss version='2.0'><channel/></rss>", SOURCE)
