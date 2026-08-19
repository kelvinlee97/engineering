# AWS Glue - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Glue is a serverless data integration service for discovering, preparing, moving, and integrating data. It provides a central Data Catalog, crawlers for schema discovery, ETL jobs on Spark or Ray engines, streaming ETL, workflows, and visual tooling (Glue Studio). Data in the catalog is queryable from Athena, EMR, and Redshift Spectrum.

## Key concepts

- **Data Catalog**: a central metadata store of databases, tables (schemas), and partitions.
- **Crawler**: connects to data sources, infers schemas, and populates the Data Catalog.
- **ETL job**: serverless script (PySpark, Scala, Python, or Ray) that transforms and loads data.
- **Glue Studio**: graphical interface for building and monitoring ETL jobs.
- **Triggers and workflows**: schedule, event-based, or dependency-driven job orchestration.
- **Streaming ETL**: consume and transform streaming data in transit (Kinesis, Kafka).
- **Interactive sessions and notebooks**: develop and debug ETL code interactively.
- **Sensitive data detection**: identify and protect sensitive data in pipelines and the data lake.

## Common operations (AWS CLI)

```bash
# Create a database and crawler
aws glue create-database --database-input Name=analytics
aws glue create-crawler --name s3-crawler --role arn:aws:iam::123456789012:role/glue-role \
  --database-name analytics \
  --targets '{"S3Targets":[{"Path":"s3://data-bucket/raw/"}]}'

# Run and monitor the crawler
aws glue start-crawler --name s3-crawler
aws glue get-crawler --name s3-crawler
aws glue list-crawlers

# Create and run an ETL job
aws glue create-job --name etl-clean --role arn:aws:iam::123456789012:role/glue-role \
  --command Name=glueetl,ScriptLocation=s3://scripts-bucket/etl.py,PythonVersion=3
aws glue start-job-run --job-name etl-clean
aws glue get-job-runs --job-name etl-clean

# Triggers
aws glue create-trigger --name nightly --type SCHEDULED \
  --schedule "cron(0 2 * * ? *)" --actions JobName=etl-clean --start-on-creation
```

## Best practices

- Use crawlers on a schedule (or event-driven) and review inferred schemas before relying on them.
- Keep the Data Catalog close to consumers: query it from Athena, EMR, and Redshift Spectrum.
- Use columnar formats (Parquet) and partition layouts to reduce downstream scan costs.
- Store job scripts in S3 and version them; use job bookmarks for incremental processing.
- Use Glue Studio and interactive sessions for development; promote scripts through environments.
- Set job capacity (DPUs) based on workload and monitor job metrics in CloudWatch.
- Protect sensitive data with Glue sensitive data detection and Lake Formation access controls.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Crawler fails | Check IAM role permissions on the source, and network access (VPC) to the data source. |
| No tables in catalog | Verify crawler targets, database name, and that schema inference completed. |
| Job fails | Inspect job logs in CloudWatch, script syntax, and S3 location permissions. |
| Job bookmarks not working | Bookmarks only support append-only sources; enable/verify bookmark state. |
| Slow ETL | Increase DPUs, use columnar formats, and coalesce/repartition appropriately. |

## Limits

Concurrent crawlers, concurrent job runs, DPU capacity, and Data Catalog objects have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Glue?](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [AWS Glue service quotas](https://docs.aws.amazon.com/glue/latest/dg/glue-limits.html)
- [AWS Glue pricing](https://aws.amazon.com/glue/pricing/)
- [AWS CLI: glue commands](https://docs.aws.amazon.com/cli/latest/reference/glue/)
