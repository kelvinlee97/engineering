from __future__ import annotations

import json
from pathlib import Path

from yt_transcript.models import CaptureStatus, Cue, EvidenceBundle
from yt_transcript.summary_contract import load_evidence, validate_summary_pair


def evidence(status: CaptureStatus = CaptureStatus.COMPLETE) -> EvidenceBundle:
    return EvidenceBundle(
        status=status,
        source_url="https://www.youtube.com/watch?v=JJyLynh5d6M",
        title="Example",
        language="en",
        source_type="creator",
        cues=[
            Cue("cue-0001", 0, 4, "Start with a real problem."),
            Cue("cue-0002", 4, 8, "Test a small offer."),
        ],
    )


ENGLISH = """# Example

## Source
Status: complete

## What the video says
Start with a real customer problem. [[cue-0001]]
Test a small offer before expanding. [[cue-0002]]

## Practical application
Interview five potential customers this week.

## Limitations
The summary follows the selected subtitle track.
"""

CHINESE = """# 示例

## 来源
状态：complete

## 视频内容
先从真实的客户问题开始。[[cue-0001]]
扩张前先测试一个小型方案。[[cue-0002]]

## 实际应用
本周访谈五位潜在客户。

## 限制
本摘要以选定的字幕轨道为证据。
"""


def test_valid_aligned_summary_pair_passes() -> None:
    assert validate_summary_pair(evidence(), ENGLISH, CHINESE) == []


def test_unknown_citation_is_rejected() -> None:
    errors = validate_summary_pair(evidence(), ENGLISH.replace("cue-0002", "cue-9999"), CHINESE)

    assert "English summary cites unknown cue cue-9999" in errors


def test_mismatched_bilingual_citation_sets_are_rejected() -> None:
    errors = validate_summary_pair(evidence(), ENGLISH, CHINESE.replace("。[[cue-0002]]", "。"))

    assert "English and Chinese summaries cite different evidence" in errors


def test_partial_evidence_cannot_validate_full_summaries() -> None:
    errors = validate_summary_pair(evidence(CaptureStatus.PARTIAL), ENGLISH, CHINESE)

    assert "full summaries require complete evidence" in errors


def test_load_evidence_reconstructs_typed_bundle(tmp_path: Path) -> None:
    path = tmp_path / "evidence.json"
    path.write_text(
        json.dumps(
            {
                "status": "complete",
                "source_url": "https://www.youtube.com/watch?v=JJyLynh5d6M",
                "title": "Example",
                "language": "en",
                "source_type": "creator",
                "cues": [
                    {
                        "cue_id": "cue-0001",
                        "start_seconds": 0,
                        "end_seconds": 4,
                        "text": "Start with a real problem.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    bundle = load_evidence(path)

    assert bundle.status is CaptureStatus.COMPLETE
    assert bundle.cues[0].cue_id == "cue-0001"
