# AWS X-Ray - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS X-Ray 收集应用程序所处理请求的数据，并提供查看、过滤和分析这些数据的工具。它展示请求经过前端、微服务、数据库和下游 AWS API 的完整路径，帮助你定位瓶颈、延迟尖峰和错误。

## 核心概念

- **Segment 与 Subsegment**：描述服务（或服务内一次调用）所做工作的追踪数据单元。
- **Trace**：由跨服务的 segment/subsegment 组成的完整请求路径。
- **Service map**：以可视化图形展示服务及调用关系，并带有延迟和错误数据。
- **采样（Sampling）**：控制记录多少请求以管理成本；包括默认规则和自定义规则。
- **埋点（Instrumentation）**：X-Ray SDK（Java、Python、Node.js、Go、.NET、Ruby）将 segment 文档发送给 X-Ray 守护进程，守护进程通过 UDP 批量上传。
- **集成服务**：Lambda、API Gateway、ECS/EKS、EC2、Elastic Beanstalk 等可最小化配置自动发送追踪数据。
- **Trace header**：`X-Amzn-Trace-Id` 在服务间传播追踪上下文。

## 常用操作（AWS CLI）

```bash
# 获取服务图（近期追踪数据）
aws xray get-service-graph --start-time 1784332800 --end-time 1784419200

# 汇总与追踪详情
aws xray get-trace-summaries --start-time 1784332800 --end-time 1784419200 \
  --filter-expression 'service("checkout") { fault = true }'
aws xray batch-get-traces --trace-ids <trace-id>

# 分组
aws xray create-group --group-name errors --filter-expression 'fault = true'
aws xray get-groups
```

## 最佳实践

- 在服务边界埋点：使用 SDK 时，HTTP 客户端、AWS SDK 调用和数据库查询会自动生成 subsegment。
- 在 EC2/本地环境运行 X-Ray 守护进程（Lambda 和 Elastic Beanstalk 平台已内置）。
- 设置采样规则，让高流量服务记录有代表性的样本而不超预算。
- 使用 trace header 跨服务传播上下文；将 ID 写入应用程序日志以便关联。
- 需要长期保留的追踪数据导出到 S3；追踪数据默认保留 30 天。
- 定期查看 service map，关注延迟和错误热点。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 看不到追踪 | 检查 SDK 埋点、守护进程状态以及 X-Ray 服务的 IAM 权限。 |
| 缺少下游调用 | 核对 SDK 版本，确认 HTTP/AWS SDK 客户端已埋点。 |
| 成本过高 | 降低采样率，或为低价值端点添加采样规则。 |
| 追踪上下文丢失 | 确认 trace header 已在服务间（代理/Lambda）正确传播。 |
| Service map 有缺口 | 检查哪些服务已埋点及其所在区域。 |

## 配额

追踪保留期（30 天）、每个 trace 的 segment 数以及 API 请求速率都有配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS X-Ray？- X-Ray 开发者指南](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
- [AWS X-Ray 配额](https://docs.aws.amazon.com/general/latest/gr/xray.html)
- [AWS X-Ray 定价](https://aws.amazon.com/xray/pricing/)
- [AWS CLI：xray 命令](https://docs.aws.amazon.com/cli/latest/reference/xray/)
