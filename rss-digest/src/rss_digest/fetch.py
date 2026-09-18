"""Read feed documents over HTTP with conditional requests."""

from __future__ import annotations

import urllib.error
import urllib.request
from collections.abc import Callable

from rss_digest.models import FeedSource, FetchOutcome
from rss_digest.parse import ParseError, parse_feed

USER_AGENT = "rss-digest/0.1 (+https://github.com/kelvinlee97/engineering)"
TIMEOUT_SECONDS = 20
MAX_BYTES = 8 * 1024 * 1024

Reader = Callable[[FeedSource, str | None, str | None], tuple[int, str, dict[str, str]]]


def http_reader(
    source: FeedSource, etag: str | None, last_modified: str | None
) -> tuple[int, str, dict[str, str]]:
    """Fetch one feed, returning (status, body, response headers)."""

    request = urllib.request.Request(source.url, headers={"User-Agent": USER_AGENT})
    if etag:
        request.add_header("If-None-Match", etag)
    if last_modified:
        request.add_header("If-Modified-Since", last_modified)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read(MAX_BYTES)
            headers = {key.lower(): value for key, value in response.headers.items()}
            charset = response.headers.get_content_charset() or "utf-8"
            return response.status, raw.decode(charset, errors="replace"), headers
    except urllib.error.HTTPError as error:
        if error.code == 304:
            return 304, "", {key.lower(): value for key, value in error.headers.items()}
        raise


def fetch_source(
    source: FeedSource,
    etag: str | None = None,
    last_modified: str | None = None,
    reader: Reader = http_reader,
) -> FetchOutcome:
    """Fetch and parse one source; network and parse failures become outcomes, not raises."""

    try:
        status, body, headers = reader(source, etag, last_modified)
    except (urllib.error.URLError, OSError, ValueError) as error:
        return FetchOutcome(source=source, status="error", error=str(error))

    if status == 304:
        return FetchOutcome(
            source=source, status="not-modified", etag=etag, last_modified=last_modified
        )
    if status != 200:
        return FetchOutcome(source=source, status="error", error=f"HTTP {status}")

    try:
        entries = parse_feed(body, source)
    except ParseError as error:
        return FetchOutcome(source=source, status="error", error=str(error))

    return FetchOutcome(
        source=source,
        status="ok",
        entries=entries,
        etag=headers.get("etag"),
        last_modified=headers.get("last-modified"),
    )
