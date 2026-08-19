# AWS Certified Developer - Associate（DVA-C02）- 学习大纲

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 考试概览

DVA-C02 验证开发、测试、部署和调试 AWS 云应用的熟练度。覆盖应用代码编写、AWS 服务使用（包括 Lambda 和数据存储）、安全与加密实现，以及用 CI/CD 自动化部署。

## 官方资源

- [DVA-C02 考试指南](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-02/developer-associate-02.html)
- [AWS 认证总览](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/)

## 内容领域

官方考试指南定义了四个内容领域及其权重：

1. 使用 AWS 服务进行开发。
2. 安全。
3. 部署。
4. 故障排查与优化。

详细任务说明以考试指南为准；本大纲沿用原知识库的结构。

## 版本控制与协作

- **CodeCommit**：托管 Git 仓库，支持分支、拉取请求和基于 IAM 的访问控制。
- **CodeStar**：项目模板和团队仪表盘，用于开发和交付应用。
- 相关：[Git 与仓库工作流](../../../Git/README.md)（如适用）。

## CI/CD

- **CodeBuild**：完全托管的构建服务；从源代码仓库构建并产出工件。
- **CodePipeline**：自动化发布流水线，包含构建、测试、部署等阶段；可与 CodeCommit、CodeBuild、CodeDeploy 和第三方工具集成。
- **CodeDeploy**：自动部署应用到 EC2、Lambda 和本地服务器；支持 in-place、蓝绿、金丝雀策略和回滚。
- 相关概念：部署策略、健康检查和回滚行为。

## 基础设施即代码与平台

- **CloudFormation**：以堆栈方式声明和预置资源；支持变更集和漂移检测。
- **Elastic Beanstalk**：托管平台，无需管理底层基础设施即可部署 Web 应用。
- **OpsWorks**：面向旧式工作负载的配置管理平台（Chef/Puppet）；新项目先评估当前替代方案。
- 相关 runbook：[CloudFormation](../../cloudformation/README.md)。

## 无服务器与 API

- **Lambda**：函数即服务；触发器、并发、环境变量、层和 IAM 角色。
- **Step Functions**：编排 Lambda 和其他服务的状态机；Standard 与 Express 工作流。
- **API Gateway**：在 Lambda 等后端前的 REST、HTTP 和 WebSocket API；缓存、限流和认证。
- 相关 runbook：[Lambda](../../lambda/README.md)、[Step Functions](../../step-functions/README.md)、[API Gateway](../../api-gateway/README.md)。

## 容器

- **ECS**：在 Fargate 或 EC2 上运行容器；任务、服务和负载均衡。
- 相关 runbook：[ECS](../../ecs/README.md)。

## 开发者安全

- 应用用 IAM 角色和策略，遵循最小权限。
- 用 KMS 加密；密钥和参数用 Secrets Manager 和 SSM Parameter Store 管理。
- 保护传输中（TLS）和静态数据。
- 相关 runbook：[IAM](../../iam/README.md)、[KMS](../../kms/README.md)、[Secrets Manager](../../secrets-manager/README.md)。

## 学习计划

1. 通读官方 DVA-C02 考试指南，标注任务说明。
2. 动手实践 Lambda、API Gateway、DynamoDB 和 SDK（boto3/CLI）。
3. 用 CodeCommit、CodeBuild、CodePipeline 搭建小型 CI/CD 流水线。
4. 在 AWS Skill Builder 做官方练习题，针对薄弱领域复习。
5. 报名前再次核对考试指南；AWS 会随时间更新考试范围。

## 练习资源

官方练习题和课程在 AWS Skill Builder 提供。题库内容（含第三方练习集）有意不在此发布。

## 本知识库相关 Runbook

- [Lambda](../../lambda/README.md)、[API Gateway](../../api-gateway/README.md)、[Step Functions](../../step-functions/README.md)
- [ECS](../../ecs/README.md)、[EKS](../../eks/README.md)
- [CloudFormation](../../cloudformation/README.md)、[CDK](../../cdk/README.md)
- [S3](../../s3/README.md)、[DynamoDB](../../dynamodb/README.md)、[SQS](../../sqs/README.md)、[SNS](../../sns/README.md)
- [CLI](../../cli/README.md)、[SDK](../../sdk/README.md)、[boto3](../../boto3/README.md)
- [IAM](../../iam/README.md)、[KMS](../../kms/README.md)、[Secrets Manager](../../secrets-manager/README.md)
