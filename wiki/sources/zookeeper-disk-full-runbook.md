---
type: Source Summary
title: ZooKeeper disk-full recovery runbook (summary)
description: Summary of the legacy runbook for rebuilding one ZooKeeper member whose transaction log was truncated by a full disk.
tags: [zookeeper, runbook]
sources:
  - id: zookeeper-disk-full-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/runbooks/disk-full-transaction-log-recovery/README.md
    title: ZooKeeper Disk-Full Recovery Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
A runbook in this repository, `ZooKeeper/runbooks/disk-full-transaction-log-recovery/README.md`, for one member that cannot start after a full disk left its transaction log incomplete.[^zookeeper-disk-full-runbook]

## Takeaways

- A truncated log on one member is a local storage problem while the others hold quorum; move the damaged data aside and let the member resync.[^zookeeper-disk-full-runbook] See [ZooKeeper single-member recovery](../engineering/zookeeper/single-member-recovery.md).

[^zookeeper-disk-full-runbook]: ZooKeeper Disk-Full Recovery Runbook
