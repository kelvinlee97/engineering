# AWS Serverless Application Model（SAM）与 Serverless Application Repository - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Serverless Application Model（AWS SAM）是用于构建无服务器应用的开源基础设施即代码框架。它扩展 CloudFormation，用简化语法定义 Lambda 函数、API Gateway API、DynamoDB 表等无服务器资源，并提供 SAM CLI 做本地开发、测试、构建和部署。AWS Serverless Application Repository（SAR）是使用 SAM 模板发布和部署无服务器应用的目录。

## 核心概念

- **SAM 模板**：带 SAM 简写（`AWS::Serverless::Function`、`AWS::Serverless::Api`、`AWS::Serverless::SimpleTable` 等）的 CloudFormation 模板；SAM 将其转换为标准 CloudFormation 资源。
- **SAM CLI**：覆盖全生命周期的命令——`sam init`、`sam build`、`sam local invoke/start-api`（本地测试）、`sam deploy`、`sam sync`（持续同步），并支持 Terraform 应用本地调试 Lambda。
- **SAM connectors**：在模板中声明资源间权限；SAM 生成所需 IAM 权限。
- **策略模板（Policies）**：简化 IAM 策略模板（例如 S3 读写、DynamoDB CRUD）附加到函数。
- **Serverless Application Repository**：公开或私有（团队/组织内共享）发布应用，从 Lambda 控制台一键部署，并带版本元数据（readme、源码）。
- **CI/CD**：通过 CodePipeline 用 SAM 模板部署 staging/production 环境。

## 常用操作（SAM CLI）

```bash
# 初始化、构建和本地测试
sam init --runtime python3.12 --name my-app
sam build
sam local invoke MyFunction --event event.json

# 部署（引导式）和同步
sam deploy --guided
sam sync --stack-name my-app --watch

# 发布到 Serverless Application Repository
sam publish -t template.yaml --region us-east-1
```

## 最佳实践

- SAM 模板与应用代码一起纳入版本管理；用 `sam build` 保证打包确定性。
- 部署前用 `sam local` 本地测试并补充集成测试。
- 用 connectors 和策略模板精确限定 IAM 权限；避免宽泛策略。
- 开发期用 `sam sync`，生产用带变更集的 `sam deploy`。
- 为无服务器应用配置 CI/CD（CodePipeline + CodeBuild），分阶段并加审批。
- SAR 发布时补全元数据（readme、源码 URL、许可证），保持版本不可变。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| `sam build` 失败 | 检查运行时/依赖包和构建环境（原生模块需要 Docker）。 |
| 本地调用报错 | 核对事件 JSON、环境变量和 IAM 角色模拟。 |
| 部署失败 | 查看 CloudFormation 事件；检查模板 transform（`AWS::Serverless-2016-10-31`）和权限。 |
| SAR 发布被拒 | 修复元数据校验（语义版本、readme、源码 URL）后重试。 |
| 权限过宽 | 用 SAM 策略模板或 connectors 替代通用策略。 |

## 配额

SAM 模板受 CloudFormation 限制；SAR 有每账户/区域应用与版本限制。以 AWS SAM 和 Serverless Application Repository 文档为准。

## 官方参考

- [什么是 AWS Serverless Application Model？- 开发者指南](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS Serverless Application Repository 开发者指南](https://docs.aws.amazon.com/serverlessrepo/latest/devguide/what-is-serverlessrepo.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
- [AWS SAM 定价](https://aws.amazon.com/serverless/sam/pricing/)
