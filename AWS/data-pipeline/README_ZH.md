# AWS Data Pipeline - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Data Pipeline 是用于自动化 AWS 服务与本地数据源之间数据移动和转换的 Web 服务。你定义包含数据驱动活动和依赖关系的管道定义，管道在 EC2 实例上调度并运行任务。注意：AWS Data Pipeline 已不再向新客户开放且处于维护模式；现有客户可继续使用，AWS 提供将工作负载迁移到其他服务的指引。

## 核心概念

- **管道定义（Pipeline definition）**：以定义文件指定数据管理的业务逻辑（活动、计划、前置条件、资源）。
- **管道（Pipeline）**：通过供给 EC2 实例执行定义的工作来调度和运行任务；激活管道后开始运行。
- **Task Runner**：轮询并执行任务（例如将日志复制到 S3、启动 EMR 集群）；AWS 提供 Task Runner，你也可以编写自定义任务执行器。
- **依赖关系**：任务可依赖前序任务的成功完成（例如 EMR 分析等待最后一天的数据上传完成）。
- **定价**：按活动与前置条件被调度的频率和运行位置付费；创建不足 12 个月的账户有少量免费额度。

## 常用操作（AWS CLI）

```bash
# 创建并激活管道
aws datapipeline create-pipeline --name log-archive --unique-id log-archive
aws datapipeline put-pipeline-definition --pipeline-id <pipeline-id> \
  --pipeline-definition file://definition.json
aws datapipeline activate-pipeline --pipeline-id <pipeline-id>

# 查看管道与运行
aws datapipeline list-pipelines
aws datapipeline describe-pipelines --pipeline-ids <pipeline-id>
aws datapipeline describe-run --pipeline-id <pipeline-id> \
  --pipeline-object-id <object-id>

# 停用和删除
aws datapipeline deactivate-pipeline --pipeline-id <pipeline-id>
aws datapipeline delete-pipeline --pipeline-id <pipeline-id>
```

## 最佳实践

- 管道定义纳入版本管理，先在小数据集上测试再上生产计划。
- 用前置条件（preconditions）控制依赖活动，而不是硬编码时间。
- 监控管道运行，为失败活动设置告警；在 S3 中查看运行日志。
- 合理设置定义中的 EC2 资源规格以控制成本。
- 现有客户：规划迁移到当前服务（例如 AWS Glue、Step Functions、EventBridge Scheduler），因为服务处于维护模式且新客户无法开通。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 管道卡住 | 在控制台/describe-run 中检查前置条件状态和依赖活动失败原因。 |
| Task Runner 未运行 | 确认任务执行器已安装/运行在资源上，且可访问 AWS。 |
| 活动失败 | 查看活动在 S3 中的日志输出，以及所用资源的角色权限。 |
| 定义被拒绝 | 校验管道定义文件语法和对象引用。 |
| 无法开通新管道 | 该服务已对新手关闭；改用当前 AWS 数据编排服务。 |

## 配额

每账户管道数、每管道活动/前置条件数以及 API 请求速率有限制。以 AWS Data Pipeline 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Data Pipeline？- 开发者指南](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/what-is-datapipeline.html)
- [从 AWS Data Pipeline 迁移工作负载](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/migrate.html)
- [AWS Data Pipeline 定价](https://aws.amazon.com/datapipeline/pricing/)
- [AWS CLI：datapipeline 命令](https://docs.aws.amazon.com/cli/latest/reference/datapipeline/)
