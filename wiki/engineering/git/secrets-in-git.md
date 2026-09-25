---
type: Pattern
title: Keeping secrets out of Git
description: Never commit credentials; if one leaks, revoke or rotate it first, because deleting the file or rewriting history cannot prove it was not copied.
tags: [git, security]
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
  - id: git-tutorial-02-add
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/02-add/README.md
    title: "Git command-line basics: git add"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:30:00Z }
status: draft
---
Tokens, private keys, `.env` files, `kubeconfig`, cloud credentials, production backups, and customer data never belong in a commit.[^git-operations-reference]

## Why cleanup does not work

- `.gitignore` only affects files that are not yet tracked; adding a rule does not remove a committed file.[^git-operations-reference]
- `git rm --cached` stops tracking a file from now on, but leaves it in history and does not invalidate a leaked credential.[^git-operations-reference]
- Making a repository private after pushing a secret does not make the secret safe.[^git-publish-guide]

## If a credential leaks

Revoke or rotate it first, then assess access logs and exposure, and only then use the platform's approved history-cleanup process.[^git-operations-reference]

## Prevention

`git add .` will happily pick up `.env` files, so check `git status` before committing and add sensitive files to `.gitignore`.[^git-tutorial-02-add] Stage explicit paths and review `git diff --staged`.[^git-publish-guide]

## Related

- [Git commit workflow](commit-workflow.md)
- Source: [Essential Git commands for operations](../../sources/git-operations-reference.md)
- Source: [Publish changes to GitHub](../../sources/git-publish-guide.md)
- Source: [Git basics: git add](../../sources/git-tutorial-02-add.md)

[^git-operations-reference]: Essential Git Commands for Operations
[^git-publish-guide]: Publish Changes to GitHub: A Beginner's Guide
[^git-tutorial-02-add]: Git command-line basics: git add
