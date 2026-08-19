# AWS Service Catalog - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Service Catalog 让组织创建和管理已批准 IT 服务的目录，从单一资源（基于 AMI 的服务器、数据库、软件）到完整的多层应用架构。管理员用约束和访问控制组装 portfolio；终端用户自助发现并只供给已批准的产品。

## 核心概念

- **产品（Product）**：用户可以供给的 IT 服务；产品基于 CloudFormation 模板（或 Terraform 开源）构建，可包含多个版本。
- **Portfolio**：产品集合，加上约束（启动、模板、stack set、通知约束）和资源标签；通过 IAM 用户/组/角色授予 portfolio 访问权限。
- **已供给产品（Provisioned product）**：用户启动的产品实例；支持更新和终止。
- **自助发现**：终端用户浏览其有权限的产品和 portfolio 并自助启动，无需直接访问底层 AWS 服务。
- **版本控制与复用**：一个产品可加入多个 portfolio；更新产品版本会传播到所有引用它的 portfolio。
- **服务动作与预算**：对已供给产品运行预定义操作，并附加预算约束。

## 常用操作（AWS CLI）

```bash
# 产品与 portfolio
aws servicecatalog create-product --name web-app --owner platform \
  --product-type CLOUD_FORMATION_TEMPLATE \
  --provisioning-artifact-parameters file://artifact.json
aws servicecatalog create-portfolio --display-name Platform --provider-name eng

# 关联与约束
aws servicecatalog associate-product-with-portfolio \
  --product-id <product-id> --portfolio-id <portfolio-id>
aws servicecatalog create-constraint \
  --portfolio-id <portfolio-id> --product-id <product-id> \
  --type LAUNCH --parameters file://launch-constraint.json

# 供给和管理
aws servicecatalog provision-product --product-id <product-id> \
  --provisioning-artifact-id <artifact-id> \
  --provisioned-product-name web-01 \
  --provisioning-parameters file://params.json
aws servicecatalog list-provisioned-products
aws servicecatalog terminate-provisioned-product --provisioned-product-id <pp-id>
```

## 最佳实践

- 把产品当作版本化制品：先在低环境测试新版本，再放入生产 portfolio。
- 用启动约束（实例类型限制、IAM 角色）、模板约束和 stack set 约束强化治理，支持多账户发布。
- 向组/角色而非个人授予 portfolio；用 tag options 保持资源标签一致。
- 用预算监控已供给产品的支出。
- 定期审查目录：下线不再使用的产品和版本，审计已供给产品。
- 与 Control Tower Account Factory 和 Organizations 集成，实现受治理的账户级供给。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 用户看不到产品 | 检查 portfolio 关联、对 portfolio 的 IAM 访问以及产品版本可用性。 |
| 供给失败 | 查看 CloudFormation 栈事件、启动约束角色权限和参数校验。 |
| 更新未生效 | 确认新 provisioning artifact 已关联，且已供给产品已执行更新。 |
| 约束未生效 | 核对约束是否正确附加到 portfolio/产品组合。 |
| 无法终止 | 某些产品需要终止约束/角色；检查 IAM 和栈状态。 |

## 配额

每账户产品、portfolio、约束和已供给产品数量有限制。以 AWS Service Catalog 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Service Catalog？- 管理员指南](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html)
- [AWS Service Catalog 配额](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/limits.html)
- [AWS Service Catalog 定价](https://aws.amazon.com/servicecatalog/pricing/)
- [AWS CLI：servicecatalog 命令](https://docs.aws.amazon.com/cli/latest/reference/servicecatalog/)
