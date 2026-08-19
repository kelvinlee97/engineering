# AWS CloudFormation - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS CloudFormation 用代码建模并预置 AWS 资源。你编写描述所需资源的模板，CloudFormation 以一个整体（堆栈 Stack）创建、更新和删除这些资源，并自动处理依赖关系。

## 核心概念

- **模板（Template）**：YAML 或 JSON，描述资源及其属性。
- **堆栈（Stack）**：由一个模板创建的一组资源，作为一个整体管理。
- **Stack set**：把同一模板应用到多个账户和区域。
- **变更集（Change set）**：应用更新前预览将要发生的变化。
- **漂移检测（Drift detection）**：对比线上资源与模板的差异。
- **嵌套堆栈**：用其他堆栈组合出可复用的堆栈。
- **资源类型**：EC2、RDS、S3、Lambda、IAM 等数千种。

## 常用操作（AWS CLI）

```bash
# 校验模板
aws cloudformation validate-template --template-body file://template.yaml

# 创建堆栈
aws cloudformation create-stack --stack-name my-stack \
  --template-body file://template.yaml --parameters ParameterKey=Env,ParameterValue=prod

# 部署（创建或更新；模板含 IAM 资源时需要 capability）
aws cloudformation deploy --stack-name my-stack \
  --template-file template.yaml --capabilities CAPABILITY_NAMED_IAM

# 变更集（安全更新）
aws cloudformation create-change-set --stack-name my-stack \
  --template-body file://template.yaml --change-set-name my-change
aws cloudformation execute-change-set --stack-name my-stack --change-set-name my-change

# 查看与排障
aws cloudformation describe-stacks --stack-name my-stack
aws cloudformation describe-stack-events --stack-name my-stack
aws cloudformation list-stacks

# 删除
aws cloudformation delete-stack --stack-name my-stack
```

## 最佳实践

- 模板当代码管理：进版本控制、走评审、先在非生产环境测试。
- 生产环境更新用**变更集**，先看影响再执行。
- 有状态资源（数据库、S3 桶）设置 `DeletionPolicy` / `UpdateReplacePolicy`。
- 不要硬编码：用参数、`AWS::SSM::Parameter`、Secrets Manager 引用。
- 最小权限；对 `CAPABILITY_IAM` 保持谨慎。
- 生产堆栈开启**漂移检测**；按生命周期拆分堆栈（网络、数据、应用）。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 堆栈创建失败并回滚 | 用 `describe-stack-events` 找到第一个 `CREATE_FAILED` 事件定位根因。 |
| 更新失败 | 复查变更集；必要时回滚到上一个模板版本。 |
| IAM 资源报错 | 加 `--capabilities CAPABILITY_NAMED_IAM` 重试，或收敛模板中的 IAM 权限。 |
| 依赖错误 | 检查跨堆栈引用和输出名称；正确使用 `Fn::ImportValue`。 |
| 检测到漂移 | 对比模板与线上资源，决定更新堆栈还是修正资源。 |

## 配额

直接传参时模板正文上限 51,200 字节；上传 S3 后 1 MB。堆栈相关配额以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS CloudFormation？- CloudFormation 用户指南](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS CLI：cloudformation 命令](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/)
