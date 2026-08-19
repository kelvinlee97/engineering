# AWS Well-Architected Framework - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Well-Architected Framework 是用于在云中设计和运营可靠、安全、高效且经济的工作负载的 Best Practice 集合。AWS Well-Architected Tool（AWS WA Tool）提供一致流程，记录决策、回答评审问题，并围绕六大支柱给出改进建议。

## 核心概念

- **六大支柱**：
  1. **卓越运营（Operational excellence）**：运行和监控系统，持续改进流程。
  2. **安全（Security）**：保护数据、系统和资产；应用身份、检测和基础设施保护。
  3. **可靠性（Reliability）**：从故障恢复、扩展并满足需求；为可用性和持久性设计。
  4. **性能效率（Performance efficiency）**：高效使用计算资源满足需求。
  5. **成本优化（Cost optimization）**：避免不必要成本，最大化价值。
  6. **可持续性（Sustainability）**：最小化云工作负载的环境影响。
- **AWS WA Tool**：记录工作负载，带证据回答支柱问题，并获得高/中风险改进计划。
- **Lenses**：AWS 提供的 lens（例如 serverless、SaaS、HPC）以及你自定义的 lens。
- **评审流程**：在生命周期中定期做工作负载评审，并在工具中跟踪改进。
- **集成**：Trusted Advisor 和 Service Catalog AppRegistry 帮助收集回答评审问题所需的信息。

## 常用操作（AWS CLI）

```bash
# 创建工作负载并运行评审
aws wellarchitected create-workload --client-request-token demo \
  --workload-name prod-workload --environment PRODUCTION \
  --review-owner owner@example.com --lenses "arn:aws:wellarchitected::aws:lens/wellarchitected"
aws wellarchitected list-workloads
aws wellarchitected get-workload --workload-id <workload-id>

# 添加答案并获取改进计划
aws wellarchitected update-answer --workload-id <workload-id> \
  --lens-alias wellarchitected --question-id reliability \
  --selected-choices <choice-id>
aws wellarchitected get-lens-review --workload-id <workload-id> \
  --lens-alias wellarchitected
```

## 最佳实践

- 在设计阶段和重要里程碑（新大功能、扩展事件）运行 Well-Architected 评审。
- 为答案附上证据（架构图、仪表盘、runbook），让决策可追溯。
- 优先处理高风险项；将建议转化为带负责人的可跟踪改进任务。
- 结合支柱与 WA Tool 的改进计划，定期复查。
- 按工作负载类型使用合适 lens（serverless、SaaS 等），并用自定义 lens 支撑内部治理。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 看不到工作负载 | 确认账户/区域和 `wellarchitected:*` IAM 权限。 |
| 答案未保存 | 检查 workload/lens ID，以及选项是否对该问题有效。 |
| 没有改进计划 | 回答所有适用问题；计划由已答风险生成。 |
| 自定义 lens 缺失 | 发布/共享自定义 lens，并授予工作负载所有者访问权限。 |

## 配额

每账户工作负载和自定义 lens 数量有限制。以 AWS Well-Architected Tool 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Well-Architected Tool 用户指南](https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html)
- [AWS Well-Architected Tool 定价](https://aws.amazon.com/well-architected-tool/pricing/)
- [AWS CLI：wellarchitected 命令](https://docs.aws.amazon.com/cli/latest/reference/wellarchitected/)
