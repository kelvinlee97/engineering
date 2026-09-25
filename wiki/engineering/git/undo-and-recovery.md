---
type: Playbook
title: Undoing and recovering in Git
description: Choose between restore, reset, revert, and reflog by whether the work is shared, and check a pre-flight list before any destructive Git operation.
tags: [git, runbook]
sources:
  - id: git-operations-reference
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/README.md
    title: Essential Git Commands for Operations
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-04-commit
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/04-commit/README.md
    title: "Git command-line basics: git commit"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:30:00Z }
status: draft
---
Which undo is safe depends on one question: has anyone else seen this history? On shared branches, add a corrective commit; rewrite only work nobody else has.[^git-operations-reference]

## Pushed or deployed mistakes: revert

`git revert <bad-commit>` creates a new inverse commit and keeps an auditable history, so it suits shared branches and post-release fixes. Reverting a merge needs a mainline parent such as `-m 1`, agreed with the team.[^git-operations-reference] The same reasoning rules out `--amend` on a commit others have already pulled.[^git-tutorial-04-commit]

## Local mistakes: reset

| Command | History | Index | Working tree | Use |
| --- | --- | --- | --- | --- |
| `git reset --soft HEAD~1` | Moves back | Keeps | Keeps | Reorganize the latest unshared commit |
| `git reset --mixed HEAD~1` | Moves back | Clears | Keeps | Restage selected content (the default) |
| `git reset --hard HEAD~1` | Moves back | Overwrites | Overwrites | High risk: only confirmed-unneeded, unshared work |

As tabled in the reference. Never reset and force-push a shared `main` or release branch.[^git-operations-reference]

## Recovery and investigation

- `git reflog` shows where `HEAD` pointed before; inspect a candidate commit and protect it with a new recovery branch. Reflog is local and expires.
- `git blame` finds the last commit that changed a line (not who is responsible); `git bisect` binary-searches a regression; always finish with `git bisect reset`.[^git-operations-reference]

## High-risk operations

| Operation | Safer practice |
| --- | --- |
| `git push --force` | `--force-with-lease` on a personal branch, after fetching; never a licence to force-push shared branches |
| `git reset --hard` | Check `status`, `diff`, `reflog`; branch or stash what you may need |
| Deleting a remote branch | Check PRs, deployments, protection rules; get authorisation |
| `git clean -fd` | Preview with `git clean -nd` |

As tabled in the reference. Its pre-flight checklist asks: right repository and branch, anything unsaved, fresh remote state, shared or personal branch, a safer mechanism available, a recovery point, and whether production, releases, or credentials are involved.[^git-operations-reference]

## Related

- [Syncing a Git branch](branches-and-pull-requests.md#syncing-a-git-branch)
- [Safe change procedure](../operations/incident-operations.md#safe-change-procedure)

[^git-operations-reference]: [Essential Git Commands for Operations](../../sources/git-operations-reference.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Git/README.md)
[^git-tutorial-04-commit]: [Git command-line basics: git commit](../../sources/git-tutorial-04-commit.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Git/04-commit/README.md)
