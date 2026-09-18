"""Data structures shared by fetching, parsing and rendering."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class FeedSource:
    """One configured feed: where to read it and how to label what it produces."""

    name: str
    url: str
    topic: str = "general"
    limit: int = 10
    include: tuple[str, ...] = ()
    exclude: tuple[str, ...] = ()


@dataclass(frozen=True)
class Entry:
    """One item from a feed, normalised across RSS 2.0 and Atom."""

    source: str
    topic: str
    title: str
    link: str
    published: datetime | None
    summary: str
    guid: str

    @property
    def key(self) -> str:
        """Stable identity used for cross-run deduplication."""

        basis = self.guid or self.link or f"{self.source}:{self.title}"
        return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


@dataclass
class FetchOutcome:
    """Result of reading one source, including the failure and not-modified paths."""

    source: FeedSource
    status: str
    entries: list[Entry] = field(default_factory=list)
    etag: str | None = None
    last_modified: str | None = None
    error: str | None = None
