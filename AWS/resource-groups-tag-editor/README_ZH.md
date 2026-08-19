# AWS Resource Groups & Tag Editor - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Resource Groups 让你将 AWS 资源（EC2 实例、CloudFormation 栈、S3 桶等）组织成组，从而一次性查看和管理大量资源。Tag Editor 让你按标签搜索资源，并批量添加、删除或替换标签。两者共同支撑标签最佳实践、成本分配和自动化。

## 核心概念

- **资源（Resource）**：你可以在 AWS 中操作的实体（例如 EC2 实例、CloudFormation 栈或 S3 桶）。
- **标签（Tags）**：用于组织资源的键值对元数据；用于计费和管理。不要在标签中存放 PII 或机密数据。
- **资源组（Resource group）**：同一区域中匹配某个查询的资源集合。
  - **基于标签**：成员资格来自资源类型和标签查询（AND 语义）。
  - **基于 CloudFormation 栈**：成员资格来自单个栈（可选限制为栈内资源类型）。
  - **服务关联（Service-linked）**：部分服务自己定义和管理资源组。
  - **嵌套**：资源组可包含同一区域中的其他资源组。
- **Tag Editor**：按标签/资源类型搜索受支持资源并批量编辑标签。
- **权限**：Resource Groups 权限是账户级的；具备相应 IAM 权限的主体即可使用资源组。

## 常用操作（AWS CLI）

```bash
# 创建基于标签的资源组
aws resource-groups create-group --name prod-ec2 \
  --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::EC2::Instance\"],\"TagFilters\":[{\"Key\":\"Env\",\"Values\":[\"prod\"]}]}"}'

# 列出和获取资源组
aws resource-groups list-groups
aws resource-groups get-group --group-name prod-ec2

# 用 Tag Editor（resourcegroupstaggingapi）批量打标签
aws resourcegroupstaggingapi get-resources --tag-filters Key=Env,Values=prod
aws resourcegroupstaggingapi tag-resources \
  --resource-arn-list arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef0 \
  --tags Owner=platform
aws resourcegroupstaggingapi get-tag-values --key Env
```

## 最佳实践

- 定义全公司标签规范（环境、所有者、成本中心、应用），并用 Organizations 标签策略强制。
- 用标签做成本分配：在 Billing 激活成本分配标签，使 Cost Explorer 按标签分组。
- 用基于标签的资源组做运维视图（按环境或应用）和批量操作。
- 标签中绝不放敏感数据；标签是计费和管理可见的元数据。
- 清理过期标签，并对新资源强制必填标签（创建时打标签策略）。
- 将 Resource Groups 与 Systems Manager 结合，对分组实例批量执行命令/补丁。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 资源组返回空 | 检查标签拼写/值、资源类型，以及资源是否在同一区域。 |
| 标签未应用 | 确认资源支持打标签，以及 IAM 对该服务打标签 API 的权限。 |
| 成本未按标签分组 | 在 Billing 中为账户激活成本分配标签。 |
| Tag Editor 搜索为空 | 放宽资源类型过滤；Tag Editor 按区域索引受支持资源。 |
| 跨服务资源组为空 | 确认所选类型对应的每个服务都支持 Resource Groups 查询。 |

## 配额

每账户资源组数、每资源标签数和 API 请求速率有限制。以 AWS Resource Groups 配额页面和 Service Quotas 控制台为准。

## 官方参考

- [什么是资源组？- 用户指南](https://docs.aws.amazon.com/ARG/latest/userguide/resource-groups.html)
- [Tag Editor 用户指南](https://docs.aws.amazon.com/tag-editor/latest/userguide/tag-editor.html)
- [AWS 标签最佳实践](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)
- [AWS CLI：resource-groups 和 resourcegroupstaggingapi 命令](https://docs.aws.amazon.com/cli/latest/reference/resource-groups/)
