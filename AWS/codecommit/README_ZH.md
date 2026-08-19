# AWS CodeCommit - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS CodeCommit 是托管版本控制服务，在云中托管私有 Git 仓库。它支持完整的 Git 工作流（clone、branch、commit、push、pull、pull request），通过 IAM 控制访问，静态和传输数据加密，并且可扩展到大型仓库，仓库大小和文件类型没有限制。

## 核心概念

- **仓库（Repository）**：由 AWS 托管的私有 Git 仓库；通过控制台或 CLI 创建，可用 HTTPS 或 SSH 克隆/推送（SSH 使用密钥，HTTPS 使用 Git 凭证）。
- **Git 操作**：CodeCommit 兼容 Git，现有 Git 工具和工作流无需改动即可使用。
- **Pull request**：合并前审查和评论代码变更；CodeCommit 可通过邮件/SNS 通知审查人。
- **分支与标签**：标准 Git 引用；及时清理不再需要的分支/标签以保持操作高效。
- **加密**：仓库静态加密（KMS）且传输加密（TLS）。
- **集成**：与 CodeBuild、CodePipeline、Lambda（触发器）及第三方工具集成。

## 常用操作（AWS CLI）

```bash
# 创建仓库
aws codecommit create-repository --repository-name my-app --region us-east-1

# 克隆并操作
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-app
git add . && git commit -m "initial commit" && git push

# 创建分支和 pull request
aws codecommit create-branch --repository-name my-app \
  --branch-name feature/x --commit-id <commit-id>
aws codecommit create-pull-request --title "Add feature" \
  --targets repositoryName=my-app,sourceReference=feature/x,destinationReference=main

# 列出仓库和分支
aws codecommit list-repositories
aws codecommit list-branches --repository-name my-app
```

## 最佳实践

- 使用 IAM 角色或临时凭证；优先短时凭证而不是长期 Git 凭证。
- 策略要求时使用你控制的 KMS 密钥启用仓库加密。
- 仓库只放代码；数据库、备份或频繁变化的大二进制文件用 S3 存放。
- 生产分支使用带审查人的 pull request，并用 IAM 策略/审批规则保护。
- 配置通知（SNS）接收 PR 和推送事件；用 CloudTrail 监控仓库活动。
- 清理过期分支和标签；大文件资产使用 S3 等替代方案。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 克隆/推送认证失败 | 检查 Git 凭证或 SSH 密钥配置，以及该仓库的 IAM 权限。 |
| 仓库不可见 | 确认区域，以及 IAM 主体是否有 `codecommit:ListRepositories`/`GetRepository`。 |
| 大文件操作变慢 | 大二进制文件移到 S3；频繁变化的大文件会使 Git 增量链性能下降。 |
| Pull request 通知缺失 | 核对 SNS 主题订阅和通知规则。 |
| 推送被拒绝 | 检查分支保护/审批规则以及分支上的 IAM 条件。 |

## 配额

每账户仓库数、仓库大小、文件大小和 API 请求速率有限制。以 AWS CodeCommit 配额页面和 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS CodeCommit？- 用户指南](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)
- [AWS CodeCommit 配额](https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html)
- [AWS CodeCommit 定价](https://aws.amazon.com/codecommit/pricing/)
- [AWS CLI：codecommit 命令](https://docs.aws.amazon.com/cli/latest/reference/codecommit/)
