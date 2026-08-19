# AWS CodeStar - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS CodeStar 曾是一个统一界面，用于设置软件开发项目，提供项目仪表盘、问题跟踪和集成的 CI/CD（CodeCommit、CodeBuild、CodeDeploy、CodePipeline）。AWS 已于 2024 年 7 月 31 日停止对创建和查看 CodeStar 项目的支持：CodeStar 控制台已不可访问，无法创建新项目，CodeStar 的 AWS SDK 客户端也已移除。现有团队应使用底层服务（CodeCommit、CodeBuild、CodeDeploy、CodePipeline）以及 AWS CodeCatalyst 进行项目级协作。

## 核心概念

- **项目**：CodeStar 将代码仓库、构建/部署管道和团队成员集中到一个仪表盘。
- **状态（已退役）**：自 2024 年 7 月 31 日起，无法创建或查看 CodeStar 项目；控制台不可访问，SDK 包已弃用/移除。
- **继任方案**：项目规划与协作使用 CodeCatalyst；CI/CD 使用 Code 系列服务（CodeCommit、CodeBuild、CodeDeploy、CodePipeline）。

## 常用操作

无法再创建新的 CodeStar 资源。如仍有历史资源，通过底层服务管理：

```bash
# 直接管理底层资源
aws codecommit list-repositories
aws codepipeline list-pipelines
aws codebuild list-projects
aws codedeploy list-applications
```

## 最佳实践

- 新项目不要使用 CodeStar；它已停止服务。
- 项目协作使用 AWS CodeCatalyst（规划、仓库、CI/CD）或直接使用 Code 系列服务。
- 通过底层服务归档或删除遗留 CodeStar 资源，清理不再使用的 IAM 角色。
- 更新调用 CodeStar API 的自动化，改用底层服务 API。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无法访问 CodeStar 控制台 | 属预期：CodeStar 已停止服务（2024 年 7 月 31 日）；改用 CodeCatalyst 或 Code 系列服务。 |
| SDK 调用失败 | CodeStar SDK 客户端已移除；迁移到 CodeCommit/CodeBuild/CodeDeploy/CodePipeline API。 |
| 存在旧项目资源 | 通过底层服务定位，审慎迁移或删除。 |

## 配额

CodeStar 已停止服务，无法创建新资源。以 AWS CodeStar 用户指南发布说明和底层服务的配额为准。

## 官方参考

- [AWS CodeStar 用户指南（已归档）](https://docs.aws.amazon.com/codestar/latest/userguide/welcome.html)
- [AWS CodeStar 发布说明（退役）](https://docs.aws.amazon.com/codestar/latest/userguide/history.html)
- [AWS CodeCatalyst](https://codecatalyst.aws/)
