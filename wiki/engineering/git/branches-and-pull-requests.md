---
type: Playbook
title: Branches and pull requests
description: Keeping a branch in sync with its upstream and taking it through the GitHub pull request workflow.
tags:
- git
- github
aliases:
- engineering/git/branch-sync
- engineering/git/pull-request-workflow
sources:
- id: git-operations-reference
  resource: https://github.com/kelvinlee97/engineering/blob/main/Git/README.md
  title: Essential Git Commands for Operations
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: git-publish-guide
  resource: https://github.com/kelvinlee97/engineering/blob/main/Git/publish-to-github/README.md
  title: 'Publish Changes to GitHub: A Beginner''s Guide'
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Two workflows for getting a branch merged: first sync it with its upstream by fetching and choosing merge or rebase on purpose, then take it through a GitHub pull request.

## Syncing a Git branch

Syncing starts with facts: fetch, then see which commits exist only upstream and only locally, and only then choose how to integrate.[^git-operations-reference]

```bash
git fetch --prune
git status
git log --oneline --graph --decorate HEAD..@{upstream}   # only upstream
git log --oneline --graph --decorate @{upstream}..HEAD   # only local
```

### Choosing a strategy

| Situation | Action | Why |
| --- | --- | --- |
| Local is only behind | `git pull --ff-only` | Fast-forward only; fails on divergence instead of making a surprise merge |
| Divergent personal, unshared branch | `git pull --rebase` | Replays your commits on the updated remote; linear history |
| Shared branch where merges are preferred | `git pull --no-rebase` or `git merge @{upstream}` | Integrates without rewriting shared commits |
| A merge commit must stay visible | `--no-ff` | Only when team policy wants the extra node |
| Neither side moved | Nothing | Do not create activity just to sync |

As recommended in the operations reference. The message `Need to specify how to reconcile divergent branches` asks you to choose; it does not mean data is corrupt.[^git-operations-reference] The GitHub guide starts every piece of work with `git pull --ff-only` on `main`, and if it fails, stops to inspect rather than force-pushing or resetting a shared branch.[^git-publish-guide]

### Conflicts

Edit the file, remove the markers, check the result, `git add` it, then `git rebase --continue` or `git commit`; `--abort` backs out safely. Do not pick one side just to make the markers go away: a conflict means two changes to the same meaning, so run the relevant checks afterwards.[^git-operations-reference]

## GitHub pull request workflow

Publishing to GitHub is a straight line: edit, inspect, test, commit, push a branch, open a pull request, merge. Nothing reaches `main` until the pull request is merged.[^git-publish-guide]

### Steps

1. **Update the base:** `git switch main`, `git pull --ff-only`.
2. **Branch:** one focused branch per purpose, such as `fix/login-timeout`.
3. **Change and check:** follow the repository's `README`, `CONTRIBUTING.md`, or `AGENTS.md`, run the smallest relevant check, and read `git status` and `git diff`.
4. **Stage and commit** explicit paths, following the [commit workflow](git-fundamentals.md#commit-workflow).
5. **Push:** confirm `git remote -v`, then `git push --set-upstream origin HEAD`.
6. **Open the PR** (`gh pr create --web`): check base and head branches, a title stating the outcome, and a description of what changed, why, and how it was checked; draft if not ready.
7. **Respond:** push fixes to the same branch rather than opening new PRs, and fix failed checks before merging.
8. **Merge and clean up** once reviews and checks pass; squash merge folds the branch into one commit where the repository allows it. After a squash merge, `git branch -d` cannot prove the branch merged, so confirm the PR is merged before `git branch -D`.

Without push access, use the fork model: fork, clone your fork, add the original as `upstream`, push to your fork, and open the PR against the original. `git worktree add` gives a second branch its own directory for parallel work; remove it with `git worktree remove`, not by deleting the folder.[^git-publish-guide]

### Mistakes the guide calls out

Working on `main`, `git add .` without looking, treating commit as publish, pushing secrets and deleting them later, force-pushing to fix a rejection, the wrong base branch, merging with failing checks, and accepting an AI-written PR description without comparing it to the diff.[^git-publish-guide]

Tags are for traceability: an annotated tag identifies a source commit but does not prove the deployment succeeded, and `git push origin --tags` can publish tags that are not ready.[^git-operations-reference]

## Related

- [Undoing and recovering in Git](undo-and-recovery.md)
- [Git's four places](git-fundamentals.md#gits-four-places)
- [Agents propose, people and policy accept](../ai-engineering/ai-native-sdlc.md#agents-propose-people-and-policy-accept): the same PR gates applied to agent-authored changes.

[^git-operations-reference]: [Essential Git Commands for Operations](../../sources/git-operations-reference.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Git/README.md)
[^git-publish-guide]: [Publish Changes to GitHub: A Beginner's Guide](../../sources/git-publish-guide.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Git/publish-to-github/README.md)
