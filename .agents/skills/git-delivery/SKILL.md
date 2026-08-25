---
name: git-delivery
description: "GitHub-only delivery workflow: validate changes, branch, stage, commit, push, and open a pull request. Use when the user asks to commit, push, open a pull request, deliver, publish, or release GitHub work, or invokes $git-delivery. Merge and delete branches only when explicitly requested. Requires gh."
---

# Git Delivery (GitHub + gh CLI)

Deliver local work through a GitHub pull request. Use `gh` for GitHub API/PR operations and `git` for local work and transport. Merge or delete only on explicit request.

## Preflight

1. `gh auth status` — confirm access; stop if not authenticated.
2. `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` — get the default branch (used below).
3. Snapshot `git status --short`, `git diff --cached --name-only`, and `git diff --name-only`; stop if any existing change is unrelated, including staged files.
4. Run applicable validation (docs: link/EN-ZH check; code: tests/build/lint). Stop and ask if it fails or the scope is unclear.

## Starting states

- **State A — uncommitted changes**: carry them to a new branch; stage only task paths.
- **State B — local default is ahead of origin**: verify every ahead commit is this task; branch from local default; do not create an empty commit.
- **State C — feature branch**: fetch and verify `git log origin/<default>..HEAD --oneline` contains only this task; stop on anything unexpected, then push and continue at step 4.
- Mixed uncommitted changes and local commits: stop and ask.

## Deliver

1. **Branch**: `git fetch origin`; State A uses `git switch -c <type>/<slug> origin/<default>`, State B uses local default, and State C skips this step. Inspect any reused branch first.
2. **Stage**: `git add <paths>`; `git diff --cached --name-only` must contain only task paths; review the cached stat.
3. **Commit and push**: State A commits using the repository convention; State B does not commit. Push with `git push -u origin <branch>`. State B restores local default only after the branch contains the old tip and the worktree is clean.
4. **Open the PR**: query with `gh pr list --head <branch>`; create only after a successful empty result, then read its number. Stop on query errors.
5. **Merge gate**: without an explicit merge request, report the PR and stop. Otherwise wait for checks (note if none exist), require `MERGEABLE/CLEAN`, and satisfy required reviews/checks.
6. **Merge and clean up**: `gh pr merge $PR --squash --delete-branch`. If squash is rejected as unavailable, stop and ask before changing merge strategy.
7. **Sync local**: `git switch <default>`; `git pull --ff-only`; `git fetch --prune origin`. If pull fails, stop — no rebase or force.
8. **Verify**: require PR state `MERGED`; read `mergeCommit`, verify it is an ancestor of `<default>`, compare `git status --short` with the preflight baseline, and verify `<branch>` is gone locally and from `git ls-remote --heads origin <branch>`.
9. **Rollback**: branch from `origin/<default>`; use `git revert <sha>` for a squash commit or `git revert -m 1 <sha>` for a merge commit; then use the same PR flow.
10. **Hard rules**: never push the default branch directly, force-push shared branches, or delete the default branch; never merge or delete without explicit user authorization.

## Stop and ask

- Unrelated worktree or staged changes exist; secrets or credentials are involved.
- An unexpected commit, merge conflict, remote branch change, validation failure, command error, or unsupported merge strategy occurs.
- Leave the working tree as-is; do not force cleanup.

## Notes

- GitHub-only; requires an authenticated `gh` CLI.
- Follow repo-level AGENTS.md or user overrides when they conflict with these defaults.
