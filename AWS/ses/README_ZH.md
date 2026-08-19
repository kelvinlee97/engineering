# Amazon SES - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Simple Email Service（Amazon SES）是可扩展的电子邮件平台，用于发送事务性邮件（订单确认、密码重置）、营销邮件（优惠、新闻简报），也支持接收邮件。你可以通过 SES API、SMTP 接口或 AWS SDK 发送邮件，将收到的邮件路由到 S3、SNS 或 Lambda。按发送和接收的邮件量付费。

## 核心概念

- **邮件身份（Email identity）**：你获授权用来发信的已验证域名或邮箱地址；域名需要配置 DKIM 和 SPF/DMARC。
- **Easy DKIM**：SES 为你的域名管理 DKIM 签名（DNS 在 Route 53 时尤其简单）；生产发送必需。
- **Configuration set**：分组发送设置和事件目标（CloudWatch、Amazon Data Firehose、SNS、EventBridge、Pinpoint），用于跟踪退信、投诉、投递以及打开/点击。
- **抑制与声誉**：SES 跟踪退信和投诉率、应用发送限制，并允许你管理抑制列表。
- **接收邮件**：通过接收规则（receipt rules）将入站邮件路由到 S3（可选 KMS 加密）、SNS 或 Lambda。
- **SMTP 接口**：通过 SES SMTP 凭证（与 IAM 分开）支持使用 SMTP 的应用/工具发送。
- **发送限制**：每日邮件配额和每秒最大发送速率，可根据声誉在 SES 控制台/API 申请调整。

## 常用操作（AWS CLI）

```bash
# 验证身份（域名）
aws sesv2 create-email-identity --identity-name example.com
aws sesv2 get-email-identity --email-identity-name example.com

# 发送邮件
aws sesv2 send-email \
  --from-email-address no-reply@example.com \
  --destination '{"ToAddresses":["user@example.com"]}' \
  --content '{"Simple":{"Subject":{"Data":"Hello"},"Body":{"Text":{"Data":"Test from SES"}}}}'

# Configuration set 和事件目标
aws sesv2 create-configuration-set --configuration-set-name prod
aws sesv2 create-configuration-set-event-destination \
  --configuration-set-name prod --event-destination-name cloudwatch \
  --event-destination '{"Enabled":true,"MatchingEventTypes":["BOUNCE","COMPLAINT"],"CloudWatchDestination":{"DimensionConfigurations":[]}}'

# 发送统计和配额
aws sesv2 get-account
aws sesv2 get-send-quota

# 接收邮件（带 S3 动作的规则集）
aws sesv2 create-receipt-rule-set --rule-set-name default
aws sesv2 create-receipt-rule --rule-set-name default \
  --rule file://rule.json
```

## 最佳实践

- 所有发送域名验证并配置 Easy DKIM（以及 SPF/DMARC）；绝不用未验证身份发信。
- 新身份逐步预热，保持退信/投诉率低；及时处理反馈通知。
- 每个工作负载使用独立 configuration set，并对退信/投诉激增设置告警。
- 维护抑制列表并尊重退订请求，保护声誉并符合邮件法规。
- 事务性与营销邮件用独立身份/configuration set 分离。
- 用 IAM 最小权限保护 SES 凭证（SMTP 或 API），并用 CloudTrail 监控 API 调用。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 使用未验证身份发送 | 验证域名/邮箱身份并完成 DKIM 配置，等待传播。 |
| 超出每日配额 | 查看 `get-send-quota`；在退信/投诉率低时申请提高限额。 |
| 邮件进入垃圾箱 | 核对 DKIM/SPF/DMARC、预热身份，并审查内容和发送模式。 |
| 缺少退信/投诉事件 | 确认 configuration set 已附加，事件目标配置正确。 |
| 入站邮件未投递 | 检查接收规则集顺序、S3/SNS/Lambda 动作权限和垃圾过滤行为。 |

## 配额

每日发送配额、最大发送速率、消息大小和每账户身份数有限制；SES 会根据声誉调整配额。以 SES 服务配额页面和 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon SES？- 开发者指南](https://docs.aws.amazon.com/ses/latest/dg/Welcome.html)
- [Amazon SES 服务配额](https://docs.aws.amazon.com/ses/latest/dg/quotas.html)
- [Amazon SES 定价](https://aws.amazon.com/ses/pricing/)
- [AWS CLI：sesv2 命令](https://docs.aws.amazon.com/cli/latest/reference/sesv2/)
