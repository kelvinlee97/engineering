"""Tests for validate_automation_config.py.

Run with: python3 -m pytest .github/scripts/test_validate_automation_config.py
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

import pytest

SCRIPT = pathlib.Path(__file__).with_name("validate_automation_config.py")
REPO = SCRIPT.parents[2]


def run(cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(cwd / ".github/scripts/validate_automation_config.py")],
        capture_output=True,
        text=True,
    )


@pytest.fixture
def repo(tmp_path: pathlib.Path) -> pathlib.Path:
    """A copy of the real .github tree, plus the directory dependabot expects."""
    shutil.copytree(REPO / ".github", tmp_path / ".github")
    (tmp_path / "youtube-transcript").mkdir()
    return tmp_path


def write_labels(repo: pathlib.Path, labels: list[dict[str, str]]) -> None:
    (repo / ".github/labels.json").write_text(json.dumps(labels), encoding="utf-8")


def test_the_real_config_passes() -> None:
    result = run(REPO)
    assert result.returncode == 0, result.stderr
    assert "ok:" in result.stdout


def test_copied_config_passes(repo: pathlib.Path) -> None:
    assert run(repo).returncode == 0


def test_duplicate_label_is_rejected(repo: pathlib.Path) -> None:
    labels = json.loads((repo / ".github/labels.json").read_text())
    labels.append(dict(labels[0]))
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "duplicate label" in result.stderr


def test_bad_colour_is_rejected(repo: pathlib.Path) -> None:
    labels = json.loads((repo / ".github/labels.json").read_text())
    labels[0]["color"] = "#FF0000"
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "6 lowercase hex digits" in result.stderr


def test_unknown_key_is_rejected(repo: pathlib.Path) -> None:
    labels = json.loads((repo / ".github/labels.json").read_text())
    labels[0]["colour"] = "ff0000"
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "unknown keys" in result.stderr


def test_label_used_by_labeler_must_exist(repo: pathlib.Path) -> None:
    labels = [x for x in json.loads((repo / ".github/labels.json").read_text())
              if x["name"] != "area: aws"]
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "labeler.yml uses 'area: aws'" in result.stderr


def test_label_used_by_a_workflow_or_the_triage_module_must_exist(repo: pathlib.Path) -> None:
    labels = [x for x in json.loads((repo / ".github/labels.json").read_text())
              if x["name"] != "needs-triage"]
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "references label 'needs-triage'" in result.stderr
    # The label lives in the JS module now, so that file must be scanned too.
    assert "triage.js references label 'needs-triage'" in result.stderr


def test_size_labels_used_by_triage_must_exist(repo: pathlib.Path) -> None:
    labels = [x for x in json.loads((repo / ".github/labels.json").read_text())
              if x["name"] != "size/XL"]
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "size/XL" in result.stderr


def test_dependabot_label_must_exist(repo: pathlib.Path) -> None:
    labels = [x for x in json.loads((repo / ".github/labels.json").read_text())
              if x["name"] != "dependencies"]
    write_labels(repo, labels)
    result = run(repo)
    assert result.returncode == 1
    assert "dependabot.yml" in result.stderr


def test_missing_dependabot_directory_is_rejected(repo: pathlib.Path) -> None:
    shutil.rmtree(repo / "youtube-transcript")
    result = run(repo)
    assert result.returncode == 1
    assert "does not exist" in result.stderr


def test_malformed_workflow_yaml_raises(repo: pathlib.Path) -> None:
    (repo / ".github/workflows/broken.yml").write_text("a:\n  - b\n c:\n", encoding="utf-8")
    result = run(repo)
    assert result.returncode != 0
