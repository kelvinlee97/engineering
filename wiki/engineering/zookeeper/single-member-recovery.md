---
type: Playbook
title: ZooKeeper single-member recovery
description: Rebuild one ZooKeeper member whose transaction log a full disk truncated, by moving its data aside and letting it resync from a healthy quorum.
tags: [zookeeper, runbook, incident]
sources:
  - id: zookeeper-disk-full-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/runbooks/disk-full-transaction-log-recovery/README.md
    title: ZooKeeper Disk-Full Recovery Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
Use this when exactly one [ZooKeeper](zookeeper.md) member cannot start because a full disk left its transaction log incomplete, typically with `Last transaction was partial.`, `Unable to load database on disk`, or `java.io.EOFException`.[^zookeeper-disk-full-runbook]

Freeing disk space removes the write blockage but does not repair a truncated log, and looping on restarts does not help.[^zookeeper-disk-full-runbook]

## Preconditions

Proceed only if exactly one member is damaged, the others form a healthy quorum, `dataDir` and any `dataLogDir` are known, the damaged member is stopped, and there is capacity for a backup and a fresh sync. Stop and escalate if quorum is unavailable, freshness is uncertain, or more than one member needs rebuilding.[^zookeeper-disk-full-runbook]

## Steps

1. **Confirm quorum on the healthy members.** Expect one leader and one follower, `Outstanding: 0`, and matching or converging `Zxid` and `Node count`. `imok` from `ruok` only proves the process is bound, not that it is in quorum. Do not widen the four-letter-word allowlist during the incident; on a TLS-only port use `zkServer.sh status` with TLS settings.[^zookeeper-disk-full-runbook]
2. **Read the real paths** from `zoo.cfg` and `myid`; confirm no `QuorumPeerMain` process or listener remains.[^zookeeper-disk-full-runbook]
3. **Move, do not delete,** the damaged `version-2` to a timestamped name, keeping `myid` unchanged; move a distinct `dataLogDir` copy separately. Do not create a new `version-2` by hand.[^zookeeper-disk-full-runbook]
4. **Start the member** and look for leader discovery and a DIFF, SNAP, or TRUNC sync ending in the follower role.[^zookeeper-disk-full-runbook]

## Acceptance

One leader, two followers, `Outstanding: 0`, matching `Node count`, and matching or converging `Zxid`. Then repeat the original dependent-service request (the runbook loops it 20 times), because ZooKeeper recovering does not prove it was the only cause.[^zookeeper-disk-full-runbook]

Never clear `version-2` on two or more members, copy another member's `myid`, `chmod 777`, or delete the backup right after the member rejoins.[^zookeeper-disk-full-runbook]

## Related

- [ZooKeeper quorum-loss restore](quorum-loss-restore.md): when more than one member is lost.
- [Incident closure criteria](../operations/incident-closure-criteria.md)
- Source: [ZooKeeper disk-full recovery runbook](../../sources/zookeeper-disk-full-runbook.md)

[^zookeeper-disk-full-runbook]: ZooKeeper Disk-Full Recovery Runbook
