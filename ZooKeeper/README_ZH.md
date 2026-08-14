# ZooKeeper

English version: [README.md](README.md)

本模块收录 ZooKeeper 教程与运维使用指南。`runbooks/` 中的事故处理流程与新手材料保持分离。

## Guides

| 指南 | 说明 |
| --- | --- |
| [ZooKeeper 新手教程](guides/getting-started/README_ZH.md) | 了解 ZooKeeper 是什么、何时使用，以及基本的本地 CLI 操作。 |
| [生产部署基线](guides/production-deployment/README_ZH.md) | 供事故 Runbook 使用的部署与 TLS-aware 状态检查基线。 |

## Runbooks

| Runbook | 说明 |
| --- | --- |
| [磁盘满事务日志恢复](runbooks/disk-full-transaction-log-recovery/README_ZH.md) | 处理单个 ZooKeeper 节点因磁盘满导致本地事务日志不完整的恢复流程。 |
| [Quorum-loss 快照恢复](runbooks/quorum-loss-snapshot-restore/README_ZH.md) | quorum 丢失后从获批准快照恢复三成员 ensemble。 |
