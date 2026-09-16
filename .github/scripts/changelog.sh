#!/usr/bin/env bash
# Build release notes for a tag, grouped by conventional-commit type.
#
# Usage: changelog.sh <tag> [output-file]
#
# Notes cover the commits between the previous v* tag and <tag>, or the whole
# history when <tag> is the first release. Output goes to stdout when no
# output file is given. Tested by .github/scripts/changelog.test.sh.
set -euo pipefail

TAG="${1:?usage: changelog.sh <tag> [output-file]}"
OUT="${2:-/dev/stdout}"
SERVER_URL="${GITHUB_SERVER_URL:-https://github.com}"
REPOSITORY="${GITHUB_REPOSITORY:-}"

TYPED='^(docs|feat|fix|ci|build|chore|style|refactor|test|perf)(\(|:|!)'

previous="$(git tag --sort=-creatordate --list 'v*' | grep -Fxv "$TAG" | head -n1 || true)"
if [ -n "$previous" ]; then
  range="$previous..$TAG"
  printf 'Changes since %s\n\n' "$previous" >"$OUT"
else
  range="$TAG"
  printf 'First release\n\n' >"$OUT"
fi

emit() {
  local heading="$1" pattern="$2" body
  body="$(git log --no-merges --pretty=format:'- %s (%h)' --perl-regexp --grep="$pattern" "$range")"
  if [ -n "$body" ]; then
    printf '### %s\n\n%s\n\n' "$heading" "$body" >>"$OUT"
  fi
}

emit "New and updated articles" '^(docs|feat)(\(|:|!)'
emit "Fixes" '^fix(\(|:|!)'
emit "Site and tooling" '^(ci|build|chore|style|refactor|test|perf)(\(|:|!)'

other="$(git log --no-merges --pretty=format:'- %s (%h)' --perl-regexp --invert-grep --grep="$TYPED" "$range")"
if [ -n "$other" ]; then
  printf '### Other\n\n%s\n\n' "$other" >>"$OUT"
fi

if [ -n "$previous" ] && [ -n "$REPOSITORY" ]; then
  printf '**Full diff**: %s/%s/compare/%s...%s\n' "$SERVER_URL" "$REPOSITORY" "$previous" "$TAG" >>"$OUT"
fi
