# Amazon RDS - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Relational Database Service（Amazon RDS）让你在云中更容易地搭建、运维和扩展关系型数据库。AWS 负责备份、软件补丁、自动故障检测与恢复。

## 核心概念

- **数据库实例（DB instance）**：基本单元，云中的隔离数据库环境。
- **引擎**：IBM Db2、MariaDB、Microsoft SQL Server、MySQL、Oracle、PostgreSQL（Aurora 单独成档）。
- **实例类**：通用型（`db.m*`）、内存优化（`db.z*`、`db.x*`、`db.r*`）、计算优化（`db.c*`）、突发型（`db.t*`）。
- **存储**：通用型 SSD 和预置 IOPS SSD；magnetic 已弃用（2026-07-01 后不能再恢复到 magnetic）。
- **Multi-AZ**：另一可用区的同步备用实例用于故障转移；Multi-AZ DB cluster 额外提供只读节点。
- **只读副本**：异步扩展读流量。
- **备份**：自动备份 + 时间点恢复（PITR），以及手动快照。
- **安全**：VPC + 安全组、IAM 认证、静态加密（KMS）、传输 TLS。

## 常用操作（AWS CLI）

```bash
# 创建数据库实例
aws rds create-db-instance --db-instance-identifier mydb \
  --db-instance-class db.m7g.large --engine postgres \
  --master-username admin --master-user-password 'ChangeMe123!' \
  --allocated-storage 100 --db-subnet-group-name my-db-subnet-group

# 查看
aws rds describe-db-instances --db-instance-identifier mydb
aws rds describe-db-engine-versions --engine postgres

# 修改 / 重启
aws rds modify-db-instance --db-instance-identifier mydb --allocated-storage 200 --apply-immediately
aws rds reboot-db-instance --db-instance-identifier mydb

# 备份
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snapshot
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier mydb-restored --db-snapshot-identifier mydb-snapshot

# 只读副本
aws rds create-db-instance-read-replica --db-instance-identifier mydb-ro --source-db-instance-identifier mydb

# 删除（仅测试环境可 skip-final-snapshot）
aws rds delete-db-instance --db-instance-identifier mydb --skip-final-snapshot
```

## 最佳实践

- 生产用 **Multi-AZ**，读扩展用**只读副本**。
- 开启**自动备份 + 时间点恢复**；长期保留用手动快照。
- 用**安全组**限制网络访问；没有充分理由不要开启 public accessibility。
- 开启**静态加密（KMS）**并要求 TLS 连接。
- 数据库用户最小权限；支持时用 IAM 认证。
- 用 CloudWatch、Enhanced Monitoring、Performance Insights 监控；用参数组调优。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 连接拒绝/超时 | 检查安全组来源规则、VPC/子网路由、public accessibility。 |
| 存储满 | 修改实例增加存储；检查增长快的表和日志。 |
| 发生故障转移 | 查看 RDS 事件和通知；检查副本延迟与主库负载。 |
| 查询慢 | 用 Performance Insights 定位负载；优化查询、索引和参数组。 |
| 副本延迟增长 | 检查副本实例类、主库写入负载、长事务。 |
| 恢复到 magnetic 失败 | magnetic 已弃用；恢复到通用型或预置 IOPS SSD。 |

## 配额

每区域配额：数据库实例默认 40 个、存储、只读副本；存储上下限因引擎而异。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon RDS？- Amazon RDS 用户指南](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [AWS CLI：rds 命令](https://docs.aws.amazon.com/cli/latest/reference/rds/)
