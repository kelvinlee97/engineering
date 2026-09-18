"""End-to-end CLI behaviour against a local feed file."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rss_digest import cli

FEED = """<?xml version="1.0"?>
<rss version="2.0"><channel><item>
  <title>Post one</title><link>https://example.com/1</link>
  <description>EKS networking note</description>
</item></channel></rss>
"""


@pytest.fixture()
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "feeds.toml").write_text(
        '[[feeds]]\nname = "example"\nurl = "https://example.com/feed"\ntopic = "infra"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(cli, "fetch_source", _reader(FEED))
    return tmp_path


def _reader(document: str, status: int = 200):  # type: ignore[no-untyped-def]
    from rss_digest.fetch import fetch_source as real

    def patched(source, etag=None, last_modified=None, reader=None):  # type: ignore[no-untyped-def]
        return real(source, etag, last_modified, lambda *_: (status, document, {"etag": '"v1"'}))

    return patched


def run(workspace: Path, *extra: str) -> int:
    return cli.main(
        [
            "--config",
            str(workspace / "feeds.toml"),
            "--state",
            str(workspace / "state.json"),
            "--days",
            "0",
            *extra,
        ]
    )


def test_run_writes_a_digest_and_dedupes_the_second_run(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(workspace) == 0
    first = capsys.readouterr().out
    assert "Post one" in first
    assert "EKS networking note" in first

    assert run(workspace) == 0
    assert "No new items in this window." in capsys.readouterr().out


def test_all_flag_ignores_the_seen_ledger(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run(workspace)
    capsys.readouterr()
    run(workspace, "--all")
    assert "Post one" in capsys.readouterr().out


def test_dry_run_leaves_no_state_behind(workspace: Path) -> None:
    run(workspace, "--dry-run")
    assert not (workspace / "state.json").exists()


def test_output_file_and_json_format(workspace: Path) -> None:
    target = workspace / "out" / "digest.json"
    assert run(workspace, "--format", "json", "--output", str(target)) == 0
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["entries"][0]["title"] == "Post one"
    assert payload["sources"][0]["status"] == "ok"


def test_bad_configuration_exits_two(tmp_path: Path) -> None:
    (tmp_path / "feeds.toml").write_text("feeds = []\n", encoding="utf-8")
    assert cli.main(["--config", str(tmp_path / "feeds.toml")]) == 2


def test_every_source_failing_exits_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "feeds.toml").write_text(
        '[[feeds]]\nname = "example"\nurl = "https://example.com/feed"\n', encoding="utf-8"
    )
    monkeypatch.setattr(cli, "fetch_source", _reader("", status=500))
    assert run(tmp_path) == 1
    assert "warning: example: HTTP 500" in capsys.readouterr().err
