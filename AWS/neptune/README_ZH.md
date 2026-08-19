# Amazon Neptune - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Neptune 是快速、可靠、完全托管的图数据库，用于高度关联的数据集。它支持属性图（Apache TinkerPop Gremlin 和 openCypher）与 RDF 图（SPARQL），常用于欺诈检测、推荐引擎、知识图谱、药物发现和网络安全。

## 核心概念

- **DB 集群**：一个主实例加最多 15 个只读副本，共享集群卷。
- **集群卷**：SSD 存储，跨三个可用区复制；持久、自愈、自动增长。
- **属性图 vs RDF**：属性图用 Gremlin/openCypher，RDF 数据用 SPARQL。
- **Neptune Analytics**：把大图数据（来自 Neptune 或数据湖）加载到内存做快速分析的分析引擎。
- **备份**：持续备份到 S3，支持时间点恢复（PITR）。
- **安全**：VPC 隔离、IAM、静态和传输加密。
- **图笔记本**：Neptune Workbench/Jupyter 笔记本用于开发和可视化。

## 常用操作（AWS CLI）

```bash
# 创建集群和实例
aws neptune create-db-cluster --db-cluster-identifier graph-prod \
  --engine neptune \
  --db-cluster-instance-class db.r6g.large \
  --master-username adminuser --master-user-password <password> \
  --backup-retention-period 7

aws neptune create-db-instance --db-instance-identifier graph-prod-1 \
  --db-cluster-identifier graph-prod --db-instance-class db.r6g.large --engine neptune

# 添加只读副本
aws neptune create-db-instance --db-instance-identifier graph-prod-2 \
  --db-cluster-identifier graph-prod --db-instance-class db.r6g.large --engine neptune

# 查看
aws neptune describe-db-clusters
aws neptune describe-db-instances

# 备份和恢复
aws neptune create-db-cluster-snapshot --db-cluster-identifier graph-prod \
  --db-cluster-snapshot-identifier graph-prod-backup
aws neptune restore-db-cluster-from-snapshot \
  --db-cluster-identifier graph-restored --snapshot-identifier graph-prod-backup \
  --engine neptune
```

## 最佳实践

- 有意识地做图建模：高扇出节点和深度遍历才是图数据库相对关系库关联查询的优势场景。
- 用副本支撑读取和自动故障转移；写入走主实例。
- ID 和索引（Gremlin/SPARQL）匹配查询模式，避免全图扫描。
- PITR 保留期匹配 RPO；演练快照恢复。
- 集群放私有子网，用 IAM 数据库认证加 TLS。
- 用 CloudWatch（CPU、内存、副本延迟）和 Neptune 指标（查询数、Gremlin/SPARQL 请求延迟）监控。
- 大量图数据分析用 Neptune Analytics，而不是 OLTP 查询。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 遍历慢 | 检查查询计划、加索引、减少超级节点遍历。 |
| 写入吞吐低 | 扩大主实例规格；Neptune 读可扩展，写入走主实例。 |
| 故障转移异常 | 确认副本在不同可用区，检查副本延迟。 |
| PITR 不可用 | 确认已配置备份保留期（PITR 依赖自动备份）。 |
| 连接被拒 | 检查 Neptune 端口（8182）的安全组规则和 TLS 设置。 |

## 配额

每集群最多 15 个副本；实例规格、每账号集群数和存储增长受配额限制。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon Neptune？](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html)
- [Amazon Neptune 配额](https://docs.aws.amazon.com/neptune/latest/userguide/limits.html)
- [Amazon Neptune 定价](https://aws.amazon.com/neptune/pricing/)
- [AWS CLI：neptune 命令](https://docs.aws.amazon.com/cli/latest/reference/neptune/)
