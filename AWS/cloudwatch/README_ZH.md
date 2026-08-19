# Amazon CloudWatch - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon CloudWatch 是 AWS 的监控与可观测性服务。它收集并跟踪 AWS 资源和应用程序的指标、日志与追踪数据，并提供告警、仪表盘和自动操作。它还提供应用性能监控（Application Signals）、日志分析（Logs Insights）、合成监控和跨账户可观测性。

## 核心概念

- **指标（Metrics）**：时间序列数据点；AWS 服务自动发布指标，你也可以从应用程序发布自定义指标。
- **告警（Alarms）**：根据阈值监控指标并触发操作（SNS、EC2 Auto Scaling、Systems Manager）。
- **仪表盘（Dashboards）**：统一、可定制的指标与日志视图，可在账户和区域间共享。
- **日志（Logs）**：来自 AWS 服务和应用程序的日志组与日志流；使用 Logs Insights（SQL/PPL）查询，可创建指标过滤器和订阅过滤器。
- **CloudWatch 代理**：从 EC2 和本地服务器收集系统级指标（CPU、内存、磁盘、网络）、日志和追踪数据。
- **Application Signals / SLO**：无需修改代码即可监控延迟、错误率和请求速率；可定义带有错误预算的服务水平目标。
- **Synthetics 与 RUM**：canary 模拟用户流程；RUM 收集真实用户性能数据。
- **Container Insights / Lambda Insights / Database Insights**：针对特定服务的监控视图。
- **OpenTelemetry**：原生 OTLP 摄取指标、日志和追踪数据。

## 常用操作（AWS CLI）

```bash
# 发布自定义指标
aws cloudwatch put-metric-data --namespace App --metric-name Latency \
  --value 120 --unit Milliseconds --dimensions Service=checkout

# 获取统计信息
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
  --start-time 2026-08-18T00:00:00Z --end-time 2026-08-19T00:00:00Z \
  --period 300 --statistics Average

# 告警
aws cloudwatch put-metric-alarm --alarm-name high-cpu --alarm-description "CPU > 80%" \
  --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average \
  --period 300 --threshold 80 --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts

# 日志
aws logs create-log-group --log-group-name /app/prod
aws logs filter-log-events --log-group-name /app/prod --filter-pattern "ERROR"
aws logs start-query --log-group-name /app/prod \
  --start-time 1784332800 --end-time 1784419200 \
  --query-string "fields @timestamp, @message | stats count(*) by bin(5m)"
aws logs get-query-results --query-id <query-id>

# 仪表盘
aws cloudwatch put-dashboard --dashboard-name ops --dashboard-body file://dashboard.json
```

## 最佳实践

- 使用标准（免费）指标做广泛覆盖，只在需要处启用详细监控以控制成本。
- 使用一致的命名空间/维度发布自定义指标，并用于应用级告警。
- 将日志集中到日志组，用 Logs Insights 查询排查问题；将关键日志流式传输到 S3 保留。
- 在 EC2/本地服务器上使用 CloudWatch 代理（或 OpenTelemetry）采集操作系统级指标。
- 为运维信号（CPU、内存、错误率、队列深度）设置告警并定期审查。
- 在多账户环境中从中央监控账户使用跨账户可观测性。
- 组合指标、日志和追踪（X-Ray/OTLP）做端到端根因分析。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 实例没有指标 | 确认 CloudWatch 代理已安装/运行，且 IAM 角色允许 `cloudwatch:PutMetricData`。 |
| 告警不触发 | 检查指标名称/命名空间、周期、阈值，以及告警状态是否处于 INSUFFICIENT_DATA。 |
| 日志缺失 | 核对日志组/日志流名称、代理配置和权限。 |
| CloudWatch 成本高 | 减少自定义指标量、日志摄取量或详细监控；高效使用指标过滤器。 |
| Logs Insights 查询报错 | 校验查询语言（SQL/PPL）和时间范围。 |

## 配额

指标分辨率、保留期（标准指标 15 个月）、每账户告警数和日志摄取速率都有配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon CloudWatch？- CloudWatch 用户指南](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [Amazon CloudWatch 服务配额](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_limits.html)
- [Amazon CloudWatch 定价](https://aws.amazon.com/cloudwatch/pricing/)
