# AWS Cloud9 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Cloud9 是基于浏览器的云集成开发环境（IDE），提供代码编辑、调试、内建终端和 AWS 服务集成。**Cloud9 已不再对新客户开放**；现有客户可继续正常使用。

## 核心概念

- **环境（Environment）**：存放项目文件、运行开发工具的位置；连接到一个计算资源。
- **EC2 环境**：由 Cloud9 创建并管理的 EC2 实例（推荐）。
- **SSH 环境**：Cloud9 通过 SSH 连接现有云实例或你自己的服务器。
- **IDE**：浏览器端编辑器，支持多种语言、调试器和终端。
- **集成**：克隆仓库（CodeCommit、GitHub）、运行 Docker、用 AWS CDK 开发、部署无服务器应用。

## 常用操作（AWS CLI）

```bash
# 创建 EC2 环境
aws cloud9 create-environment-ec2 --name devbox \
  --instance-type t3.micro --image-id amazonlinux-2023-x86_64 \
  --subnet-id subnet-0123456789abcdef0

# 查看和更新环境
aws cloud9 describe-environments --environment-ids <env-id>
aws cloud9 describe-environment-memberships --environment-id <env-id>
aws cloud9 update-environment --environment-id <env-id> --name devbox-v2

# 分享给用户
aws cloud9 create-environment-membership --environment-id <env-id> \
  --user-arn arn:aws:iam::123456789012:user/developer --permissions read-write

# 删除
aws cloud9 delete-environment --environment-id <env-id>
```

## 最佳实践

- 注意当前生命周期：新客户入驻已关闭；新项目规划替代方案（如 IDE 工具包 + EC2/CloudShell）。
- 存量环境用 EC2 环境（托管实例），保持 IDE/实例补丁更新。
- 挂最小权限的 IAM 实例配置；不要在环境里存长期密钥。
- 结对用 `read-write`/`read-only` 成员分享，用后移除成员。
- 代码放仓库（CodeCommit/GitHub），让环境可随时重建。
- 空闲时停止 EC2 环境控制成本；删除不再使用的环境。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无法打开 IDE | 检查环境状态，以及浏览器/网络到环境 URL 的访问。 |
| EC2 环境慢 | 调整实例规格，或停止/重启环境。 |
| 权限报错 | 核对所用服务的实例配置/角色策略。 |
| SSH 环境不可达 | 检查服务器 SSH 配置、密钥和安全组规则。 |
| 环境磁盘满 | 扩大实例磁盘或清理工作区。 |

## 配额

每账号环境数和 EC2 环境实例规格受配额限制。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Cloud9？](https://docs.aws.amazon.com/cloud9/latest/user-guide/welcome.html)
- [AWS Cloud9 服务配额](https://docs.aws.amazon.com/cloud9/latest/user-guide/limits.html)
- [AWS CLI：cloud9 命令](https://docs.aws.amazon.com/cli/latest/reference/cloud9/)
