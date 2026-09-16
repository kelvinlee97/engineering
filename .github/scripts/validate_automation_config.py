#!/usr/bin/env python3
"""Check that the repository automation config is well formed.

Run by the "Automation checks" workflow (and usable locally):

    python3 .github/scripts/validate_automation_config.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
GITHUB = ROOT / ".github"
HEX_COLOR = re.compile(r"^[0-9a-f]{6}$")


def main() -> int:
    errors: list[str] = []

    labels = json.loads((GITHUB / "labels.json").read_text(encoding="utf-8"))
    names: set[str] = set()
    for entry in labels:
        name = entry.get("name")
        if not name:
            errors.append(f"label entry without a name: {entry!r}")
            continue
        if name in names:
            errors.append(f"duplicate label: {name}")
        names.add(name)
        color = entry.get("color", "")
        if not HEX_COLOR.match(color):
            errors.append(f"label {name!r}: color must be 6 lowercase hex digits, got {color!r}")
        unknown = set(entry) - {"name", "color", "description"}
        if unknown:
            errors.append(f"label {name!r}: unknown keys {sorted(unknown)}")

    labeler = yaml.safe_load((GITHUB / "labeler.yml").read_text(encoding="utf-8"))
    for label in labeler:
        if label not in names:
            errors.append(f"labeler.yml uses {label!r}, which is missing from labels.json")

    # Every label named in a workflow or in the triage module must exist too.
    sources = sorted((GITHUB / "workflows").glob("*.yml"))
    sources += [p for p in sorted((GITHUB / "scripts").glob("*.js")) if not p.name.endswith(".test.js")]
    for source in sources:
        text = source.read_text(encoding="utf-8")
        if source.suffix == ".yml":
            yaml.safe_load(text)  # raises on malformed YAML
        for quoted in re.findall(r"['\"](needs-triage|size/[A-Z]{1,2}|area: [a-z-]+|translation|bug|enhancement|question|dependencies)['\"]", text):
            if quoted not in names:
                errors.append(f"{source.name} references label {quoted!r}, missing from labels.json")

    dependabot = yaml.safe_load((GITHUB / "dependabot.yml").read_text(encoding="utf-8"))
    if dependabot.get("version") != 2:
        errors.append("dependabot.yml: version must be 2")
    for update in dependabot.get("updates", []):
        for label in update.get("labels", []):
            if label not in names:
                errors.append(
                    f"dependabot.yml: {update.get('package-ecosystem')} uses label {label!r}, "
                    "missing from labels.json"
                )
        directory = update.get("directory", "/")
        if not (ROOT / directory.lstrip("/")).is_dir():
            errors.append(f"dependabot.yml: directory {directory!r} does not exist")

    for problem in errors:
        print(f"error: {problem}", file=sys.stderr)
    if errors:
        return 1
    print(f"ok: {len(labels)} labels, {len(labeler)} labeler rules, "
          f"{len(dependabot.get('updates', []))} dependabot ecosystems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
