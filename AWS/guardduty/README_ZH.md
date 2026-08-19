# Amazon GuardDuty - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon GuardDuty 是威胁检测服务，持续监控和分析 AWS 数据源，包括 CloudTrail 管理事件、VPC Flow Logs 和 DNS 日志；还提供可选的保护计划，覆盖 EKS 审计日志、RDS 登录活动、S3 数据事件、EBS 恶意软件扫描、EC2/EKS/ECS 运行时监控、Lambda 网络活动和 AI 工作负载。GuardDuty 使用威胁情报（恶意 IP、域名和文件哈希）和机器学习生成安全发现（finding）。

## 核心概念

- **Detector**：GuardDuty 的配置对象；每个账号每个区域一个。
- **Finding（安全发现）**：检测到威胁的结构化记录，含严重级别（低/中/高）和资源详情。
- **基础数据源**：CloudTrail 管理事件、VPC Flow Logs（来自 EC2）和 DNS 日志；启用 GuardDuty 后自动开始摄取。
- **保护计划**：可选功能组，如 S3 Protection、EKS Audit Log Monitoring、Malware Protection（EBS/S3/备份）、RDS Protection、Runtime Monitoring、Lambda Protection 和 AI Protection。
- **管理员与成员账号**：通过 AWS Organizations（推荐）或邀请方式做多账号管理。
- **过滤器和抑制规则**：减少已知无害活动的噪音。
- **威胁情报集与可信 IP 列表**：自定义检测上下文。

## 常用操作（AWS CLI）

```bash
# 启用 GuardDuty（创建 detector）
aws guardduty create-detector --enable

# 获取 detector ID
aws guardduty list-detectors

# 列出并查看 finding
aws guardduty list-findings --detector-id <detector-id>
aws guardduty get-findings --detector-id <detector-id> --finding-ids <finding-id>

# 暂停（保留数据）或删除（删除 finding 和配置）
aws guardduty update-detector --detector-id <detector-id> --no-enable
aws guardduty delete-detector --detector-id <detector-id>

# 归档或取消归档 finding
aws guardduty archive-findings --detector-id <detector-id> --finding-ids <finding-id>
aws guardduty unarchive-findings --detector-id <detector-id> --finding-ids <finding-id>

# 添加威胁情报集
aws guardduty create-threat-intel-set --detector-id <detector-id> --name my-intel \
  --format TXT --location s3://bucket/threat-intel.txt --activate
```

## 最佳实践

- 在所有区域和账号启用 GuardDuty；通过 AWS Organizations 委派管理员做多账号管理。
- 按工作负载启用对应保护计划（S3、EKS 审计、运行时监控、恶意软件防护）。
- 将 finding 接入 EventBridge 和 AWS Security Hub CSPM，并用 Lambda/SNS 自动化响应。
- 用示例 finding 和 GuardDuty 测试脚本验证检测与响应链路。
- 将 finding 导出到 S3，保留超过 90 天并便于分析。
- 谨慎使用过滤器和抑制规则：它们只是隐藏 finding，不会修复根因。
- IAM 最小权限；为检测自动化使用专用角色。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 没有 finding | 确认 detector 已启用且基础数据源在摄取；用示例 finding 测试。 |
| 缺少 S3/EKS/RDS 检测 | 在同一区域启用对应保护计划。 |
| Security Hub CSPM 中没有 finding | 在同一区域启用 Security Hub CSPM 及其 GuardDuty 集成。 |
| EventBridge 规则不触发 | 核对事件模式 source（`aws.guardduty`）以及是否有新 finding。 |
| 恶意软件扫描不运行 | 检查 Malware Protection 计划、快照权限和扫描配额。 |
| 误删除 | `delete-detector` 会删除 finding 和配置；需要保留数据请用暂停（`update-detector --no-enable`）。 |

## 配额

每账号每区域 1 个 detector；finding 保留 90 天（固定）；最多 6 个威胁情报集、1 个可信 IP 列表、100 个过滤器；每区域通过邀请最多 5,000 个成员账号，通过 Organizations 最多 50,000 个。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon GuardDuty？- GuardDuty 用户指南](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Amazon GuardDuty 端点和配额](https://docs.aws.amazon.com/general/latest/gr/guardduty.html)
- [Amazon GuardDuty 定价](https://aws.amazon.com/guardduty/pricing/)
- [AWS CLI：guardduty 命令](https://docs.aws.amazon.com/cli/latest/reference/guardduty/)
