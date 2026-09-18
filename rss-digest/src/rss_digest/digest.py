"""Filter, deduplicate and render collected entries."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from rss_digest.models import Entry, FeedSource, FetchOutcome


def matches_filters(entry: Entry, source: FeedSource) -> bool:
    """Keyword gate: every include list is an OR, every exclude match drops the entry."""

    haystack = f"{entry.title}\n{entry.summary}".lower()
    if source.include and not any(word in haystack for word in source.include):
        return False
    return not any(word in haystack for word in source.exclude)


def select(
    outcomes: list[FetchOutcome],
    *,
    since: datetime | None = None,
    is_new: Callable[[str], bool] | None = None,
) -> list[Entry]:
    """Apply per-source filters, the age window, the dedup check, and the per-source limit."""

    selected: list[Entry] = []
    for outcome in outcomes:
        kept = 0
        for entry in outcome.entries:
            if kept >= outcome.source.limit:
                break
            if not matches_filters(entry, outcome.source):
                continue
            if since and entry.published and entry.published < since:
                continue
            if is_new is not None and not is_new(entry.key):
                continue
            selected.append(entry)
            kept += 1
    selected.sort(
        key=lambda entry: entry.published or datetime.min.replace(tzinfo=UTC), reverse=True
    )
    return selected


def window_start(days: int, now: datetime | None = None) -> datetime | None:
    """Start of the age window, or None when the run is unbounded."""

    if days <= 0:
        return None
    return (now or datetime.now(UTC)) - timedelta(days=days)


def _stamp(entry: Entry) -> str:
    return entry.published.strftime("%Y-%m-%d %H:%M UTC") if entry.published else "undated"


def render_markdown(
    entries: list[Entry], outcomes: list[FetchOutcome], generated: datetime | None = None
) -> str:
    """One digest: a run header, entries grouped by topic then source, then a source ledger."""

    moment = (generated or datetime.now(UTC)).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# RSS digest — {moment}", ""]
    ok = sum(1 for outcome in outcomes if outcome.status == "ok")
    lines.append(f"> {len(entries)} new items from {ok}/{len(outcomes)} readable sources.")
    lines.append("")

    if not entries:
        lines.append("No new items in this window.")
        lines.append("")
    else:
        by_topic: dict[str, dict[str, list[Entry]]] = defaultdict(lambda: defaultdict(list))
        for entry in entries:
            by_topic[entry.topic][entry.source].append(entry)
        for topic in sorted(by_topic):
            lines.append(f"## {topic}")
            lines.append("")
            for source in sorted(by_topic[topic]):
                lines.append(f"### {source}")
                lines.append("")
                for entry in by_topic[topic][source]:
                    title = entry.title.replace("[", "\\[").replace("]", "\\]")
                    heading = f"- **[{title}]({entry.link})** — {_stamp(entry)}"
                    lines.append(heading if entry.link else f"- **{title}** — {_stamp(entry)}")
                    if entry.summary:
                        lines.append(f"  - {entry.summary}")
                lines.append("")

    lines.append("## Source status")
    lines.append("")
    lines.append("| Source | Status | Items | Note |")
    lines.append("| --- | --- | --- | --- |")
    counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        counts[entry.source] += 1
    for outcome in outcomes:
        note = outcome.error or ""
        lines.append(
            f"| {outcome.source.name} | {outcome.status} | {counts[outcome.source.name]} | {note} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_json(entries: list[Entry], outcomes: list[FetchOutcome]) -> str:
    """Machine-readable form of the same run, for piping into another tool."""

    payload = {
        "entries": [
            {
                "source": entry.source,
                "topic": entry.topic,
                "title": entry.title,
                "link": entry.link,
                "published": entry.published.isoformat() if entry.published else None,
                "summary": entry.summary,
                "key": entry.key,
            }
            for entry in entries
        ],
        "sources": [
            {"name": outcome.source.name, "status": outcome.status, "error": outcome.error}
            for outcome in outcomes
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
