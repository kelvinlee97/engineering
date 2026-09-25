---
type: Concept
title: Git's four places
description: Git moves work between the working tree, the staging area, the local repository, and a remote; most commands inspect or move content between them.
tags: [git]
sources:
  - id: git-operations-reference
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/README.md
    title: Essential Git Commands for Operations
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-00-init
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/00-init/README.md
    title: "Git command-line basics: git init"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-02-add
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/02-add/README.md
    title: "Git command-line basics: git add"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-06-diff
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/06-diff/README.md
    title: "Git command-line basics: git diff"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:30:00Z }
status: draft
---
Almost every everyday Git command either inspects or moves content between four places: the working tree, the staging area, the local repository, and a remote repository.[^git-operations-reference]

| Place | What it holds |
| --- | --- |
| Working tree | The files you see and edit |
| Staging area (index) | The exact content prepared for the next commit |
| Local repository | Commit history on this machine; `HEAD` normally marks the current branch's latest commit |
| Remote repository | For example `origin`; `origin/main` is your *local record* of it, only as fresh as your last `fetch` |

As defined in the operations reference.[^git-operations-reference] `git init` creates the hidden `.git/` directory that holds the local repository; before that, Git does not know the folder exists.[^git-tutorial-00-init]

## Moving and inspecting

`git add` moves chosen changes into the staging area, `git commit` records them in history, `git push` publishes, and `git fetch` updates remote-tracking branches without touching your files.[^git-operations-reference] The staging area exists so you can split mixed changes into separate, clean commits, such as a bug fix and a docs update.[^git-tutorial-02-add]

`git diff` compares the working tree with the staging area; `git diff --staged` compares the staging area with the last commit; `git diff HEAD` skips the distinction.[^git-tutorial-06-diff]

## Divergence

When local and remote history have both moved on from a common commit, Git cannot guess whether you want a merge or a rebase, so it asks for an explicit strategy.[^git-operations-reference] See [Syncing a Git branch](branch-sync.md).

## Related

- [Git basic commands](basic-commands.md)
- [Git commit workflow](commit-workflow.md)
- Source: [Essential Git commands for operations](../../sources/git-operations-reference.md)
- Source: [Git basics: git init](../../sources/git-tutorial-00-init.md)
- Source: [Git basics: git add](../../sources/git-tutorial-02-add.md)
- Source: [Git basics: git diff](../../sources/git-tutorial-06-diff.md)

[^git-operations-reference]: Essential Git Commands for Operations
[^git-tutorial-00-init]: Git command-line basics: git init
[^git-tutorial-02-add]: Git command-line basics: git add
[^git-tutorial-06-diff]: Git command-line basics: git diff
