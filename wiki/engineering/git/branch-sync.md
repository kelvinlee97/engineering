---
type: Playbook
title: Syncing a Git branch
description: Fetch first, compare local and upstream commits, then choose fast-forward, rebase, or merge deliberately, and resolve conflicts on purpose.
tags: [git, runbook]
sources:
  - id: git-operations-reference
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/README.md
    title: Essential Git Commands for Operations
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-publish-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/publish-to-github/README.md
    title: "Publish Changes to GitHub: A Beginner's Guide"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:30:00Z }
status: draft
---
Syncing starts with facts: fetch, then see which commits exist only upstream and only locally, and only then choose how to integrate.[^git-operations-reference]

```bash
git fetch --prune
git status
git log --oneline --graph --decorate HEAD..@{upstream}   # only upstream
git log --oneline --graph --decorate @{upstream}..HEAD   # only local
```

## Choosing a strategy

| Situation | Action | Why |
| --- | --- | --- |
| Local is only behind | `git pull --ff-only` | Fast-forward only; fails on divergence instead of making a surprise merge |
| Divergent personal, unshared branch | `git pull --rebase` | Replays your commits on the updated remote; linear history |
| Shared branch where merges are preferred | `git pull --no-rebase` or `git merge @{upstream}` | Integrates without rewriting shared commits |
| A merge commit must stay visible | `--no-ff` | Only when team policy wants the extra node |
| Neither side moved | Nothing | Do not create activity just to sync |

As recommended in the operations reference.[^git-operations-reference] The message `Need to specify how to reconcile divergent branches` asks you to choose; it does not mean data is corrupt.[^git-operations-reference] The GitHub guide starts every piece of work with `git pull --ff-only` on `main`, and if it fails, stops to inspect rather than force-pushing or resetting a shared branch.[^git-publish-guide]

## Conflicts

Edit the file, remove the markers, check the result, `git add` it, then `git rebase --continue` or `git commit`; `--abort` backs out safely. Do not pick one side just to make the markers go away: a conflict means two changes to the same meaning, so run the relevant checks afterwards.[^git-operations-reference]

## Related

- [Undoing and recovering in Git](undo-and-recovery.md)
- [Git's four places](git-four-places.md)
- Source: [Essential Git commands for operations](../../sources/git-operations-reference.md)
- Source: [Publish changes to GitHub](../../sources/git-publish-guide.md)

[^git-operations-reference]: Essential Git Commands for Operations
[^git-publish-guide]: Publish Changes to GitHub: A Beginner's Guide
