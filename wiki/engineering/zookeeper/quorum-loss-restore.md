---
type: Playbook
title: ZooKeeper quorum-loss restore
description: Restore a three-member ZooKeeper ensemble that lost quorum by loading the same approved snapshot into every member, one at a time, through a temporary loopback-only admin endpoint.
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
An incident-only procedure for a three-member [ZooKeeper](zookeeper.md) ensemble that has lost quorum and cannot accept updates. With no surviving authoritative copy to resync from, recovery is a rebuild from one approved snapshot. It destroys each member's current local state and may lose writes made after the snapshot.[^zookeeper-quorum-loss-runbook]

## Before starting

- Incident commander, ZooKeeper owner, application owners, and security owner approve it.[^zookeeper-quorum-loss-runbook]
- Client traffic is blocked and applications are stopped or in safe mode.[^zookeeper-quorum-loss-runbook]
- No two members report a healthy quorum; if two do, use [single-member recovery](single-member-recovery.md) instead.[^zookeeper-quorum-loss-runbook]
- One approved snapshot with a verified SHA-512 checksum, an administrator certificate already proven to hold `ALL` on `/`, `serializeLastProcessedZxid` enabled, and a rehearsal in an isolated environment.[^zookeeper-quorum-loss-runbook]

## Steps

1. **Confirm quorum loss and preserve evidence** on all three members. `ruok` is not quorum evidence.[^zookeeper-quorum-loss-runbook]
2. **Enable a temporary AdminServer** on one member through a systemd drop-in: bound to `127.0.0.1:8443`, HTTPS forced, client certificate required. Reach it only through an SSH tunnel, and confirm a request without the client certificate fails.[^zookeeper-quorum-loss-runbook]
3. **Restore member by member.** Stop the member, move both `version-2` directories aside with a timestamp, create empty ones plus the one-time `initialize` marker, start it, `POST` the same verified snapshot to `/commands/restore`, then persist it with `/commands/snapshot?streaming=false` and record `last_zxid`. Never mix snapshots or run members in parallel.[^zookeeper-quorum-loss-runbook]
4. **Re-form quorum** without restarting: wait for election and check for exactly one leader and two followers. If it does not form, stop and escalate rather than retrying as an experiment.[^zookeeper-quorum-loss-runbook]
5. **Close the recovery interface.** Remove the drop-in, restart one member at a time, and confirm nothing listens on `8443`. Run each application's ACL checks, reopen traffic gradually, and keep the preserved directories until the incident closes.[^zookeeper-quorum-loss-runbook]

## Related

- [ZooKeeper production deployment](production-deployment.md)
- [Incident closure criteria](../operations/incident-closure-criteria.md)
- Source: [ZooKeeper quorum-loss snapshot restore runbook](../../sources/zookeeper-quorum-loss-runbook.md)

[^zookeeper-quorum-loss-runbook]: ZooKeeper Quorum-Loss Snapshot Restore Runbook
