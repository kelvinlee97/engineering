"""Load the feed list from a TOML file."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from rss_digest.models import FeedSource

DEFAULT_LIMIT = 10


class ConfigError(ValueError):
    """The configuration file is missing required fields or has the wrong shape."""


def _strings(raw: Any, field: str, name: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ConfigError(f"feed {name!r}: {field} must be a list of strings")
    return tuple(item.strip().lower() for item in raw if item.strip())


def parse_config(data: dict[str, Any]) -> list[FeedSource]:
    """Turn parsed TOML into feed sources, failing loudly on a malformed entry."""

    raw_feeds = data.get("feeds")
    if not isinstance(raw_feeds, list) or not raw_feeds:
        raise ConfigError("configuration needs a non-empty [[feeds]] array")

    default_limit = data.get("limit", DEFAULT_LIMIT)
    if not isinstance(default_limit, int) or default_limit < 1:
        raise ConfigError("limit must be a positive integer")

    sources: list[FeedSource] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_feeds, start=1):
        if not isinstance(raw, dict):
            raise ConfigError(f"feed #{index} must be a table")
        url = raw.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise ConfigError(f"feed #{index} needs an http(s) url")
        name = raw.get("name") or url
        if not isinstance(name, str):
            raise ConfigError(f"feed #{index}: name must be a string")
        if name in seen:
            raise ConfigError(f"duplicate feed name {name!r}")
        seen.add(name)
        topic = raw.get("topic", "general")
        if not isinstance(topic, str):
            raise ConfigError(f"feed {name!r}: topic must be a string")
        limit = raw.get("limit", default_limit)
        if not isinstance(limit, int) or limit < 1:
            raise ConfigError(f"feed {name!r}: limit must be a positive integer")
        sources.append(
            FeedSource(
                name=name,
                url=url,
                topic=topic,
                limit=limit,
                include=_strings(raw.get("include"), "include", name),
                exclude=_strings(raw.get("exclude"), "exclude", name),
            )
        )
    return sources


def load_config(path: Path) -> list[FeedSource]:
    """Read and validate a feeds TOML file."""

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigError(f"configuration file not found: {path}") from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"{path} is not valid TOML: {error}") from error
    return parse_config(data)
