from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from yt_transcript.models import CaptureStatus

_TIMESTAMP = re.compile(r"youtube\.com/watch\?v=[^\s)]+&t=(\d+)s")
_DISPOSITIONS = {"included", "compressed", "cta"}
_AUDIT_KEYS = (
    "missing_from_english",
    "missing_from_chinese",
    "unsupported_english_claims",
    "unsupported_chinese_claims",
    "timestamp_mismatches",
)


def _timestamps(markdown: str) -> set[int]:
    return {int(value) for value in _TIMESTAMP.findall(markdown)}


def validate_publication(
    validation_path: Path, english_path: Path, chinese_path: Path
) -> list[str]:
    payload: Any = json.loads(validation_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return ["validation ledger is not an object"]
    errors: list[str] = []
    if payload.get("status") != CaptureStatus.COMPLETE.value:
        errors.append("local capture is not complete")
    chunks = payload.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        errors.append("validation ledger has no chunks")
        chunks = []

    required_timestamps: set[int] = set()
    for index, chunk in enumerate(chunks, start=1):
        if not isinstance(chunk, dict):
            errors.append(f"chunk {index} is invalid")
            continue
        if chunk.get("status") != "processed":
            errors.append(f"chunk {index} is not processed")
        items = chunk.get("content_items")
        if not isinstance(items, list) or not items:
            errors.append(f"chunk {index} has no content items")
            continue
        for item_index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"chunk {index} item {item_index} is invalid")
                continue
            disposition = item.get("disposition")
            if disposition not in _DISPOSITIONS:
                errors.append(f"chunk {index} item {item_index} has invalid disposition")
                continue
            if disposition != "cta":
                timestamp = item.get("timestamp_seconds")
                if not isinstance(timestamp, int) or timestamp < 0:
                    errors.append(f"chunk {index} item {item_index} has no timestamp")
                else:
                    required_timestamps.add(timestamp)

    audit = payload.get("audit")
    if not isinstance(audit, dict) or audit.get("status") != "complete":
        errors.append("independent audit is not complete")
    elif any(audit.get(key) for key in _AUDIT_KEYS):
        errors.append("independent audit contains unresolved findings")

    english_timestamps = _timestamps(english_path.read_text(encoding="utf-8"))
    chinese_timestamps = _timestamps(chinese_path.read_text(encoding="utf-8"))
    if english_timestamps != chinese_timestamps:
        errors.append("English and Chinese summaries use different timestamps")
    missing = required_timestamps - english_timestamps
    if missing:
        errors.append(f"summaries omit required timestamps: {sorted(missing)}")
    return errors
