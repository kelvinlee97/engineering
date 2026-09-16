#!/usr/bin/env bash
# Tests for changelog.sh, run against throwaway git repositories.
# Usage: .github/scripts/changelog.test.sh
set -euo pipefail

SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/changelog.sh"
failures=0
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

check() {
  local name="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "ok - $name"
  else
    echo "not ok - $name"
    echo "    expected: $expected"
    echo "    actual:   $actual"
    failures=$((failures + 1))
  fi
}

contains() {
  local name="$1" needle="$2" haystack="$3"
  if printf '%s' "$haystack" | grep -qF -- "$needle"; then
    echo "ok - $name"
  else
    echo "not ok - $name (missing: $needle)"
    failures=$((failures + 1))
  fi
}

absent() {
  local name="$1" needle="$2" haystack="$3"
  if printf '%s' "$haystack" | grep -qF -- "$needle"; then
    echo "not ok - $name (unexpectedly present: $needle)"
    failures=$((failures + 1))
  else
    echo "ok - $name"
  fi
}

new_repo() {
  local dir="$tmp/$1"
  mkdir -p "$dir"
  git -C "$dir" init -q
  git -C "$dir" config user.email t@example.com
  git -C "$dir" config user.name Test
  echo "$dir"
}

commit() {
  local dir="$1" subject="$2"
  echo "$RANDOM" >>"$dir/file"
  git -C "$dir" add file
  git -C "$dir" commit -q -m "$subject"
}

# --- first release: every group, no compare link -----------------------------
repo="$(new_repo first)"
commit "$repo" "docs: add an article"
commit "$repo" "feat(pages): add search"
commit "$repo" "fix: correct a typo"
commit "$repo" "ci: bump actions"
commit "$repo" "random unstructured commit"
git -C "$repo" tag -a v1.0.0 -m v1.0.0
notes="$(cd "$repo" && GITHUB_REPOSITORY=o/r "$SCRIPT" v1.0.0)"

contains "first release header" "First release" "$notes"
contains "docs grouped under articles" "- docs: add an article" "$notes"
contains "feat grouped under articles" "- feat(pages): add search" "$notes"
contains "fix grouped under fixes" "### Fixes" "$notes"
contains "ci grouped under tooling" "### Site and tooling" "$notes"
contains "unstructured commit grouped under other" "- random unstructured commit" "$notes"
absent "no compare link on a first release" "**Full diff**" "$notes"
check "each commit appears once" "5" "$(printf '%s\n' "$notes" | grep -c '^- ')"

# --- incremental release: only new commits, with a compare link ---------------
commit "$repo" "docs: a later article"
git -C "$repo" tag -a v1.1.0 -m v1.1.0
notes="$(cd "$repo" && GITHUB_REPOSITORY=o/r "$SCRIPT" v1.1.0)"

contains "incremental header names the previous tag" "Changes since v1.0.0" "$notes"
contains "new commit is listed" "- docs: a later article" "$notes"
absent "commits from the previous release are excluded" "add an article" "$notes"
contains "compare link is present" "https://github.com/o/r/compare/v1.0.0...v1.1.0" "$notes"

# --- a release with no commits of a given type omits that heading ------------
repo="$(new_repo docsonly)"
commit "$repo" "docs: only docs here"
git -C "$repo" tag -a v1.0.0 -m v1.0.0
notes="$(cd "$repo" && "$SCRIPT" v1.0.0)"
absent "empty Fixes heading is omitted" "### Fixes" "$notes"
absent "empty Other heading is omitted" "### Other" "$notes"
absent "compare link omitted without GITHUB_REPOSITORY" "**Full diff**" "$notes"

# --- merge commits are excluded ----------------------------------------------
repo="$(new_repo merges)"
commit "$repo" "docs: base"
git -C "$repo" checkout -qb side
commit "$repo" "fix: on a branch"
git -C "$repo" checkout -q -
git -C "$repo" merge -q --no-ff side -m "Merge pull request #1 from side"
git -C "$repo" tag -a v1.0.0 -m v1.0.0
notes="$(cd "$repo" && "$SCRIPT" v1.0.0)"
contains "branch commit is listed" "- fix: on a branch" "$notes"
absent "merge commit is not listed" "Merge pull request" "$notes"

# --- breaking-change and scoped prefixes still group correctly ---------------
repo="$(new_repo prefixes)"
commit "$repo" "feat!: breaking change"
commit "$repo" "fix(ci): scoped fix"
commit "$repo" "fixup something unstructured"
git -C "$repo" tag -a v1.0.0 -m v1.0.0
notes="$(cd "$repo" && "$SCRIPT" v1.0.0)"
contains "feat! groups under articles" "- feat!: breaking change" "$notes"
contains "fix(ci) groups under fixes" "- fix(ci): scoped fix" "$notes"
contains "'fixup' is not treated as a fix" "### Other" "$notes"

# --- writes to a file when given one -----------------------------------------
(cd "$repo" && "$SCRIPT" v1.0.0 "$tmp/notes.md")
contains "output file is written" "First release" "$(cat "$tmp/notes.md")"

# --- a missing tag argument fails loudly -------------------------------------
if (cd "$repo" && "$SCRIPT" >/dev/null 2>&1); then
  echo "not ok - missing tag argument should fail"
  failures=$((failures + 1))
else
  echo "ok - missing tag argument fails"
fi

echo
if [ "$failures" -eq 0 ]; then
  echo "all changelog tests passed"
else
  echo "$failures changelog test(s) failed"
  exit 1
fi
