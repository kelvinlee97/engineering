"""Aggregate configured RSS/Atom feeds into one deduplicated Markdown digest."""

from rss_digest.models import Entry, FeedSource, FetchOutcome

__all__ = ["Entry", "FeedSource", "FetchOutcome"]
