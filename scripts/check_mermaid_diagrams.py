#!/usr/bin/env python3
"""Actually render every Mermaid diagram in the repo's tracked Markdown files.

`wiki_check.py` only checks diagram text with regexes (e.g. for
accTitle/accDescr); it never parses the diagram, so syntax errors that Mermaid
itself rejects (invalid edge-style combinations, bad label escaping, etc.)
can pass validation and still fail to render on GitHub. This script closes
that gap by feeding every diagram through the real Mermaid renderer.

All diagrams are concatenated into one temporary Markdown file and rendered
in a single `mmdc` invocation (one browser launch) rather than one process
per diagram, which is roughly 250x faster across this repo's diagram count.
The tradeoff: `mmdc` stops at the first diagram it cannot parse, so a run
that fails only guarantees at least one bad diagram, not an exhaustive list.
Re-run after each fix to find the next one, if any.

Requires `@mermaid-js/mermaid-cli` (invoked via `npx`) and a Chromium the
environment can launch; see PUPPETEER_CONFIG below.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MERMAID_RE = re.compile(r"(?ms)^```mermaid[^\n]*\n(?P<body>.*?)^```\s*$")
SUCCESS_RE = re.compile(r"✅ \S+\.svg")
PUPPETEER_CONFIG = {"args": ["--no-sandbox"]}


def _tracked_markdown_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "*.md"],
        capture_output=True,
        check=True,
    )
    return sorted(
        root / item.decode() for item in result.stdout.split(b"\0") if item
    )


def _locate_failure(output: str, order: list[tuple[Path, int]]) -> str:
    """Identify which diagram failed.

    mmdc renders diagrams from a Markdown file sequentially and reports a
    parse error's line number relative to that one diagram's own text, not
    the combined file, so we can't map it back directly. Instead, count how
    many diagrams rendered successfully (✅ lines) before the first "Error"
    in the output: since rendering is sequential in document order, that
    count is the (0-based) index of the diagram that failed, in the same
    order diagrams were appended to `order`.
    """

    error_pos = output.find("Error")
    if error_pos == -1:
        return "unknown diagram (no 'Error' marker found in output)"
    successes_before = len(SUCCESS_RE.findall(output[:error_pos]))
    if successes_before >= len(order):
        return "unknown diagram (success count exceeds known diagrams)"
    path, index = order[successes_before]
    return f"{path} (diagram {index})"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    files = _tracked_markdown_files(root)

    order: list[tuple[Path, int]] = []
    lines: list[str] = []
    total = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        for per_file_index, match in enumerate(MERMAID_RE.finditer(text), start=1):
            total += 1
            lines.append("```mermaid")
            lines.extend(match.group("body").splitlines())
            lines.append("```")
            lines.append("")
            order.append((path.relative_to(root), per_file_index))

    if total == 0:
        print("No Mermaid diagrams found.")
        return 0

    print(f"Rendering {total} Mermaid diagram(s) in one batch...")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        config_path = tmp_path / "puppeteer-config.json"
        config_path.write_text(json.dumps(PUPPETEER_CONFIG))
        combined_path = tmp_path / "combined.md"
        combined_path.write_text("\n".join(lines), encoding="utf-8")
        out_path = tmp_path / "combined_out.md"

        result = subprocess.run(
            [
                "npx",
                "--yes",
                "@mermaid-js/mermaid-cli",
                "-p",
                str(config_path),
                "-i",
                str(combined_path),
                "-o",
                str(out_path),
            ],
            capture_output=True,
            text=True,
        )

        combined_output = result.stdout + result.stderr
        failed = result.returncode != 0 or "Error" in combined_output

        if failed:
            print("\nMermaid rendering failed.\n", file=sys.stderr)
            source = _locate_failure(combined_output, order)
            print(f"Likely source: {source}\n", file=sys.stderr)
            print(combined_output, file=sys.stderr)
            print(
                "\nNote: mmdc stops at the first unparsable diagram, so fix "
                "this one and re-run to check for any others.",
                file=sys.stderr,
            )
            return 1

    print(f"All {total} Mermaid diagrams rendered successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
