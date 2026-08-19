# AWS CloudTrail - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS CloudTrail 记录用户、角色和 AWS 服务在账户中执行的操作（控制台、CLI、SDK 和 API），以事件形式保存。它支持运营与风险审计、治理和合规。CloudTrail 提供 Event history、Trail 和 CloudTrail Lake。

## 核心概念

- **Event history**：每个区域最近 90 天管理事件的可查看、可搜索、不可变记录；默认免费提供。
- **Trail**：将管理事件（可选数据事件/Insights 事件）投递到 S3 存储桶，并可选择投递到 CloudWatch Logs 和 EventBridge。
- **管理事件**：控制平面操作（谁、何时、从哪里做了什么）。
- **数据事件**：资源操作（S3 对象级活动、Lambda 调用、DynamoDB 操作）。
- **Insights 事件**：检测管理事件中的异常 API 活动（速率和错误异常）。
- **CloudTrail Lake**：托管审计数据湖，使用事件数据存储；按所选定价选项可保留事件约 7-10 年；支持 SQL 查询和仪表盘可视化，并可联合查询 Athena。
- **组织 Trail**：为 AWS Organizations 中所有账户创建的单个 Trail；成员账户不能禁用或修改它。

## 常用操作（AWS CLI）

```bash
# 创建多区域 Trail
aws cloudtrail create-trail --name default --s3-bucket-name trail-bucket \
  --is-multi-region-trail --include-global-service-events

# 启用日志并检查状态
aws cloudtrail start-logging --name default
aws cloudtrail get-trail-status --name default

# 事件选择器（管理事件 + S3 数据事件）
aws cloudtrail put-event-selectors --trail-name default \
  --event-selectors file://event-selectors.json

# 搜索近期管理事件
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventSource,AttributeValue=ec2.amazonaws.com

# CloudTrail Lake：创建事件数据存储
aws cloudtrail create-event-data-store --name audit-store \
  --retention-period 2557 \
  --advanced-event-selectors file://advanced-selectors.json

# 列出 Trail
aws cloudtrail list-trails
```

## 最佳实践

- 在管理账户创建组织 Trail，并投递到专用、加密、私有的 S3 存储桶。
- 启用 CloudTrail Insights 检测管理事件的异常行为。
- 有选择地记录数据事件（高价值存储桶、Lambda）以控制成本。
- 用存储桶策略保护 Trail 存储桶（拒绝公开访问），启用 S3 版本控制并使用 KMS 加密。
- 投递到 CloudWatch Logs 实现实时告警，用 CloudTrail Lake 做长期查询/审计。
- 用 CloudWatch 告警监控 Trail 状态，避免日志静默停止。
- 用 IAM 和 SCP 限制 `cloudtrail:StopLogging` 和 `DeleteTrail`。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 没有事件投递 | 确认 Trail 正在记录、S3 存储桶策略允许 CloudTrail 写入、KMS 密钥权限正确。 |
| 缺少数据事件 | 检查 Trail 的事件选择器和高级事件选择器。 |
| Event history 只有 90 天 | Event history 固定为 90 天；创建 Trail 或 Lake 事件数据存储以延长保留。 |
| 组织成员看不到事件 | 确认组织 Trail 已启用，且成员账户权限允许 `cloudtrail:GetTrail`。 |
| Lake 查询无结果 | 检查事件数据存储选择器、保留期和摄取状态。 |

## 配额

Event history 保留 90 天；Lake 事件数据存储按定价选项支持最多约 7 年（2,557 天）或 10 年（3,653 天）。Trail、事件数据存储和投递速率有配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS CloudTrail？- CloudTrail 用户指南](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
- [AWS CloudTrail 配额](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html)
- [AWS CloudTrail 定价](https://aws.amazon.com/cloudtrail/pricing/)
- [AWS CLI：cloudtrail 命令](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/)
