# Rollback

Only on an explicit rollback request, branch from `origin/<default>`, revert the merged squash commit, push it, and use the normal PR flow. Use `git revert -m 1` only when reverting a merge commit.
