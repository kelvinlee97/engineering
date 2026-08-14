# ZooKeeper

Chinese version: [README_ZH.md](README_ZH.md)

This module contains ZooKeeper tutorials and operational usage guides. Incident procedures under `runbooks/` remain separate from beginner material.

## Guides

| Guide | Description |
| --- | --- |
| [ZooKeeper beginner tutorial](guides/getting-started/README.md) | Learn what ZooKeeper is, when to use it, and basic local CLI operations. |
| [Production deployment baseline](guides/production-deployment/README.md) | Deployment and TLS-aware status baseline for incident runbooks. |

## Runbooks

| Runbook | Description |
| --- | --- |
| [Disk-full transaction-log recovery](runbooks/disk-full-transaction-log-recovery/README.md) | Recover one ZooKeeper member when a full disk leaves its local transaction log incomplete. |
| [Quorum-loss snapshot restore](runbooks/quorum-loss-snapshot-restore/README.md) | Restore a three-member ensemble from an approved snapshot after quorum loss. |
