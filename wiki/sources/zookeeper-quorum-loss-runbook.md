---
type: Source Summary
title: ZooKeeper quorum-loss snapshot restore runbook (summary)
description: Summary of the legacy incident runbook for restoring a three-member ZooKeeper ensemble from one approved snapshot after quorum loss.
tags: [zookeeper, runbook, disaster-recovery]
sources:
  - id: zookeeper-quorum-loss-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/runbooks/quorum-loss-snapshot-restore/README.md
    title: ZooKeeper Quorum-Loss Snapshot Restore Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
An incident-only runbook in this repository, `ZooKeeper/runbooks/quorum-loss-snapshot-restore/README.md`, for a three-member ensemble that has lost quorum. It is destructive to local state and may lose writes made after the chosen snapshot.[^zookeeper-quorum-loss-runbook]

## Takeaways

- With no surviving authoritative copy, recovery is a rebuild: every member is restored from the same approved snapshot, one at a time.[^zookeeper-quorum-loss-runbook] See [ZooKeeper quorum-loss restore](../engineering/zookeeper/zookeeper-recovery.md#restoring-after-quorum-loss).

[^zookeeper-quorum-loss-runbook]: ZooKeeper Quorum-Loss Snapshot Restore Runbook, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/runbooks/quorum-loss-snapshot-restore/README.md)
