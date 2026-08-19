# Amazon QLDB - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Quantum Ledger Database（Amazon QLDB）曾是具有追加式日志、密码学校验和 PartiQL 查询的完全托管账本数据库。**Amazon QLDB 已于 2025 年 7 月 31 日停止支持。** 官方指引现有客户把 QLDB 账本迁移到 Amazon Aurora PostgreSQL。请勿再基于 QLDB 构建新系统。

## 核心概念（迁移背景）

- **账本（Ledger）**：QLDB 数据库资源，保存不可变、追加式的日志。
- **日志（Journal）**：对所有变更以密码学链式记录的日志。
- **摘要与校验（Digest and verification）**：基于哈希的完整性校验，证明日志未被篡改。
- **PartiQL**：读写文档所用的 SQL 兼容查询语言。
- **迁移路径**：官方文档化的替代方案是把账本工作负载迁移到 Amazon Aurora PostgreSQL（追加/审计设计）。

## 常用操作（针对存量账本）

```bash
# 列出和查看存量账本
aws qldb list-ledgers
aws qldb describe-ledger --name my-ledger

# 退役前把日志导出到 S3
aws qldb export-journal-to-s3 --name my-ledger \
  --inclusive-start-time 2025-01-01T00:00:00Z \
  --exclusive-end-time 2026-08-19T00:00:00Z \
  --s3-export-configuration Bucket=export-bucket,Prefix=qldb/

# 删除存量账本
aws qldb delete-ledger --name my-ledger
```

## 最佳实践

- 不要用 QLDB 开启新项目；它已停止支持。评估 Amazon Aurora PostgreSQL 或其他账本/审计架构。
- 如果还有存量 QLDB 账本，请先规划并执行到 Aurora PostgreSQL 的迁移，再退役。
- 删除前把日志导出到 S3 作为留存记录。
- 维护账本和 IAM 权限清单，确保无用账本被干净移除。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无法创建新账本 | 符合预期：服务已停止支持，不再提供新建能力。 |
| 迁移问题 | 按官方指南执行 QLDB 账本到 Amazon Aurora PostgreSQL 的迁移。 |
| 退役 | 先把日志导出到 S3，再删除账本并清理相关 IAM 角色/策略。 |

## 配额

该服务已停止支持（2025 年 7 月 31 日结束）。原容量配额不再适用于新用量；请规划退役和迁移。

## 官方参考

- [Amazon QLDB 开发者指南（终止支持通知）](https://docs.aws.amazon.com/qldb/latest/developerguide/what-is.html)
- [迁移 Amazon QLDB 账本到 Amazon Aurora PostgreSQL](https://docs.aws.amazon.com/qldb/latest/developerguide/migrate-to-aurora-postgresql.html)
- [AWS CLI：qldb 命令](https://docs.aws.amazon.com/cli/latest/reference/qldb/)
