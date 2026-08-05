from __future__ import annotations

import html
import re
from pathlib import Path

from yt_transcript.models import Cue, DiscardedCue, ParseResult

_TIMING = re.compile(
    r"^(?P<start>(?:\d{2}:)?\d{2}:\d{2}\.\d{3})\s+-->\s+"
    r"(?P<end>(?:\d{2}:)?\d{2}:\d{2}\.\d{3})(?:\s+.*)?$"
)
_TAG = re.compile(r"<[^>]+>")


def _seconds(value: str) -> float:
    parts = value.split(":")
    if len(parts) == 2:
        hours = "0"
        minutes, seconds = parts
    else:
        hours, minutes, seconds = parts
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def _clean_text(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip())
    return " ".join(html.unescape(_TAG.sub("", text)).split())


def parse_vtt(path: Path) -> ParseResult:
    content = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    blocks = [block.strip() for block in re.split(r"\n{2,}", content) if block.strip()]
    cue_blocks = [
        block for block in blocks if not block.startswith(("WEBVTT", "NOTE", "STYLE", "REGION"))
    ]
    cues: list[Cue] = []
    discarded: list[DiscardedCue] = []

    for source_index, block in enumerate(cue_blocks, start=1):
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            discarded.append(DiscardedCue(source_index, "missing timing line", block))
            continue

        match = _TIMING.match(lines[timing_index].strip())
        if match is None:
            discarded.append(DiscardedCue(source_index, "invalid timing line", block))
            continue

        text = _clean_text(lines[timing_index + 1 :])
        if not text:
            discarded.append(DiscardedCue(source_index, "empty cue text", block))
            continue

        start = _seconds(match.group("start"))
        end = _seconds(match.group("end"))
        if end < start:
            discarded.append(DiscardedCue(source_index, "cue ends before it starts", block))
            continue

        cues.append(Cue(f"cue-{len(cues) + 1:04d}", start, end, text))

    return ParseResult(cues=cues, source_cue_count=len(cue_blocks), discarded=discarded)
