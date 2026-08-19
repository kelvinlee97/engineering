# AWS Config - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Config 记录账号和区域内受支持 AWS 资源的配置，跟踪配置及关系随时间的变化，并按规则评估合规性。它把配置历史和快照投递到 S3，通过 SNS 发送变更通知，还支持合规包（conformance pack）、聚合器和高级查询。

## 核心概念

- **配置项（Configuration item, CI）**：某个时间点资源状态的记录，含资源关系。
- **配置记录器（Configuration recorder）**：捕获变更；每账号每区域一个客户托管记录器（服务关联记录器由集成服务如 Security Hub CSPM 创建）。
- **配置历史与快照**：按计划或按需投递到 S3 桶。
- **配置流（Configuration stream）**：记录到资源变更时通过 SNS 发送通知。
- **规则（Rules）**：托管或自定义（Lambda）评估，报告合规/不合规。
- **合规包（Conformance packs）**：以 YAML 打包的规则和修复操作，作为一个整体部署。
- **聚合器（Aggregators）**：集中多个账号和区域的配置与合规数据。
- **高级查询**：对已记录的资源配置执行类 SQL 查询（`SELECT`）。

## 常用操作（AWS CLI）

```bash
# 配置记录器（使用 AWS Config 服务关联角色）
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig

# 设置投递通道（S3 + SNS）
aws configservice put-delivery-channel \
  --delivery-channel s3BucketName=config-bucket,snsTopicARN=arn:aws:sns:us-east-1:123456789012:config-topic

# 开始记录
aws configservice start-configuration-recorder --configuration-recorder-name default

# 规则
aws configservice put-config-rule --config-rule file://rule.json
aws configservice describe-config-rules
aws configservice describe-compliance-by-config-rule --config-rule-names s3-bucket-ssl-requests-only
aws configservice get-compliance-details-by-config-rule --config-rule-name <rule-name>

# 高级查询
aws configservice select-resource-config \
  --expression "SELECT resourceId, resourceType WHERE resourceType = 'AWS::EC2::Instance'"

# 聚合器（多账号 / 多区域视图）
aws configservice put-configuration-aggregator --configuration-aggregator-name org-aggregator \
  --organization-aggregation-source AllRegions=true
```

## 最佳实践

- 记录所有受支持的资源类型（或至少是合规范围需要的）；实时监控用连续记录。
- 用托管规则和合规包在多个账号间统一合规检查。
- 投递用的 S3 桶保持私有并加密；只给 AWS Config 必要权限。
- 用聚合器构建多账号、多区域合规仪表盘。
- 支持时使用组织级规则和合规包做集中治理。
- 用高级查询做资源清点和漂移检查；保存可复用查询。
- 修复操作（SSM Automation 文档）先在测试环境验证，再自动执行。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 资源未记录 | 确认记录器已启动、IAM 角色有权限、资源类型在该区域受支持。 |
| 没有合规结果 | 确认规则已部署、被评估的资源类型已记录、评估已完成。 |
| 投递到 S3/SNS 失败 | 检查桶策略、主题权限和投递通道配置。 |
| 聚合器无数据 | 确认源账号已授权聚合，且选择了所需区域。 |
| 高级查询无结果 | 检查资源类型是否已记录、属性名是否符合配置 schema。 |
| 删除后仍有旧结果 | 记录器必须运行才能捕获删除事件；重新启动记录器。 |

## 配额

每区域每账号最多 1,000 条规则；50 个合规包；每个合规包最多 130 条规则；50 个聚合器（可调整）；每个聚合器最多 10,000 个账号；300 个保存的查询；每个资源最多 50 个标签；每账号每区域一个客户托管配置记录器。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Config？- AWS Config 开发者指南](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [AWS Config 服务限制](https://docs.aws.amazon.com/config/latest/developerguide/configlimits.html)
- [AWS Config 定价](https://aws.amazon.com/config/pricing/)
- [AWS CLI：configservice 命令](https://docs.aws.amazon.com/cli/latest/reference/configservice/)
