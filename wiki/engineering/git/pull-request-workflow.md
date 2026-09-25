---
type: Playbook
title: GitHub pull request workflow
description: Publish a change on GitHub through a focused branch, a reviewed pull request, passing checks, and a merge, then clean up.
tags: [git, github, runbook]
sources:
  - id: git-publish-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/publish-to-github/README.md
    title: "Publish Changes to GitHub: A Beginner's Guide"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-operations-reference
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/README.md
    title: Essential Git Commands for Operations
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:30:00Z }
status: draft
---
Publishing to GitHub is a straight line: edit, inspect, test, commit, push a branch, open a pull request, merge. Nothing reaches `main` until the pull request is merged.[^git-publish-guide]

## Steps

1. **Update the base:** `git switch main`, `git pull --ff-only`.[^git-publish-guide]
2. **Branch:** one focused branch per purpose, such as `fix/login-timeout`.[^git-publish-guide]
3. **Change and check:** follow the repository's `README`, `CONTRIBUTING.md`, or `AGENTS.md`, run the smallest relevant check, and read `git status` and `git diff`.[^git-publish-guide]
4. **Stage and commit** explicit paths, following the [commit workflow](commit-workflow.md).[^git-publish-guide]
5. **Push:** confirm `git remote -v`, then `git push --set-upstream origin HEAD`.[^git-publish-guide]
6. **Open the PR** (`gh pr create --web`): check base and head branches, a title stating the outcome, and a description of what changed, why, and how it was checked; draft if not ready.[^git-publish-guide]
7. **Respond:** push fixes to the same branch rather than opening new PRs, and fix failed checks before merging.[^git-publish-guide]
8. **Merge and clean up** once reviews and checks pass; squash merge folds the branch into one commit where the repository allows it. After a squash merge, `git branch -d` cannot prove the branch merged, so confirm the PR is merged before `git branch -D`.[^git-publish-guide]

Without push access, use the fork model: fork, clone your fork, add the original as `upstream`, push to your fork, and open the PR against the original.[^git-publish-guide] `git worktree add` gives a second branch its own directory for parallel work; remove it with `git worktree remove`, not by deleting the folder.[^git-publish-guide]

## Mistakes the guide calls out

Working on `main`, `git add .` without looking, treating commit as publish, pushing secrets and deleting them later, force-pushing to fix a rejection, the wrong base branch, merging with failing checks, and accepting an AI-written PR description without comparing it to the diff.[^git-publish-guide]

Tags are for traceability: an annotated tag identifies a source commit but does not prove the deployment succeeded, and `git push origin --tags` can publish tags that are not ready.[^git-operations-reference]

## Related

- [Agents propose, people and policy accept](../ai-engineering/propose-accept-boundary.md): the same PR gates applied to agent-authored changes.
- [Syncing a Git branch](branch-sync.md)
- Source: [Publish changes to GitHub](../../sources/git-publish-guide.md)
- Source: [Essential Git commands for operations](../../sources/git-operations-reference.md)

[^git-publish-guide]: Publish Changes to GitHub: A Beginner's Guide
[^git-operations-reference]: Essential Git Commands for Operations
