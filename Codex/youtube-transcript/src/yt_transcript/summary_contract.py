from __future__ import annotations

import json
import re
from pathlib import Path

from yt_transcript.models import CaptureStatus, Cue, EvidenceBundle

_CITATION = re.compile(r"\[\[(cue-\d{4})\]\]")


def _citations(markdown: str) -> set[str]:
    return set(_CITATION.findall(markdown))


def load_evidence(path: Path) -> EvidenceBundle:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("cues"), list):
        raise ValueError("evidence file has an invalid structure")
    try:
        cues = [
            Cue(
                cue_id=str(item["cue_id"]),
                start_seconds=float(item["start_seconds"]),
                end_seconds=float(item["end_seconds"]),
                text=str(item["text"]),
            )
            for item in payload["cues"]
            if isinstance(item, dict)
        ]
        return EvidenceBundle(
            status=CaptureStatus(str(payload["status"])),
            source_url=str(payload["source_url"]),
            title=str(payload["title"]),
            language=str(payload["language"]),
            source_type=str(payload["source_type"]),
            cues=cues,
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("evidence file has an invalid structure") from error


def validate_summary_pair(
    evidence: EvidenceBundle,
    english_markdown: str,
    chinese_markdown: str,
) -> list[str]:
    errors: list[str] = []
    if evidence.status is not CaptureStatus.COMPLETE:
        errors.append("full summaries require complete evidence")

    known = {cue.cue_id for cue in evidence.cues}
    english_citations = _citations(english_markdown)
    chinese_citations = _citations(chinese_markdown)

    for cue_id in sorted(english_citations - known):
        errors.append(f"English summary cites unknown cue {cue_id}")
    for cue_id in sorted(chinese_citations - known):
        errors.append(f"Chinese summary cites unknown cue {cue_id}")
    if english_citations != chinese_citations:
        errors.append("English and Chinese summaries cite different evidence")
    if not english_citations:
        errors.append("full summaries require evidence citations")

    english_sections = (
        "## Source",
        "## What the video says",
        "## Practical application",
        "## Limitations",
    )
    chinese_sections = ("## 来源", "## 视频内容", "## 实际应用", "## 限制")
    for section in english_sections:
        if section not in english_markdown:
            errors.append(f"English summary is missing section: {section}")
    for section in chinese_sections:
        if section not in chinese_markdown:
            errors.append(f"Chinese summary is missing section: {section}")

    return errors
