# AWS Amplify - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Amplify 帮助你在 AWS 上构建和托管全栈 Web/移动应用。**Amplify Hosting** 提供基于 Git 的工作流，持续部署到 AWS 全球 CDN。**Amplify Gen 2** 是当前的 code-first 后端体验：用 TypeScript 定义 data、auth 和 functions，用 `ampx` 管理。Gen 1 应用使用旧版 Amplify CLI 和 Studio。

## 核心概念

- **Amplify Hosting**：连接 Git 仓库（GitHub、Bitbucket、GitLab 或 CodeCommit），以 CI/CD 部署前端。
- **功能分支**：每个连接的分支成为一个环境（生产/预发），各有独立后端。
- **PR 预览**：为拉取请求生成预览应用；支持原子部署和自定义域名。
- **Amplify Gen 2 后端**：TypeScript 定义的 `data`、`auth`、`storage`、`functions` 资源，自动生成云基础设施。
- **Amplify Libraries**：客户端 SDK（JS、React、Swift、Android、Flutter）连接后端。
- **定价**：构建分钟、托管和后端用量按量付费。

## 常用操作

```bash
# Gen 2 后端（项目目录内）
npx ampx sandbox            # 本地开发后端
npx ampx generate outputs   # 生成客户端配置
npx ampx deploy             # 部署后端

# Gen 1 CLI（旧版）
amplify init
amplify add auth
amplify push

# 通过 AWS CLI 托管
aws amplify create-app --name my-app --repository https://github.com/example/my-app \
  --platform WEB
aws amplify list-apps
aws amplify start-deployment --app-id <app-id> --branch-name main --source-url s3://artifact-bucket/app.zip
aws amplify create-branch --app-id <app-id> --branch-name staging
```

## 最佳实践

- 新项目用 Amplify Gen 2；Gen 1 是旧版，只用于存量应用。
- 每个环境连接分支，保护生产分支；用 PR 预览做评审。
- 在后端 schema 中定义 auth 规则，用 sandbox 验证访问模式。
- 保持构建可复现（锁定依赖、固定 Node.js），合理缓存。
- 配置自定义域名和 HTTPS，监控部署日志和构建指标。
- 构建环境变量要安全保管；不要把密钥提交到仓库。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 构建失败 | 查看构建日志、依赖版本和环境变量。 |
| 后端没更新 | 执行 `ampx deploy`（Gen 1 用 `amplify push`）并重新部署前端。 |
| 认证问题 | 核对 auth 规则、用户池/客户端配置和客户端库版本。 |
| 自定义域名不解析 | 检查 DNS 记录和 Amplify Hosting 中的证书状态。 |
| 预览不出现 | 确认 PR 分支命名和应用的预览设置。 |

## 配额

构建分钟、托管存储/流量和后端资源用量有账号限制；以 AWS Amplify 定价页当前层级和配额为准。

## 官方参考

- [欢迎使用 AWS Amplify Hosting](https://docs.aws.amazon.com/amplify/latest/userguide/welcome.html)
- [Amplify Gen 2 文档](https://docs.amplify.aws/)
- [AWS Amplify 定价](https://aws.amazon.com/amplify/pricing/)
