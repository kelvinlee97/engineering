---
type: Pattern
title: Git commit workflow
description: Review what changed, stage explicit paths, review what is staged, commit, and confirm the result before pushing.
tags: [git]
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
  - id: git-tutorial-06-diff
    resource: https://github.com/kelvinlee97/engineering/blob/main/Git/06-diff/README.md
    title: "Git command-line basics: git diff"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:30:00Z }
status: draft
---
A safe commit is a short loop of look, stage precisely, look again, commit, confirm.[^git-operations-reference]

1. `git diff` to see what actually changed.[^git-operations-reference]
2. `git add path/to/file` with explicit paths, so unrelated files stay out; the GitHub guide calls this safer for beginners than `git add .`.[^git-operations-reference][^git-publish-guide]
3. `git diff --staged` to review exactly what the commit will contain; forgetting it is how debug calls and temporary code slip into commits.[^git-operations-reference][^git-tutorial-06-diff]
4. `git commit`, which creates local history only.[^git-operations-reference]
5. `git show --stat HEAD` to confirm the commit and its scope.[^git-operations-reference]

Before pushing, confirm the branch and target with `git branch --show-current`, `git branch -vv`, and `git remote -v`, then push to an explicit remote and branch.[^git-operations-reference]

If you staged the wrong file, `git restore --staged path/to/file` keeps the edit but removes it from the next commit.[^git-publish-guide]

## Related

- [Keeping secrets out of Git](secrets-in-git.md)
- [GitHub pull request workflow](pull-request-workflow.md)
- Source: [Essential Git commands for operations](../../sources/git-operations-reference.md)
- Source: [Publish changes to GitHub](../../sources/git-publish-guide.md)
- Source: [Git basics: git diff](../../sources/git-tutorial-06-diff.md)

[^git-operations-reference]: Essential Git Commands for Operations
[^git-publish-guide]: Publish Changes to GitHub: A Beginner's Guide
[^git-tutorial-06-diff]: Git command-line basics: git diff
