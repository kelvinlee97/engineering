# AWS OpsWorks - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS OpsWorks（OpsWorks Stacks）曾是一项配置管理服务，使用 Chef 自动化 EC2 实例的配置和运维，包括 stack、layer、自动修复（auto healing）和部署。OpsWorks Stacks 已达到生命周期终点：已停止接受新客户，并于 2024 年 5 月 26 日对所有客户停止服务。不要在新工作负载中使用 OpsWorks。

## 核心概念（历史）

- **Stack**：同一区域中资源和配置的容器。
- **Layer**：配置和 recipe 相同的一组 EC2 实例（例如应用层、Web 层、数据库层）。
- **Recipe 与 cookbook**：配置实例的 Chef 脚本；OpsWorks 在生命周期事件（setup、configure、deploy、undeploy、shutdown）中运行它们。
- **自动修复与扩缩**：OpsWorks 替换故障实例，并通过基于负载或基于时间的实例扩展 layer。
- **部署（Deployments）**：将更新的应用代码部署到 layer 中的实例。
- **状态**：服务已于 2024 年 5 月 26 日对新老客户停止；AWS 建议将工作负载迁移到其他解决方案。

## 常用操作

无法再创建新的 OpsWorks 资源。如果仍运行遗留资源，请遵循 AWS 的生命周期终点指引，规划迁移到当前替代服务：

```bash
# 直接用当前服务管理底层资源
aws ec2 describe-instances
aws cloudformation list-stacks
aws ssm describe-instance-information
aws codedeploy list-applications
```

## 迁移选项

- **配置管理**：用 AWS Systems Manager（Run Command、State Manager、Patch Manager）替代 Chef 生命周期 recipe。
- **基础设施即代码**：用 AWS CloudFormation 或 Terraform 实现 stack/layer 式模板；用 EC2 用户数据或自定义 AMI 完成引导。
- **部署**：用 AWS CodeDeploy 或 CI/CD 管道（CodePipeline）发布应用。
- **容器**：容器化工作负载用 Amazon ECS/EKS 或 AWS App Runner。
- **托管平台**：Web/Worker 应用用 Elastic Beanstalk 替代 OpsWorks stack。

## 最佳实践

- 新项目不要使用 OpsWorks；它已停止服务。
- 盘点遗留 OpsWorks 管理的实例，映射到当前服务（运维用 SSM、基础设施用 CloudFormation、部署用 CodeDeploy）。
- 先在部分工作负载上测试迁移，再停用旧 stack。
- 迁移后清理不再使用的 OpsWorks IAM 角色和资源。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无法创建 stack | 属预期：OpsWorks Stacks 已停止服务（2024 年 5 月 26 日）；使用当前配置管理服务。 |
| 遗留 stack 仍在运行 | 将工作负载迁移到 Systems Manager、CloudFormation、CodeDeploy 及容器/托管平台，然后下线。 |
| 仍在使用 Chef recipe | 将 recipe 移植为 SSM 文档（或用户数据），应用部署改用 CodeDeploy。 |

## 配额

OpsWorks Stacks 已停止服务，无法创建新资源。以 AWS OpsWorks 生命周期终点指引和迁移目标服务的配额为准。

## 官方参考

- [AWS OpsWorks Stacks 生命周期终点公告](https://docs.aws.amazon.com/opsworks/latest/userguide/opsworks-stacks-eol.html)
- [AWS Systems Manager 用户指南](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [AWS CodeDeploy 用户指南](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)
