# AWS CLI - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Command Line Interface（AWS CLI）是开源的命令行工具，用于在 shell 中操作 AWS 服务。版本 2 是当前主版本，支持全部最新功能；通过官方捆绑安装包安装。CLI 提供与服务 API 一致的能力，并针对部分服务提供更高级的定制命令。

## 核心概念

- **凭据链**：CLI 按顺序从命令行参数、环境变量、共享 `~/.aws/credentials`、IAM 角色（EC2/EKS/ECS）、SSO 和容器角色解析凭据。
- **配置文件（Profile）**：`~/.aws/config` 和 `~/.aws/credentials` 中的命名凭据/区域组合；用 `--profile` 或 `AWS_PROFILE` 选择。
- **区域与输出**：用 `aws configure` 设置默认区域和输出格式（`json`、`yaml`、`text`、`table`）。
- **SSO**：`aws configure sso` 配置 IAM Identity Center 会话；`aws sso login` 刷新会话。
- **查询与过滤**：`--query`（JMESPath）和 `--output` 决定命令结果的形态，便于脚本处理。
- **返回码与 dry-run**：非零退出码表示失败；支持处 `--dry-run` 只校验权限、不实际变更。

## 常用操作（AWS CLI）

```bash
# 安装（macOS 捆绑安装包）
curl "https://awscli.amazonaws.com/AWSIV2.pkg" -o "AWSIV2.pkg"
sudo installer -pkg AWSIV2.pkg -target /

# 配置
aws configure
aws configure set default.region us-east-1
aws configure set default.output json

# 配置文件与 SSO
aws configure --profile dev
aws configure sso --profile dev-sso
aws sso login --profile dev-sso

# 验证身份和权限
aws sts get-caller-identity
aws iam get-user

# 常见用法
aws s3 ls --profile dev
aws ec2 describe-instances --region ap-southeast-1 \
  --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name}' --output table
aws s3 cp file.txt s3://bucket/ --dryrun
```

## 最佳实践

- 不要把长期访问密钥写进脚本或源码；优先用 IAM 角色或 SSO。
- 每个环境/账号用独立 profile，角色遵循最小权限。
- 固定并升级 CLI 版本：v1 仅维护、缺少 v2 功能；使用官方安装包。
- 用 `--query` 和 `--output` 让脚本输出确定；尽量用 `jq` 或 JSON 解析。
- 开启 CloudTrail 审计 CLI 变更；破坏性操作前先 `--dry-run`。
- 持久资源优先用基础设施即代码（CloudFormation/CDK/Terraform），而不是临时 CLI 命令。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| `Unable to locate credentials` | 配置凭据/profile 或设置环境变量；检查凭据链顺序。 |
| `AccessDenied` | 核对 IAM 策略以及当前使用的 profile/角色。 |
| SSO 会话过期 | 重新执行 `aws sso login --profile <profile>`。 |
| 区域结果不对 | 显式加 `--region`，或修正 profile 默认区域。 |
| 脚本 JSON 解析报错 | 校验 `--query`（JMESPath）语法，使用 `--output json`。 |

## 配额

CLI 本身没有服务配额；各服务的 API 限速和配额仍适用。以 Service Quotas 控制台各服务当前值为准。

## 官方参考

- [什么是 AWS Command Line Interface？](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [AWS CLI 命令参考](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS SDKs and Tools 参考指南](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html)
