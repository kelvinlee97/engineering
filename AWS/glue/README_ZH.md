# AWS Glue - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Glue 是无服务器数据集成服务，用于发现、准备、移动和整合数据。它提供集中式 Data Catalog、schema 发现的爬虫、Spark 或 Ray 引擎的 ETL 作业、流式 ETL、工作流和可视化工具（Glue Studio）。目录中的数据可由 Athena、EMR 和 Redshift Spectrum 查询。

## 核心概念

- **Data Catalog**：数据库、表（schema）和分区的集中元数据存储。
- **爬虫（Crawler）**：连接数据源、推断 schema 并写入 Data Catalog。
- **ETL 作业**：无服务器脚本（PySpark、Scala、Python 或 Ray），负责转换和加载数据。
- **Glue Studio**：可视化构建和监控 ETL 作业的界面。
- **触发器和工作流**：按计划、事件或依赖关系编排作业。
- **流式 ETL**：在传输中消费和转换流数据（Kinesis、Kafka）。
- **交互式会话与笔记本**：交互式开发和调试 ETL 代码。
- **敏感数据检测**：在流水线和数据湖中发现并保护敏感数据。

## 常用操作（AWS CLI）

```bash
# 创建数据库和爬虫
aws glue create-database --database-input Name=analytics
aws glue create-crawler --name s3-crawler --role arn:aws:iam::123456789012:role/glue-role \
  --database-name analytics \
  --targets '{"S3Targets":[{"Path":"s3://data-bucket/raw/"}]}'

# 运行并监控爬虫
aws glue start-crawler --name s3-crawler
aws glue get-crawler --name s3-crawler
aws glue list-crawlers

# 创建并运行 ETL 作业
aws glue create-job --name etl-clean --role arn:aws:iam::123456789012:role/glue-role \
  --command Name=glueetl,ScriptLocation=s3://scripts-bucket/etl.py,PythonVersion=3
aws glue start-job-run --job-name etl-clean
aws glue get-job-runs --job-name etl-clean

# 触发器
aws glue create-trigger --name nightly --type SCHEDULED \
  --schedule "cron(0 2 * * ? *)" --actions JobName=etl-clean --start-on-creation
```

## 最佳实践

- 按计划（或事件触发）运行爬虫，并先审阅推断出的 schema 再使用。
- 让 Data Catalog 贴近消费者：Athena、EMR、Redshift Spectrum 直接查询。
- 用列式格式（Parquet）和合理分区布局，降低下游扫描成本。
- 作业脚本放 S3 并做版本管理；增量处理用 job bookmark。
- 开发用 Glue Studio 和交互式会话，脚本按环境逐步发布。
- 按负载设置作业容量（DPU），用 CloudWatch 监控作业指标。
- 用敏感数据检测和 Lake Formation 访问控制保护数据。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 爬虫失败 | 检查数据源 IAM 角色权限，以及到数据源（VPC）的网络。 |
| 目录里没有表 | 检查爬虫目标、数据库名和 schema 推断是否完成。 |
| 作业失败 | 查看 CloudWatch 作业日志、脚本语法和 S3 位置权限。 |
| bookmark 不生效 | bookmark 只支持追加型数据源；确认已启用且状态正确。 |
| ETL 慢 | 增加 DPU、用列式格式，合理 coalesce/repartition。 |

## 配额

并发爬虫数、并发作业数、DPU 容量和 Data Catalog 对象数有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Glue？](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [AWS Glue 服务配额](https://docs.aws.amazon.com/glue/latest/dg/glue-limits.html)
- [AWS Glue 定价](https://aws.amazon.com/glue/pricing/)
- [AWS CLI：glue 命令](https://docs.aws.amazon.com/cli/latest/reference/glue/)
