# Amazon QuickSight - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon QuickSight 是 Amazon Quick（由 QuickSight 演进而来的 AI 驱动服务）中的商业智能与数据可视化能力。它连接数据源、构建交互式仪表盘和分析，并支持在应用中嵌入分析。所有现有 QuickSight API、SDK 和集成继续可用。

## 核心概念

- **数据源**：连接 AWS 服务（Athena、Redshift、RDS、S3）、SaaS 应用和数据库；数据可导入 SPICE（内存引擎）或实时查询。
- **SPICE**：Super-fast, Parallel, In-memory Calculation Engine，缓存导入数据以获得快速交互分析。
- **分析（Analyses）与仪表盘（Dashboards）**：分析是工作文档；仪表盘是发布给用户的只读视图。
- **数据集与字段**：数据集定义数据及其转换（计算字段、连接、过滤器），供分析使用。
- **身份与访问**：用户通过 IAM Identity Center、IAM 联邦或 QuickSight 托管用户管理；按用户分配 reader/author/admin 角色。
- **嵌入**：在应用中嵌入仪表盘和分析；支持基于 API 的访问。
- **Amazon Quick 演进**：Quick 新增 AI 智能体、flows、automations、research 和应用构建；QuickSight 仍是分析功能，根据计划可带或不带 AWS 账户登录。

## 常用操作（AWS CLI）

```bash
# 数据源、数据集和分析
aws quicksight create-data-source --aws-account-id 123456789012 \
  --data-source-id athena-prod --name athena-prod \
  --type ATHENA --parameters file://params.json
aws quicksight create-data-set --aws-account-id 123456789012 \
  --data-set-id orders --name orders --physical-table-map file://tables.json
aws quicksight create-analysis --aws-account-id 123456789012 \
  --analysis-id orders-analysis --name orders-analysis \
  --source-entity file://source.json

# 发布仪表盘并列出资源
aws quicksight create-dashboard --aws-account-id 123456789012 \
  --dashboard-id orders-dashboard --name orders-dashboard \
  --source-entity file://source.json
aws quicksight list-dashboards --aws-account-id 123456789012
aws quicksight list-data-sources --aws-account-id 123456789012
```

## 最佳实践

- 大型、读密集型数据集使用 SPICE，需要新鲜度的场景用实时查询；监控 SPICE 容量。
- 在数据集中建模（连接、计算字段），而不是在每个分析中重复转换。
- 发布精选仪表盘，按用户/组限制访问；多租户数据使用行级安全。
- 配置 IAM Identity Center 或联邦，集中管理身份和生命周期。
- 监控每用户用量和成本；按需启用容量和 API 控制。
- 嵌入场景沿用控制台的治理与刷新计划。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 数据源连接失败 | 核对网络访问（VPC/安全组）、凭证以及数据源类型/区域。 |
| SPICE 刷新失败 | 检查数据集刷新计划、源权限和 SPICE 容量。 |
| 用户看不到仪表盘 | 确认用户/组有访问权限，且仪表盘已发布（而不只是分析）。 |
| 嵌入空白 | 核对嵌入 URL/域名白名单和 IAM/QuickSight 会话权限。 |
| 查询慢 | 导入数据用 SPICE，或优化底层查询（Athena/Redshift）。 |

## 配额

SPICE 容量、用户数、数据集、仪表盘和 API 请求速率有限制。以 Amazon QuickSight 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon QuickSight？- 用户指南](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)
- [Amazon QuickSight 端点和配额](https://docs.aws.amazon.com/general/latest/gr/quicksight.html)
- [Amazon QuickSight 定价](https://aws.amazon.com/quicksight/pricing/)
- [AWS CLI：quicksight 命令](https://docs.aws.amazon.com/cli/latest/reference/quicksight/)
