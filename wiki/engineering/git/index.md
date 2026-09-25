# Concept

* [Git's four places](git-four-places.md) - Git moves work between the working tree, the staging area, the local repository, and a remote; most commands inspect or move content between them.

# Pattern

* [Git commit workflow](commit-workflow.md) - Review what changed, stage explicit paths, review what is staged, commit, and confirm the result before pushing.
* [Keeping secrets out of Git](secrets-in-git.md) - Never commit credentials; if one leaks, revoke or rotate it first, because deleting the file or rewriting history cannot prove it was not copied.

# Playbook

* [GitHub pull request workflow](pull-request-workflow.md) - Publish a change on GitHub through a focused branch, a reviewed pull request, passing checks, and a merge, then clean up.
* [Syncing a Git branch](branch-sync.md) - Fetch first, compare local and upstream commits, then choose fast-forward, rebase, or merge deliberately, and resolve conflicts on purpose.
* [Undoing and recovering in Git](undo-and-recovery.md) - Choose between restore, reset, revert, and reflog by whether the work is shared, and check a pre-flight list before any destructive Git operation.

# Command

* [Git basic commands](basic-commands.md) - The seven everyday Git commands, init, clone, add, status, commit, log, and diff, with their most useful flags and pitfalls.
