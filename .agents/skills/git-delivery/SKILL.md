---
name: git-delivery
description: "GitHub-only Git delivery workflow driven by the gh CLI: validate changes, create a feature branch, stage only relevant files, commit, push, open a pull request, merge it, and delete the branch. Use when the user asks to commit, push, open or merge a pull request, deliver, publish, or release finished GitHub work, or explicitly invokes $git-delivery. Requires GitHub and the gh CLI. Stop and ask before acting when unrelated changes, secrets, merge conflicts, or destructive operations are involved."
---

# Git Delivery (GitHub + gh CLI)

Deliver completed local work to the default branch via a GitHub pull request, then clean up. GitHub-only; use the gh CLI for all remote operations.

## Preflight

1. `gh auth status` — confirm access; stop if not authenticated.
2. `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` — get the default branch (used below).
3. `git status --short` — note unrelated/uncommitted changes; never stage or commit them.
4. Run applicable validation (docs: link/EN-ZH check; code: tests/build/lint). Stop and ask if it fails or the scope is unclear.

## Starting states

- **State A — uncommitted changes**: step 1 carries them to the new branch; in step 2 stage only this task's paths.
- **State B — commits already on the local default branch** (ahead of origin): never push the default branch directly. In step 1 branch from your local default (no `origin/` prefix) so the commits move onto the branch; after step 3's push, restore the local default per step 3's preconditions.
- **State C — already on a feature branch**: `git fetch origin`, verify only this task's commits (`git log origin/<default>..HEAD --oneline`), push, continue from step 4.
- Uncommitted changes plus local commits at once: commit the relevant changes first or stop and ask.

## Deliver

1. **Branch from the latest base**: `git fetch origin`; `git switch -c <type>/<slug> origin/<default>` (reuse the branch with `git switch` if it already exists). State B: no `origin/` prefix. State C: skip steps 1–3.
2. **Stage only this task's paths**: `git add <paths>`; verify with `git status --short` and `git diff --cached --stat`. An empty staged diff is expected in State B.
3. **Commit and push**: `git commit -m "<type>: <subject>"` (`docs|feat|fix`); `git push -u origin <branch>`. State B: after the push, restore the local default with `git switch <default> && git reset --hard origin/<default>` only when (1) push succeeded, (2) the branch holds every commit, (3) no unrelated uncommitted changes.
4. **Open the PR (idempotent)**: `gh pr view <branch> --json number -q .number 2>/dev/null || gh pr create --base <default> --head <branch> --title "<title>" --body "<summary>"`; then `PR=$(gh pr view <branch> --json number -q .number)`.
5. **Merge gate**: wait for a terminal state with `gh pr checks $PR --watch`; if no checks are configured, note that in the report. `gh pr view $PR --json mergeable,mergeStateStatus -q '"\(.mergeable)/\(.mergeStateStatus)"'` must be `MERGEABLE/CLEAN`. Never merge a failing or conflicting PR.
6. **Merge and clean up**: `gh pr merge $PR --squash --delete-branch`; fall back to `--merge` if squash is unavailable and say so.
7. **Sync local**: `git switch <default>`; `git pull --ff-only`; `git fetch --prune origin`. If `pull --ff-only` fails, stop — no `--rebase` or force.
8. **Verify**: `MERGED=$(gh pr view $PR --json mergedCommit -q .mergedCommit.oid)`; `git merge-base --is-ancestor $MERGED <default>` must exit 0; `git status --short` shows no new changes from this flow; `<branch>` is gone locally (`git branch -a`) and remotely (`git ls-remote --heads origin <branch>` empty).
9. **Rollback**: if the merged work is broken, `git switch -c fix/revert-<slug> origin/<default>`; `git revert <sha>`; push; PR; merge via the same flow.
10. **Hard rules**: never push the default branch directly; never force-push shared branches; only delete non-default branches.

## Stop and ask

- Unrelated worktree changes exist (keep them untouched).
- Secrets, credentials, internal addresses, or irreversible deletion are involved.
- Merge conflicts, a remote branch changed under you, or any step fails (leave the working tree as-is, no forced cleanup).

## Notes

- GitHub-only; requires an authenticated gh CLI.
- Follow repo-level AGENTS.md or user overrides when they conflict with these defaults.
