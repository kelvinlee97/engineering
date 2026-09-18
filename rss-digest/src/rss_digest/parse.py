"""Parse RSS 2.0 and Atom documents into normalised entries."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

from rss_digest.models import Entry, FeedSource

ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


class ParseError(ValueError):
    """The document is not well-formed XML, or carries no recognised feed items."""


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def clean(raw: str, limit: int = 400) -> str:
    """Strip markup and collapse whitespace so a summary stays one readable block."""

    text = WHITESPACE_RE.sub(" ", TAG_RE.sub(" ", raw)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def parse_date(raw: str) -> datetime | None:
    """Accept RFC 822 (RSS) and ISO 8601 (Atom); return an aware UTC datetime."""

    value = raw.strip()
    if not value:
        return None
    for parser in (parsedate_to_datetime, datetime.fromisoformat):
        try:
            parsed = parser(value.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
    return None


def _atom_link(item: ET.Element) -> str:
    fallback = ""
    for link in item.findall(f"{ATOM}link"):
        rel = link.get("rel", "alternate")
        href = link.get("href", "")
        if not href:
            continue
        if rel == "alternate":
            return href
        fallback = fallback or href
    return fallback


def _first(item: ET.Element, *paths: str) -> str:
    for path in paths:
        text = _text(item.find(path))
        if text:
            return text
    return ""


def parse_feed(document: str, source: FeedSource) -> list[Entry]:
    """Read one feed document into entries, newest first."""

    try:
        root = ET.fromstring(document)
    except ET.ParseError as error:
        raise ParseError(f"{source.name}: malformed XML ({error})") from error

    items = root.findall(".//item") or root.findall(f".//{ATOM}entry")
    if not items:
        raise ParseError(f"{source.name}: no <item> or <entry> elements found")

    entries: list[Entry] = []
    for item in items:
        title = _first(item, "title", f"{ATOM}title") or "(untitled)"
        link = _first(item, "link") or _atom_link(item)
        guid = _first(item, "guid", f"{ATOM}id") or link
        published = parse_date(
            _first(
                item,
                "pubDate",
                f"{DC}date",
                f"{ATOM}published",
                f"{ATOM}updated",
            )
        )
        summary = clean(
            _first(
                item,
                "description",
                f"{CONTENT}encoded",
                f"{ATOM}summary",
                f"{ATOM}content",
            )
        )
        entries.append(
            Entry(
                source=source.name,
                topic=source.topic,
                title=clean(title, limit=200),
                link=link,
                published=published,
                summary=summary,
                guid=guid,
            )
        )
    entries.sort(
        key=lambda entry: entry.published or datetime.min.replace(tzinfo=UTC), reverse=True
    )
    return entries
