# Amazon CodeGuru - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon CodeGuru 是机器学习服务，包含两个能力：CodeGuru Reviewer 分析代码中的缺陷和安全问题，CodeGuru Profiler 在运行时定位最昂贵的代码行。注意：自 2025 年 11 月 7 日起，无法再在 CodeGuru Reviewer 中创建新的仓库关联；现有功能和类似能力的替代服务见 AWS 公告。

## 核心概念

- **CodeGuru Reviewer**：使用程序分析和机器学习检测 Java 和 Python 代码中的复杂缺陷并提出改进建议（资源泄漏、安全问题、最佳实践）；集成 GitHub、Bitbucket 和 S3（通过 GitHub Actions）。
- **密钥检测**：Reviewer 可发现代码中未受保护的密钥，并与 AWS Secrets Manager 集成。
- **CodeGuru Profiler**：在生产环境对应用进行性能剖析，可视化性能，定位最昂贵的代码行和低效路径；有助于降低成本与延迟。
- **可用性变化**：Reviewer 不再支持新的仓库关联（2025 年 11 月 7 日起）；类似能力的替代服务见 AWS 公告。

## 常用操作（AWS CLI）

```bash
# CodeGuru Profiler：创建剖析组并查看结果
aws codeguruprofiler create-profiling-group --profiling-group-name prod-app
aws codeguruprofiler list-profile-times --profiling-group-name prod-app \
  --start-time 2026-08-18T00:00:00Z --end-time 2026-08-19T00:00:00Z
aws codeguruprofiler get-policy --profiling-group-name prod-app

# Reviewer（现有关联）：列出代码评审
aws codeguru-reviewer list-code-reviews --type RepositoryAnalysis
aws codeguru-reviewer describe-code-review --code-review-arn <review-arn>
```

## 最佳实践

- 在仍可用处让 Reviewer 在 pull request 上运行，使建议进入评审流程。
- 合并前修复高置信度建议（安全、资源泄漏）；跟踪建议积压。
- 生产环境持续运行 Profiler，捕获回归和昂贵代码路径；剖析有代表性的流量。
- IAM 最小权限：剖析代理与控制台访问使用独立角色。
- 监控 profiler 结果，为性能回归设置告警。
- 需要超出现有 Reviewer 关联的仓库分析时，遵循 AWS 的替代服务指引。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 没有建议 | 检查仓库关联状态、受支持语言（Java/Python）和评审范围。 |
| 无法创建仓库关联 | 新关联自 2025 年 11 月 7 日起不再支持；使用文档化的替代方案。 |
| Profiler 无数据 | 核对代理已安装/运行，IAM 允许 `codeguruprofiler:PostAgentProfile`。 |
| profile 时间为空 | 确认剖析组名称和时间范围。 |
| 建议噪声大 | 聚焦高置信度/安全检测器，建立带负责人的积压清单。 |

## 配额

每账户剖析组数、profile 保留期和 API 请求速率有限制；Reviewer 可用性受已公布的服务变更影响。以 Amazon CodeGuru 端点和配额页面为准。

## 官方参考

- [什么是 Amazon CodeGuru Reviewer？- 用户指南](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html)
- [Amazon CodeGuru Profiler 用户指南](https://docs.aws.amazon.com/codeguru/latest/profiler-ug/what-is-codeguru-profiler.html)
- [Amazon CodeGuru 端点和配额](https://docs.aws.amazon.com/general/latest/gr/codeguru.html)
- [Amazon CodeGuru 定价](https://aws.amazon.com/codeguru/pricing/)
- [AWS CLI：codeguru-reviewer 和 codeguruprofiler 命令](https://docs.aws.amazon.com/cli/latest/reference/codeguru-reviewer/)
