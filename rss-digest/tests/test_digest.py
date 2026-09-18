"""Selection and rendering: filters, window, dedup, per-source limit."""

from __future__ import annotations

from datetime import UTC, datetime

from rss_digest.digest import matches_filters, render_json, render_markdown, select, window_start
from rss_digest.models import Entry, FeedSource, FetchOutcome

NOW = datetime(2025, 9, 10, tzinfo=UTC)


def entry(title: str, *, days_old: int = 0, source: str = "example", topic: str = "infra") -> Entry:
    return Entry(
        source=source,
        topic=topic,
        title=title,
        link=f"https://example.com/{title.lower().replace(' ', '-')}",
        published=NOW.replace(day=NOW.day - days_old),
        summary=f"about {title}",
        guid=title,
    )


def outcome(source: FeedSource, entries: list[Entry]) -> FetchOutcome:
    return FetchOutcome(source=source, status="ok", entries=entries)


def test_include_and_exclude_gate_entries() -> None:
    source = FeedSource(name="s", url="https://e/f", include=("eks",), exclude=("preview",))
    assert matches_filters(entry("EKS release"), source)
    assert not matches_filters(entry("VPC release"), source)
    assert not matches_filters(entry("EKS preview"), source)


def test_window_limit_and_dedup_are_applied_together() -> None:
    source = FeedSource(name="s", url="https://e/f", limit=2)
    entries = [entry("A"), entry("B"), entry("C"), entry("D", days_old=9)]
    seen = {entries[0].key}
    selected = select(
        [outcome(source, entries)],
        since=window_start(7, now=NOW),
        is_new=lambda key: key not in seen,
    )
    assert [item.title for item in selected] == ["B", "C"]


def test_zero_days_disables_the_window() -> None:
    assert window_start(0, now=NOW) is None


def test_markdown_groups_by_topic_and_lists_every_source() -> None:
    good = FeedSource(name="good", url="https://e/f", topic="infra")
    bad = FeedSource(name="bad", url="https://e/g", topic="industry")
    outcomes = [
        outcome(good, [entry("A")]),
        FetchOutcome(source=bad, status="error", error="HTTP 500"),
    ]
    text = render_markdown([entry("A")], outcomes, generated=NOW)
    assert "# RSS digest — 2025-09-10 00:00 UTC" in text
    assert "## infra" in text
    assert "### example" in text
    assert "| bad | error | 0 | HTTP 500 |" in text
    assert "1 new items from 1/2 readable sources." in text


def test_markdown_states_an_empty_run_explicitly() -> None:
    source = FeedSource(name="s", url="https://e/f")
    assert "No new items in this window." in render_markdown([], [outcome(source, [])], NOW)


def test_json_output_carries_keys_and_source_status() -> None:
    source = FeedSource(name="s", url="https://e/f")
    payload = render_json([entry("A")], [outcome(source, [])])
    assert '"key"' in payload
    assert '"status": "ok"' in payload
