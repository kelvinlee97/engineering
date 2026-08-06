from __future__ import annotations

import json
from pathlib import Path

import pytest

from yt_transcript import cli
from yt_transcript.models import CaptureStatus, ExtractionReport, VideoProbe


def test_probe_prints_structured_result(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cli,
        "probe_video",
        lambda _: VideoProbe("JJyLynh5d6M", "Example", "Channel", 60, [], None),
    )

    exit_code = cli.main(["probe", "https://youtu.be/JJyLynh5d6M"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "blocked"


def test_capture_uses_status_as_exit_contract(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cli,
        "capture_video",
        lambda _url, _output: ExtractionReport(CaptureStatus.COMPLETE),
    )

    exit_code = cli.main(["capture", "https://youtu.be/JJyLynh5d6M", "--output", str(tmp_path)])

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out)["status"] == "complete"


def test_validate_summaries_rejects_invalid_pair(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    english = tmp_path / "summary.en.md"
    chinese = tmp_path / "summary.zh.md"
    evidence = tmp_path / "evidence.json"
    for path in (english, chinese, evidence):
        path.write_text("placeholder", encoding="utf-8")
    monkeypatch.setattr(cli, "load_evidence", lambda _: object())
    monkeypatch.setattr(cli, "validate_summary_pair", lambda *_: ["citations do not match"])

    exit_code = cli.main(["validate-summaries", str(evidence), str(english), str(chinese)])

    assert exit_code == 2
    assert json.loads(capsys.readouterr().out)["errors"] == ["citations do not match"]


def test_archive_prints_the_final_capture_directory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / ".staging" / "JJyLynh5d6M"
    target = tmp_path / "startup" / "how-to-start--JJyLynh5d6M"
    monkeypatch.setattr(cli, "archive_capture", lambda *_args, **_kwargs: target)

    exit_code = cli.main(
        [
            "archive",
            str(source),
            "--topic",
            "startup",
            "--reason",
            "The video teaches startup validation.",
            "--tag",
            "product-market-fit",
        ]
    )

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out) == {
        "status": "complete",
        "capture_dir": str(target),
    }
