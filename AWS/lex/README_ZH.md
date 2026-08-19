# Amazon Lex - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Lex V2 是使用语音和文本构建对话界面（聊天机器人）的服务。它提供自然语言理解（NLU）和自动语音识别（ASR），开发者无需深度学习专业知识即可构建、测试和发布理解用户意图并完成任务的中。你只为发起的文本或语音请求付费。

## 核心概念

- **Bot**：对话应用；在控制台或通过 API 定义对话流程。
- **Intent（意图）**：用户想做的事（例如 BookAppointment）；意图包含示例语句（utterances）和槽位。
- **Slot 与 slot type**：机器人收集的变量（例如日期、城市）；槽位类型可内置或自定义。
- **Fulfillment（履行）**：用 Lambda 函数（或条件分支）完成用户请求。
- **条件分支（Conditional branching）**：无需编写 Lambda 代码即可控制对话流程（2022 年 8 月 17 日后创建的 bot）。
- **Assisted NLU**：由 LLM 驱动的意图分类和槽位解析，保持在 bot 配置的意图/槽位范围内。
- **多区域复制（MRR）**：跨区域部署 bot，提高可用性和容灾。
- **渠道（Channels）**：发布到 Web 应用、移动端、Facebook Messenger、Slack、Teams、WhatsApp 等。
- **集成**：与 Lambda、CloudWatch 以及 Connect Customer、Comprehend、Kendra 等 AWS 服务集成。

## 常用操作（AWS CLI）

```bash
# 创建 bot、意图和槽位类型
aws lexv2-models create-bot --bot-name support-bot \
  --role-arn arn:aws:iam::123456789012:role/lex-role --data-privacy '{"childDirected":false}' \
  --idle-session-ttl-in-seconds 300 --bot-locale-settings '{}'
aws lexv2-models create-intent --bot-id <bot-id> --bot-version DRAFT \
  --locale-id en_US --intent-name BookAppointment \
  --sample-utterances file://utterances.json
aws lexv2-models create-slot-type --bot-id <bot-id> --bot-version DRAFT \
  --locale-id en_US --slot-type-name City --value-selection-setting file://slots.json

# 构建并测试
aws lexv2-models build-bot-locale --bot-id <bot-id> --bot-version DRAFT --locale-id en_US
aws lexv2-runtime recognize-text --bot-id <bot-id> --bot-alias-id <alias-id> \
  --locale-id en_US --text "Book an appointment"
```

## 最佳实践

- 从少数高价值意图和示例语句开始，根据对话日志迭代。
- 业务逻辑用带校验的槽位和 Lambda 履行；简单流程用条件分支。
- 监控 bot 分析和 CloudWatch 日志中的 fallback/混淆；改进语句并补充边界情况。
- 发布 bot 版本和别名；多区域部署用 MRR。
- 履行用最小权限 Lambda 角色；对用户输入做清洗。
- 与 Connect Customer 集成做人工升级，用 Comprehend 做情感分析。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 意图未识别 | 增加示例语句并检查 locale；查看对话日志。 |
| 槽位未收集 | 校验槽位提示/消息配置和槽位类型。 |
| 履行失败 | 检查 Lambda 函数、IAM 权限和超时设置。 |
| 渠道中 bot 无响应 | 核对部署到渠道的别名/版本和渠道凭证。 |
| fallback 率高 | 查看分析数据、改进语句，并使用 assisted NLU 功能。 |

## 配额

每账户 bot、意图、槽位、版本和 API 请求速率有限制。以 Amazon Lex 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Lex V2？- 开发者指南](https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html)
- [Amazon Lex 端点和配额](https://docs.aws.amazon.com/general/latest/gr/lex.html)
- [Amazon Lex 定价](https://aws.amazon.com/lex/pricing/)
- [AWS CLI：lexv2-models 和 lexv2-runtime 命令](https://docs.aws.amazon.com/cli/latest/reference/lexv2-models/)
