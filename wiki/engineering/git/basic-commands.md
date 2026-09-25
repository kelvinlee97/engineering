---
type: Command
title: Git basic commands
description: The seven everyday Git commands, init, clone, add, status, commit, log, and diff, with their most useful flags and pitfalls.
tags: [git, cli]
sources:
  - id: git-tutorial-00-init
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/00-init/README.md
    title: "Git command-line basics: git init"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-01-clone
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/01-clone/README.md
    title: "Git command-line basics: git clone"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-02-add
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/02-add/README.md
    title: "Git command-line basics: git add"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-03-status
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/03-status/README.md
    title: "Git command-line basics: git status"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-04-commit
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/04-commit/README.md
    title: "Git command-line basics: git commit"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-05-log
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/05-log/README.md
    title: "Git command-line basics: git log"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: git-tutorial-06-diff
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/06-diff/README.md
    title: "Git command-line basics: git diff"
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
The seven commands a beginner uses daily, in the order they usually come up.[^git-tutorial-00-init]

| Command | Does | Useful flags | Pitfall |
| --- | --- | --- | --- |
| `git init` | Turns a folder into a repository | `-b main` sets the initial branch; `--bare` for a server-side remote | Never delete `.git` and re-init an existing repo; do not init in `~` |
| `git clone` | Copies a remote repository with all history and records it as `origin` | `--branch`, `--depth 1` (shallow), `--recurse-submodules` | A shallow clone lacks history; `git fetch --unshallow` before rebase or full `log` |
| `git add` | Stages chosen changes | `-p` per hunk, `-u` tracked files only, `-A` whole repo | `git add .` can catch `.env` files; re-add a file edited after staging |
| `git status` | Shows branch, staged, unstaged, untracked | `-s`: left column is staging area, right is working tree | Read-only, so run it often |
| `git commit` | Records the staging area as a snapshot with a hash | `-m`, `-a` (tracked files only), `--amend` | Never amend a commit others already pulled; use `git revert` |
| `git log` | Shows history, newest first | `--oneline`, `--graph --all`, `-p`, `--stat`, `--follow -- file` | Press `q` to leave the pager |
| `git diff` | Shows exact line changes | `--staged`, `--stat`, `--word-diff` | Check `--staged` before committing so debug code does not slip in |

Collected from the seven chapters.[^git-tutorial-00-init][^git-tutorial-01-clone][^git-tutorial-02-add][^git-tutorial-03-status][^git-tutorial-04-commit][^git-tutorial-05-log][^git-tutorial-06-diff]

## Reading `git status -s`

`??` is untracked, ` M` modified but not staged, `M ` staged, `MM` staged then modified again, `A ` a new staged file, and ` D` deleted but not staged.[^git-tutorial-03-status]

## Commit messages

The tutorial recommends the Conventional Commits style: a type such as `feat`, `fix`, or `docs`, then a short imperative description under 50 characters, with an optional body explaining why.[^git-tutorial-04-commit] The GitHub guide adds a caution: follow the repository's existing style and do not add prefixes unless the project uses Conventional Commits.[^git-publish-guide]

## Related

- [Git's four places](git-four-places.md)
- [Git commit workflow](commit-workflow.md)
- Source: [Git basics: git init](../../sources/git-tutorial-00-init.md)
- Source: [Git basics: git clone](../../sources/git-tutorial-01-clone.md)
- Source: [Git basics: git add](../../sources/git-tutorial-02-add.md)
- Source: [Git basics: git status](../../sources/git-tutorial-03-status.md)
- Source: [Git basics: git commit](../../sources/git-tutorial-04-commit.md)
- Source: [Git basics: git log](../../sources/git-tutorial-05-log.md)
- Source: [Git basics: git diff](../../sources/git-tutorial-06-diff.md)
- Source: [Publish changes to GitHub](../../sources/git-publish-guide.md)

[^git-tutorial-00-init]: Git command-line basics: git init
[^git-tutorial-01-clone]: Git command-line basics: git clone
[^git-tutorial-02-add]: Git command-line basics: git add
[^git-tutorial-03-status]: Git command-line basics: git status
[^git-tutorial-04-commit]: Git command-line basics: git commit
[^git-tutorial-05-log]: Git command-line basics: git log
[^git-tutorial-06-diff]: Git command-line basics: git diff
[^git-publish-guide]: Publish Changes to GitHub: A Beginner's Guide
