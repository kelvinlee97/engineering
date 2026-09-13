# Publish Changes to GitHub: A Beginner's Guide

Chinese version: [README_ZH.md](README_ZH.md)

Publishing code safely is not one command. The normal path is:

```text
edit -> inspect -> test -> commit -> push a branch -> open a pull request -> merge
```

Git records changes on your computer. GitHub hosts the remote repository and adds pull
requests, reviews, and automated checks. A commit is not published until you push it, and a
pushed branch does not change `main` until it is merged.

## Before you start

You need Git, a GitHub account, and a local clone of the repository. Configure the name and
email recorded in new commits once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

If you use [GitHub CLI](https://cli.github.com/), its browser-based login is the simplest
authentication setup for many beginners:

```bash
gh auth login
gh auth status
```

Never put passwords, access tokens, private keys, `.env` files, or private customer data in a
commit. Making a repository private after pushing a secret does not make the secret safe;
revoke or rotate it.

## The everyday workflow

The examples use `main` as the base branch and `origin` as the remote. Repositories can use
different names, so confirm them instead of assuming:

```bash
git status
git remote -v
git branch --show-current
```

### 1. Start from an up-to-date base branch

Finish or stash any current work first, then update `main` without creating an accidental
merge commit:

```bash
git switch main
git pull --ff-only
```

If `--ff-only` fails, stop and inspect the history. Do not force-push or reset a shared branch
just to make the warning disappear.

### 2. Create a focused branch

```bash
git switch -c docs/explain-squash-merge
```

Use a short name that describes the change, such as `fix/login-timeout` or
`docs/install-guide`. Keep one branch and pull request focused on one purpose.

### 3. Make the change and run the relevant check

Follow the repository's `README`, `CONTRIBUTING.md`, or `AGENTS.md`. Run the smallest test,
formatter, build, or documentation check that covers your change. Then inspect the result:

```bash
git status
git diff
```

`git status` shows which files changed. `git diff` shows the actual unstaged edits. Look for
debug output, generated files, secrets, and unrelated changes before continuing.

### 4. Stage only the intended files

```bash
git add path/to/file another/file
git diff --staged
```

Staging selects the exact content for the next commit. Explicit paths are safer for beginners
than `git add .`, which can collect unrelated files. If you staged the wrong file, keep its
edit but remove it from the next commit with:

```bash
git restore --staged path/to/file
```

### 5. Create a clear commit

```bash
git commit -m "docs: explain the GitHub publishing workflow"
git show --stat HEAD
```

A useful message says what the commit accomplishes. Use the repository's existing message
style; do not add `feat:` or another prefix unless that project uses Conventional Commits.

One pull request may contain several meaningful commits. They do not need to be perfect if the
repository uses squash merge, because GitHub can combine them when merging.

### 6. Push the branch

Confirm the destination, then publish the current branch:

```bash
git remote -v
git push --set-upstream origin HEAD
```

`--set-upstream` links the local branch to its remote branch. Later pushes from this branch can
usually use `git push`. Pushing the branch still does not merge it into `main`.

### 7. Open a pull request

Open the repository on GitHub and select **Compare & pull request**, or use GitHub CLI:

```bash
gh pr create --web
```

Before submitting, confirm:

- **Base** is the branch you want to change, usually `main`.
- **Compare/head** is your feature branch.
- The title explains the outcome.
- The description says what changed, why, and how you checked it.
- `Files changed` contains no unrelated or sensitive content.

A small description is enough:

```markdown
## Summary

- Explain the branch-to-PR publishing workflow for beginners.
- Add safe checks before commit and push.

## Checks

- Reviewed Markdown links and formatting.
```

If the work is not ready, open a draft pull request. New commits pushed to the same branch are
added to the existing pull request automatically.

### 8. Respond to review and checks

Make requested edits locally, check them, commit them, and push again:

```bash
git status
git diff
# edit and run the relevant check
git add path/to/file
git diff --staged
git commit -m "docs: clarify branch selection"
git push
```

Do not open a new pull request for each revision. Watch the GitHub **Checks** tab and fix failed
checks before merging. Resolve review conversations only after the concern is addressed.

### 9. Merge and clean up

Merge only after required reviews and checks pass. If the repository offers **Squash and
merge**, it turns all pull-request commits into one commit on the base branch. This is useful
when the branch contains small correction commits and the project wants a compact `main`
history. Use the merge method required by the repository; not every project enables squash.

After the pull request is merged:

```bash
git switch main
git pull --ff-only
git fetch --prune
```

Delete the remote branch with GitHub's **Delete branch** button if the repository does not do
it automatically. For a regular merge, delete the local branch with
`git branch -d docs/explain-squash-merge`. After a squash merge, Git usually cannot prove that
the original commits were merged; confirm the PR is merged, the branch is pushed, and its
worktree is clean before using `git branch -D docs/explain-squash-merge`.

## Contributing when you cannot push to the repository

Open-source projects commonly use the fork-and-pull model:

1. Fork the project on GitHub.
2. Clone your fork.
3. Add the original repository as `upstream`.
4. Push your feature branch to your fork (`origin`).
5. Open a pull request from your fork to the original repository.

```bash
git clone https://github.com/YOUR-USER/PROJECT.git
cd PROJECT
git remote add upstream https://github.com/OWNER/PROJECT.git
git fetch upstream
git switch -c docs/example upstream/main
# edit, check, stage, and commit
git push -u origin HEAD
gh pr create --web
```

Here, `origin` is your fork and `upstream` is the original project. Always read the project's
contribution guide before making a large change.

## Optional: use a worktree for parallel work

`git worktree` gives another branch its own directory while sharing the same repository
history. It is useful when unfinished work must remain open while you prepare a separate fix
or pull request. It is not required for normal GitHub publishing.

From the main repository directory:

```bash
git fetch origin
git worktree add -b fix/login-timeout ../project-login-timeout origin/main
cd ../project-login-timeout
# edit, check, stage, commit, push, and open the PR as usual
git push -u origin HEAD
gh pr create --web
```

After the pull request is merged, leave the worktree directory and remove it through Git:

```bash
cd ../project
git worktree remove ../project-login-timeout
git fetch --prune
```

Do not delete the directory manually while it contains uncommitted work. Check with
`git status` inside the worktree first. Each branch can be checked out in only one worktree at
a time. Then delete the branch with `git branch -d fix/login-timeout`, or use `-D` only after a
verified squash merge as described above.

## Optional: automate only after you understand the steps

Anthropic's public Claude Code repository includes a `commit-commands` plugin with
`/commit-push-pr`. Its workflow inspects changes, creates a branch when needed, commits, pushes
to `origin`, and opens a pull request with `gh pr create`.

That command is a convenient wrapper, not a replacement for review. Before accepting an
automated commit or push, verify the branch, remote, diff, commit message, test result, and PR
base. Tool availability and behaviour can change between versions, so follow the plugin's
current README rather than assuming the command is installed.

## Common beginner mistakes

| Mistake | Better habit |
|---|---|
| Working directly on `main` | Create a short-lived feature branch. |
| Running `git add .` without inspection | Stage explicit paths and run `git diff --staged`. |
| Treating commit and push as the same action | Remember: commit is local; push publishes a branch. |
| Pushing secrets and deleting them later | Keep them out of Git; rotate any exposed credential. |
| Force-pushing to fix rejection | Fetch and understand the divergence first. |
| Opening a PR with the wrong base | Check base and compare branches before submission. |
| Merging while checks fail | Fix the failure or document an approved exception. |
| Using an AI-generated PR description unchecked | Compare every claim with the actual diff and checks. |

## Quick checklist

```text
[ ] I am on a focused branch, not main.
[ ] git status and git diff show only intended changes.
[ ] Relevant checks pass.
[ ] git diff --staged matches the commit message.
[ ] The remote and branch are correct before push.
[ ] The PR targets the correct base and explains the change and checks.
[ ] Required review and CI pass before merge.
[ ] I update main and delete the merged local branch.
```

## Official references

- GitHub Docs: [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- GitHub Docs: [Pushing commits to a remote repository](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)
- GitHub Docs: [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
- GitHub Docs: [Merging a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)
- GitHub Docs: [About pull request merges](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges)
- GitHub CLI: [`gh auth login`](https://cli.github.com/manual/gh_auth_login) and [`gh pr create`](https://cli.github.com/manual/gh_pr_create)
- Git: [`git worktree`](https://git-scm.com/docs/git-worktree)
- Anthropic: [Claude Code commit commands](https://github.com/anthropics/claude-code/tree/main/plugins/commit-commands)
