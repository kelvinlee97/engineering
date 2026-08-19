# AWS Step Functions - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Step Functions 是无服务器编排服务。你把工作流（状态机）定义为一串步骤，协调 Lambda 函数、AWS 服务和人工审批流程。支持可视化调试、重试、并行处理和长时间运行的工作流。

## 核心概念

- **状态机（工作流）**：用 Amazon States Language（JSON）定义的工作流。
- **状态（States）**：Task、Choice、Parallel、Map、Wait、Pass、Succeed、Fail。
- **执行（Executions）**：状态机的运行实例。
- **Standard 工作流**：精确一次执行，最长运行 1 年，每秒最多 2,000 次执行；适合长时间、可审计的流程。
- **Express 工作流**：至少一次执行，最长运行 5 分钟，每秒最多 100,000 次执行；适合高吞吐流式/摄取场景。
- **集成**：AWS SDK 集成可调用任意 AWS API；优化集成对特定服务增加模式。
- **集成模式**：Request Response、Run a Job（`.sync`）、Wait for Callback（`.waitForTaskToken`，人工审批）。
- **错误处理**：每个状态支持 `Retry` 和 `Catch`；Activity 让外部 worker 轮询任务。
- **Distributed Map**：并发运行子工作流处理大数据集。

## 常用操作（AWS CLI）

```bash
# 从定义文件创建状态机
aws stepfunctions create-state-machine --name order-flow \
  --definition file://state-machine.json \
  --role-arn arn:aws:iam::123456789012:role/stepfunctions-role \
  --type STANDARD

# 启动和监控执行
aws stepfunctions start-execution --state-machine-arn <state-machine-arn> \
  --input '{"orderId":"123"}'
aws stepfunctions describe-execution --execution-arn <execution-arn>
aws stepfunctions list-executions --state-machine-arn <state-machine-arn>

# 查看历史与更新
aws stepfunctions get-execution-history --execution-arn <execution-arn>
aws stepfunctions update-state-machine --state-machine-arn <state-machine-arn> \
  --definition file://state-machine-v2.json
```

```json
{
  "StartAt": "Validate",
  "States": {
    "Validate": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:us-east-1:123456789012:function:validate",
        "Payload.$": "$"
      },
      "Retry": [{"ErrorEquals": ["Lambda.ServiceException"], "MaxAttempts": 3}],
      "Next": "Approve"
    },
    "Approve": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:us-east-1:123456789012:function:approval",
        "Payload": {"taskToken.$": "$$.Task.Token"}
      },
      "Next": "Done"
    },
    "Done": {"Type": "Succeed"}
  }
}
```

## 最佳实践

- 可审计、长时间流程用 Standard；高吞吐、短流程用 Express。
- 优先 AWS SDK/优化集成，减少自定义 Lambda 胶水代码。
- 瞬时错误用带退避的 `Retry`，业务失败用 `Catch`。
- 人工审批用 `.waitForTaskToken` 回调建模。
- 控制执行输入/输出大小；大数据存 S3，传引用。
- 用 CloudWatch 指标和 X-Ray 追踪提升可见性；对 `ExecutionsFailed` 设置告警。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 执行失败 | 用 `get-execution-history` 查看失败状态和错误输出。 |
| Lambda 未调用 | 检查状态机 IAM 角色和 Lambda 权限。 |
| 回调不返回 | 确认 worker 把 task token 发回 Step Functions。 |
| 超时错误 | 调整状态超时/`heartbeatSeconds`。 |
| 成本高 | 检查状态转换次数；高吞吐用 Express 工作流。 |

## 配额

每秒执行数、状态转换、执行历史大小和载荷大小因 Standard/Express 而异。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Step Functions？](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon States Language 规范](https://states-language.net/spec.html)
- [AWS Step Functions 定价](https://aws.amazon.com/step-functions/pricing/)
- [AWS CLI：stepfunctions 命令](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/)
