# ZooKeeper

English version: [README.md](README.md)

本模块收录可复用的 ZooKeeper 运维文档。事故处理流程统一放在 `runbooks/`；后续可单独增加架构和日常管理资料，不需要改变 Runbook 路径。

## Runbooks

| Runbook | 说明 |
| --- | --- |
| [磁盘满事务日志恢复](runbooks/disk-full-transaction-log-recovery/README_ZH.md) | 处理单个 ZooKeeper 节点因磁盘满导致本地事务日志不完整的恢复流程。 |
