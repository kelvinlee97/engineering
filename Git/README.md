# Essential Git Commands for Operations

Chinese version: [README_ZH.md](README_ZH.md)

This guide is for operations engineers who are comfortable with a terminal and basic Git usage. Its core rule is simple: **inspect first, then change; on shared branches, prefer an auditable new corrective commit over rewriting history.**

It covers native Git commands only. Buttons, branch-protection rules, and CI configuration in GitHub, GitLab, or Bitbucket are platform features, not Git itself.

## Contents

- [Keep this model in mind](#keep-this-model-in-mind)
- [Before every change: inspect the facts](#before-every-change-inspect-the-facts)
- [Local changes and commits](#local-changes-and-commits)
- [Branches, synchronisation, and conflicts](#branches-synchronisation-and-conflicts)
- [Releases, tags, and traceability](#releases-tags-and-traceability)
- [Rollback, recovery, and investigation](#rollback-recovery-and-investigation)
- [High-risk operations and security boundaries](#high-risk-operations-and-security-boundaries)
- [Minimum daily command set](#minimum-daily-command-set)
- [Pre-flight checklist for high-risk operations](#pre-flight-checklist-for-high-risk-operations)

## Keep this model in mind

```text
Working tree --git add--> Staging area (index) --git commit--> Local repository
      ^                                                               |
      |---------------------- git restore / reset --------------------|
                                                                      |
Remote repository <-------------------------- git push ----------------+
    |
    +------------------------------- git fetch -----------------> Remote-tracking branches
```

- **Working tree**: the files currently visible and edited on your machine.
- **Staging area**: the exact file content prepared for the next commit.
- **Local repository**: commit history on this machine; `HEAD` normally identifies the latest commit of the current branch.
- **Remote repository**: for example, `origin`. `origin/main` is your *local record* of the remote branch; run `fetch` before relying on it.
- **Divergence**: local and remote history both progressed from the same commit. Git cannot know whether you want a merge or rebase, so it requires an explicit integration strategy.

## Before every change: inspect the facts

The following commands are observational. `fetch` updates local remote-tracking references, but does not merge into the working tree or push to the remote.

| Purpose | Command | Notes |
|---|---|---|
| Inspect working tree, index, and upstream | `git status` | Run first: confirm branch, uncommitted files, and ahead/behind state. |
| Compact, automation-friendly status | `git status --short --branch` | Use `--porcelain` for a format a script must parse. |
| View all branches and the commit graph | `git log --oneline --graph --decorate --all` | Especially useful for tags, merges, and divergence. |
| View unstaged changes | `git diff` | Compares working tree with index. |
| View staged changes | `git diff --staged` | **Run before committing.** |
| Inspect one commit | `git show <commit>` | Confirm a change before review, rollback, or investigation. |
| View local branches and upstreams | `git branch -vv` | Shows which remote branch each branch tracks. |
| Confirm remote URLs | `git remote -v` | Check the actual target before pushing. |
| Refresh remote state and prune deleted refs | `git fetch --prune` | Safe starting point for synchronisation; it is not `pull`. |

Official references: [git-status](https://git-scm.com/docs/git-status), [git-diff](https://git-scm.com/docs/git-diff), [git-log](https://git-scm.com/docs/git-log), and [git-fetch](https://git-scm.com/docs/git-fetch).

## Local changes and commits

### A safe commit loop

```bash
git diff
git add path/to/file
git diff --staged
git commit -m "feat: explain the change"
git show --stat HEAD
```

1. Use `git diff` to confirm what actually changed.
2. Stage precise paths with `git add path/to/file`; do not accidentally include unrelated files.
3. Use `git diff --staged` to review exactly what the commit will contain.
4. `git commit` creates local history only; it does not publish to the remote.
5. Use `git show --stat HEAD` to confirm the resulting commit and scope.

### Discard, amend, and temporarily save work

| Need | Command | Effect and boundary |
|---|---|---|
| Discard an unstaged change to one file | `git restore path/to/file` | Overwrites that working-tree file; inspect it first with `git diff -- path/to/file`. |
| Unstage a file but retain its working-tree change | `git restore --staged path/to/file` | Does not discard the edit. |
| Change the latest **unshared** commit | `git commit --amend` | Rewrites its commit ID; do not casually use after sharing or pushing. |
| Temporarily set aside tracked changes | `git stash push -m "reason"` | Does not include untracked or ignored files. Inspect with `git stash list`; `stash pop` applies and removes an entry and can conflict. |
| Also include reviewed untracked files | `git stash push --include-untracked -m "reason"` | Includes untracked files, but not ignored files. |
| Apply a stash while retaining it | `git stash apply stash@{0}` | Confirm that the target branch is compatible first. |

Official references: [git-add](https://git-scm.com/docs/git-add), [git-restore](https://git-scm.com/docs/git-restore), [git-commit](https://git-scm.com/docs/git-commit), and [git-stash](https://git-scm.com/docs/git-stash).

## Branches, synchronisation, and conflicts

### Create, switch, and publish a branch

```bash
git switch -c feature/example
git push --set-upstream origin feature/example
```

`--set-upstream` (or `-u`) associates the local branch with its remote branch, allowing later `git push` and `git pull` without arguments. Do not assume that the current branch or `origin` is correct: inspect `git status` and `git remote -v` first.

### Sync safely: fetch first, then select a strategy

```bash
git fetch --prune
git status
git log --oneline --graph --decorate HEAD..@{upstream}
git log --oneline --graph --decorate @{upstream}..HEAD
```

The two `log` commands list commits present only on the upstream and only locally, respectively. Choose based on those facts:

| Situation | Recommended action | Why |
|---|---|---|
| Local has no unique commits and is simply behind | `git pull --ff-only` | Allows only a fast-forward; fails on divergence instead of creating an unexpected merge. |
| A divergent personal, unshared feature branch | `git pull --rebase` | Replays your commits on top of the updated remote branch, keeping history linear. |
| A shared branch where merge integration is preferred | `git pull --no-rebase` or `git merge @{upstream}` | Uses merge integration without rewriting shared commits; it creates a merge commit only when history cannot fast-forward (unless a different merge policy is configured). |
| A merge commit must remain visible even when fast-forward is possible | `git pull --no-rebase --no-ff` or `git merge --no-ff @{upstream}` | Forces a merge commit; use only when the team's history policy requires the extra node. |
| Neither side has new commits | Do nothing | Do not create activity merely to "sync". |

`git pull` fetches first, then integrates according to its configuration or supplied option. The message `Need to specify how to reconcile divergent branches` means Git needs your explicit decision between merge, rebase, or fast-forward-only; it does not mean data is corrupt. For a personal branch, `git pull --rebase` is often appropriate only after confirming no one else depends on its local history. For a shared branch, prefer merge or the team's established process.

### Resolve a conflict

**During a rebase:**

```bash
git status
# Edit the conflict, remove conflict markers, and validate the intended result.
git add path/to/resolved-file
git rebase --continue

# Stop safely if unsure or the direction is wrong.
git rebase --abort
```

**During a merge:**

```bash
git status
# Edit and validate the conflict.
git add path/to/resolved-file
git commit

# Stop safely if unsure.
git merge --abort
```

Do not blindly choose one side merely to remove conflict markers. A conflict represents different changes to the same meaning; run relevant checks after resolving it.

Official references: [git-switch](https://git-scm.com/docs/git-switch), [git-pull](https://git-scm.com/docs/git-pull), [git-merge](https://git-scm.com/docs/git-merge), and [git-rebase](https://git-scm.com/docs/git-rebase).

## Releases, tags, and traceability

A Git tag identifies a source commit; **it does not prove that deployment or production verification succeeded**. Use an annotated tag for a release candidate or release:

```bash
git status
git show --stat HEAD
git tag -a v1.2.0 -m "Release v1.2.0"
git show v1.2.0
git push origin v1.2.0
```

Compare release ranges with:

```bash
git log --oneline v1.1.0..v1.2.0
git diff --stat v1.1.0 v1.2.0
git describe --tags --always
```

- `git push origin <tag>` publishes one explicit tag. `git push origin --tags` publishes every local tag and can unintentionally include tags not ready for release.
- CI/CD should retain the input commit SHA, tag, artifact identifier, and deployment result, so you can answer what is running.
- A shallow clone can omit old commits or tags, making `describe`, cross-version comparisons, `blame`, and `bisect` incomplete. Confirm history depth during an incident.

Official references: [git-tag](https://git-scm.com/docs/git-tag) and [git-describe](https://git-scm.com/docs/git-describe).

## Rollback, recovery, and investigation

### A pushed or deployed mistake: prefer revert

```bash
git show <bad-commit>
git revert <bad-commit>
git show HEAD
git branch --show-current
git branch -vv
git remote -v
git push <confirmed-remote> HEAD:<confirmed-branch>
```

`git revert` creates a new inverse commit and preserves an auditable history, making it appropriate for shared branches and post-release fixes. Replace `<confirmed-remote>` and `<confirmed-branch>` only after `git branch --show-current`, `git branch -vv`, and `git remote -v` confirm the current branch and its intended remote target. `HEAD:<confirmed-branch>` pushes the revert you just created, not a local branch selected by an implicit push rule. Reverting a merge commit requires choosing a mainline parent, such as `git revert -m 1 <merge-commit>`; confirm the merge direction and impact with the team first.

### A local mistaken commit: know what reset changes

| Command | Commit history | Index | Working tree | Appropriate use |
|---|---|---|---|---|
| `git reset --soft HEAD~1` | Moves back | Keeps | Keeps | Reorganise the latest unshared commit. |
| `git reset --mixed HEAD~1` | Moves back | Clears | Keeps | Restage selected content; this is the default mode. |
| `git reset --hard HEAD~1` | Moves back | Overwrites | Overwrites | **High risk**; only discard confirmed-unneeded, unshared work. |

`reset` moves the current branch reference. Do not reset and force-push already shared `main` or release branches: it breaks collaborators' common history. On shared branches, use `revert` for a business rollback.

### Recover a deleted branch or a bad reset with reflog

```bash
git reflog
git show <recovered-commit>
git switch -c recovery/example <recovered-commit>
```

`reflog` records where local references such as `HEAD` previously pointed. First inspect a candidate commit, then protect it by creating a **new recovery branch** rather than overwriting a branch in use. Reflog is local, not a remote backup, and is subject to expiration.

### Find the commit that introduced a problem

```bash
git blame -- path/to/file
git bisect start
git bisect bad <known-bad>
git bisect good <known-good>
# Run a repeatable check for each commit selected by Git, then mark it good or bad.
git bisect reset
```

`blame` identifies the last commit that changed a line; it does not assign responsibility. `bisect` uses binary search to narrow a regression to a commit. Always run `git bisect reset` at the end to return to the starting branch.

Official references: [git-revert](https://git-scm.com/docs/git-revert), [git-reset](https://git-scm.com/docs/git-reset), [git-reflog](https://git-scm.com/docs/git-reflog), [git-blame](https://git-scm.com/docs/git-blame), and [git-bisect](https://git-scm.com/docs/git-bisect).

## High-risk operations and security boundaries

| Operation | Risk | Safer practice |
|---|---|---|
| `git push --force` | May overwrite other people's remote commits | When a personal branch must be rewritten, use `git push --force-with-lease`; fetch first and verify the remote target. |
| `git reset --hard` | Discards working-tree, index, or unshared-commit content | Inspect `status`, `diff`, and `reflog`; create a branch or stash when retention is needed. |
| Delete a remote branch | Affects collaborators and automation | Confirm PRs, deployments, and protection rules; use an explicit branch name and obtain authorisation. |
| `git clean -fd` | Deletes untracked files and directories | Preview with `git clean -nd`; do not treat it as routine cleanup. |
| Rewrite shared history | Breaks collaborators' common base | Prefer `revert`; schedule and coordinate any unavoidable rewrite. |

`--force-with-lease` pushes only if the remote ref still matches what you expect, so it is safer than bare `--force`. It is not permission to force-push a shared branch.

### Secrets and sensitive files

- Never commit tokens, private keys, `.env`, `kubeconfig`, cloud credentials, production backups, or customer data.
- `.gitignore` affects only files that are **not yet tracked**; adding a rule does not make an already committed file disappear.
- `git rm --cached path/to/file` can stop tracking a sensitive file going forward, but it neither removes prior history nor invalidates a leaked credential.
- If credentials leak: **revoke or rotate them immediately first**, then assess access logs, scope of exposure, and the platform-approved history-cleanup process. Deleting a file or rewriting history cannot guarantee that an old credential was not copied.

Official references: [git-push](https://git-scm.com/docs/git-push), [git-clean](https://git-scm.com/docs/git-clean), and [gitignore](https://git-scm.com/docs/gitignore).

## Minimum daily command set

```bash
# Start work or prepare to synchronise.
git status
git fetch --prune
git status

# Inspect and commit.
git diff
git add path/to/file
git diff --staged
git commit -m "type: short description"

# Confirm history and target before pushing.
git branch --show-current
git branch -vv
git remote -v
git push <confirmed-remote> HEAD:<confirmed-branch>
```

## Pre-flight checklist for high-risk operations

- [ ] Am I in the correct repository and branch? (`git status`, `git remote -v`)
- [ ] Does the working tree or index contain anything to preserve? (`git diff`, `git diff --staged`)
- [ ] Have I obtained current remote state? (`git fetch --prune`)
- [ ] Is this a personal unshared branch, or a shared/protected branch?
- [ ] Can a safer mechanism such as `revert`, a new branch, or `--force-with-lease` achieve the goal?
- [ ] What is my recovery point if the operation or judgement is wrong? (commit, tag, stash, reflog, or backup)
- [ ] Does this affect production, releases, or credentials? If so, have I followed the authorised team process?

## Official documentation

Git behavior evolves between versions. Before an unfamiliar or high-risk operation, read the relevant official manual at <https://git-scm.com/docs>.
