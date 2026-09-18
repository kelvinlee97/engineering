"""Persist per-source HTTP validators and already-reported entry keys."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

MAX_SEEN_KEYS = 5000


@dataclass
class State:
    """What a previous run learned, so the next one stays incremental."""

    validators: dict[str, dict[str, str]] = field(default_factory=dict)
    seen: list[str] = field(default_factory=list)

    def validators_for(self, name: str) -> tuple[str | None, str | None]:
        entry = self.validators.get(name, {})
        return entry.get("etag"), entry.get("last_modified")

    def remember_validators(self, name: str, etag: str | None, last_modified: str | None) -> None:
        entry = {}
        if etag:
            entry["etag"] = etag
        if last_modified:
            entry["last_modified"] = last_modified
        if entry:
            self.validators[name] = entry
        else:
            self.validators.pop(name, None)

    def is_new(self, key: str) -> bool:
        return key not in set(self.seen)

    def remember_keys(self, keys: list[str]) -> None:
        known = set(self.seen)
        for key in keys:
            if key in known:
                continue
            known.add(key)
            self.seen.append(key)
        if len(self.seen) > MAX_SEEN_KEYS:
            self.seen = self.seen[-MAX_SEEN_KEYS:]


def load_state(path: Path) -> State:
    """Read the state file; a missing or corrupt file starts a clean state."""

    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return State()
    if not isinstance(raw, dict):
        return State()
    validators = raw.get("validators")
    seen = raw.get("seen")
    return State(
        validators=validators if isinstance(validators, dict) else {},
        seen=[key for key in seen if isinstance(key, str)] if isinstance(seen, list) else [],
    )


def save_state(path: Path, state: State) -> None:
    """Write the state file atomically enough for a cron-driven run."""

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"validators": state.validators, "seen": state.seen}
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)
