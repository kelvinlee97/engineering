"""Command line entry point: `rss-digest run`."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from rss_digest.config import ConfigError, load_config
from rss_digest.digest import render_json, render_markdown, select, window_start
from rss_digest.fetch import fetch_source
from rss_digest.models import FetchOutcome
from rss_digest.store import load_state, save_state

DEFAULT_CONFIG = Path("feeds.toml")
DEFAULT_STATE = Path(".local/rss-digest/state.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rss-digest",
        description="Aggregate configured RSS/Atom feeds into one deduplicated digest.",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="feeds TOML file")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="dedup/ETag state file")
    parser.add_argument("--output", type=Path, help="write the digest here instead of stdout")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument(
        "--days", type=int, default=7, help="age window in days; 0 disables the window"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="ignore the seen-entry ledger and report everything in the window",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="render the digest without recording validators or seen keys",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        sources = load_config(args.config)
    except ConfigError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    state = load_state(args.state)
    outcomes: list[FetchOutcome] = []
    for source in sources:
        etag, last_modified = state.validators_for(source.name)
        outcomes.append(fetch_source(source, etag=etag, last_modified=last_modified))

    entries = select(
        outcomes,
        since=window_start(args.days),
        is_new=None if args.all else state.is_new,
    )

    if args.format == "json":
        rendered = render_json(entries, outcomes)
    else:
        rendered = render_markdown(entries, outcomes, generated=datetime.now(UTC))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {len(entries)} items to {args.output}", file=sys.stderr)
    else:
        print(rendered)

    if not args.dry_run:
        for outcome in outcomes:
            if outcome.status in {"ok", "not-modified"}:
                state.remember_validators(outcome.source.name, outcome.etag, outcome.last_modified)
        state.remember_keys([entry.key for entry in entries])
        save_state(args.state, state)

    failures = [outcome for outcome in outcomes if outcome.status == "error"]
    for outcome in failures:
        print(f"warning: {outcome.source.name}: {outcome.error}", file=sys.stderr)
    return 1 if failures and len(failures) == len(outcomes) else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
