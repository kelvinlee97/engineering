"""The config loader fails loudly rather than silently dropping a feed."""

from __future__ import annotations

import pytest

from rss_digest.config import ConfigError, parse_config


def test_defaults_and_normalisation() -> None:
    (feed,) = parse_config(
        {"limit": 3, "feeds": [{"url": "https://example.com/feed", "include": ["EKS", " vpc "]}]}
    )
    assert feed.name == "https://example.com/feed"
    assert feed.topic == "general"
    assert feed.limit == 3
    assert feed.include == ("eks", "vpc")


@pytest.mark.parametrize(
    "data",
    [
        {"feeds": []},
        {"feeds": [{"url": "ftp://example.com/feed"}]},
        {"feeds": [{"url": "https://example.com/a", "limit": 0}]},
        {"feeds": [{"url": "https://example.com/a", "include": "eks"}]},
        {
            "feeds": [
                {"name": "dup", "url": "https://example.com/a"},
                {"name": "dup", "url": "https://example.com/b"},
            ]
        },
    ],
)
def test_malformed_configuration_is_rejected(data: dict[str, object]) -> None:
    with pytest.raises(ConfigError):
        parse_config(data)
