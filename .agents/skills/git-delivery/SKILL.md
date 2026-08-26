---
name: git-delivery
description: "Use when the user explicitly requests GitHub pull-request delivery or invokes $git-delivery. Validate, branch, stage, commit, push, and open a PR only as requested; merge and delete branches require separate explicit authorization. Requires authenticated gh."
---

# Git Delivery

Use `git` locally and `gh` for GitHub; follow the nearest `AGENTS.md`.

## Scope

Run only requested stages: commit/push alone does not imply a PR; PR delivery stops before merge unless requested.

## Preflight

1. Run `gh auth status`; stop on failure.
2. Run `gh repo view --json defaultBranchRef,deleteBranchOnMerge`; get the default branch, confirm `origin` is the push remote, and require deletion authorization if auto-delete is true.
3. Record `git status --short --branch`, `git diff --cached --name-only`, and `git diff --name-only`. If any existing path is outside the task, stop; never reset or clean it.
4. Read nearest `AGENTS.md`; run applicable checks for changed paths; stop on failure or ambiguity.

## Classify the starting state

After `git fetch origin`, inspect `git log origin/<default>..HEAD --oneline`:

- **A** — uncommitted task changes, no task commits ahead: branch from `origin/<default>` and carry them.
- **B** — local default has only task commits ahead and is clean: branch from local default; no empty commit or default push.
- **C** — clean feature branch has only task commits ahead: reuse it and push when requested.
- Detached HEAD, mixed changes plus commits, unexpected commits, missing `origin`, or a branch conflict: stop.

## Deliver

1. **Branch**: A uses `git switch -c <type>/<slug> origin/<default>`; B uses local default; C reuses the current branch. Inspect existing branches; never reset one without authorization.
2. **Stage**: `git add <paths>`; staged paths must contain only the task, then review the cached stat.
3. **Commit/push**: A commits using the repository convention; B creates no empty commit; C is already committed. Run `git push -u origin <branch>` only when requested.
4. **PR**: query `gh pr list --head <branch> --state open --limit 1 --json number`; reuse a non-empty result, otherwise run `gh pr create --base <default> --head <branch> --title "<title>" --body "<summary>"`, then read its number with `gh pr view <branch> --json number -q .number`. Inspect closed/merged history before creating another.
5. **Merge gate**: without an explicit merge request, report the PR and stop. Otherwise run `gh pr checks <PR> --watch`, require `MERGEABLE/CLEAN` and required reviews/checks, and never self-approve or use `--admin`.
6. **Merge**: run `gh pr merge <PR> --squash`; add `--delete-branch` only with separate deletion authorization, and stop if repository auto-delete is enabled without that authorization. If squash or a merge queue is unavailable, stop.
7. **Sync**: after merging, run `git switch <default>`, `git pull --ff-only origin <default>`, and `git fetch --prune origin`. If pull fails, stop.
8. **Verify**: require state `MERGED`, read `mergeCommit`, verify it is an ancestor of `<default>`, and require a clean worktree. Verify branch deletion only when authorized.

For an explicit rollback, read [references/rollback.md](references/rollback.md).

Never push default, force-push shared branches, use `--admin`, or delete default. Stop on unrelated changes, secrets, access/remote errors, unexpected commits, conflicts, failed checks, validation/query errors, or unsupported strategies; leave the worktree unchanged.
