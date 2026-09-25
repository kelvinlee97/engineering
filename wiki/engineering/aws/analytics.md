---
type: Service
title: AWS analytics
description: "Querying, transforming, warehousing, and visualizing data on AWS: Athena, Glue, EMR, Redshift, QuickSight, Data Pipeline, and AppFlow."
tags: [aws, analytics, data]
sources:
  - id: aws-athena
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/athena/README.md
    title: "Amazon Athena - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-glue
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/glue/README.md
    title: "AWS Glue - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-emr
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/emr/README.md
    title: "Amazon EMR - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-redshift
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/redshift/README.md
    title: "Amazon Redshift - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-quicksight
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/quicksight/README.md
    title: "Amazon QuickSight - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-data-pipeline
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/data-pipeline/README.md
    title: "AWS Data Pipeline - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-appflow
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/appflow/README.md
    title: "Amazon AppFlow - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services turn stored data into answers: query it in place, catalog and transform it, process it on clusters, load it into a warehouse, and chart it. Most read from [S3](data-stores.md).

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Amazon Athena](#amazon-athena) | Athena is a query engine with no storage of its own |
| [AWS Glue](#aws-glue) | AWS Glue is a serverless data integration service for discovering, preparing, moving, and integrating data |
| [Amazon EMR](#amazon-emr) | Amazon EMR (formerly Amazon Elastic MapReduce) is a managed cluster platform for running big data frameworks such as Apache Spark, Hive, HBase, Flink, Trino, and Presto |
| [Amazon Redshift](#amazon-redshift) | Redshift is a columnar, massively-parallel warehouse you either run as a provisioned cluster you size yourself (RA3 scales storage independently of compute |
| [Amazon QuickSight](#amazon-quicksight) | QuickSight connects to data sources, models them into datasets served either from the in-memory SPICE cache or live queries, and lets you work in an editable analysis before publishing a read-only dashboard that can be shared or embedded |
| [AWS Data Pipeline](#aws-data-pipeline) | AWS Data Pipeline is a web service for automating the movement and transformation of data between AWS services and on-premises data sources |
| [Amazon AppFlow](#amazon-appflow) | AppFlow is a no-code data-mover between named connectors |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Amazon Athena

Athena is a query engine with no storage of its own: it plans SQL against metadata in a Data Catalog, reads only the S3 bytes that partitioning and file format let it skip past, and every byte scanned is what you pay for. Amazon Athena is a serverless interactive query service for analyzing data directly in Amazon S3 using standard SQL. There is no infrastructure to manage: you point Athena at your data, run queries, and pay per query. Athena also supports interactive Apache Spark analytics through notebooks and APIs.

Key points:

- Workgroup: isolates queries, result settings, and cost controls per team or application.
- Data Catalog: table metadata (typically the AWS Glue Data Catalog) that maps storage locations, file formats, and schemas.
- Query execution: submitted SQL that Athena plans and runs across S3 objects in parallel.
- Federated queries: query data outside S3 (relational stores, DynamoDB, etc.) through Athena data source connectors.
- Partitioning: prune scanned data by partition columns; critical for cost and performance.

Practices:

- Partition tables by date/region and use columnar formats (Parquet) to cut bytes scanned and cost.
- Use workgroups to set result locations and enforce query cost controls.
- Compress and compact data; run `OPTIMIZE` / CTAS maintenance on small files.

| Symptom | Check |
| --- | --- |
| Query fails with table not found | Verify database/table exist in the Glue Data Catalog and the region matches the data. |
| No data returned | Check partition locations, file format registration, and that the data was written with a matching schema. |
| High cost per query | Reduce scanned bytes: partition pruning, Parquet/ORC, and more selective predicates. |
| Permission denied on S3 | Grant Athena (via workgroup/engine) read on the data locations and write on the result bucket. |

Athena enforces per-query and per-account limits (for example, query string size, result set size, concurrent queries, and capacity reservations). See the Service Quotas console for current values.[^aws-athena]


## AWS Glue

AWS Glue is a serverless data integration service for discovering, preparing, moving, and integrating data. It provides a central Data Catalog, crawlers for schema discovery, ETL jobs on Spark or Ray engines, streaming ETL, workflows, and visual tooling (Glue Studio). Data in the catalog is queryable from Athena, EMR, and Redshift Spectrum.

Key points:

- Data Catalog: a central metadata store of databases, tables (schemas), and partitions.
- Crawler: connects to data sources, infers schemas, and populates the Data Catalog.
- ETL job: serverless script (PySpark, Scala, Python, or Ray) that transforms and loads data.
- Glue Studio: graphical interface for building and monitoring ETL jobs.
- Triggers and workflows: schedule, event-based, or dependency-driven job orchestration.

Practices:

- Use crawlers on a schedule (or event-driven) and review inferred schemas before relying on them.
- Keep the Data Catalog close to consumers: query it from Athena, EMR, and Redshift Spectrum.
- Use columnar formats (Parquet) and partition layouts to reduce downstream scan costs.

| Symptom | Check |
| --- | --- |
| Crawler fails | Check IAM role permissions on the source, and network access (VPC) to the data source. |
| No tables in catalog | Verify crawler targets, database name, and that schema inference completed. |
| Job fails | Inspect job logs in CloudWatch, script syntax, and S3 location permissions. |
| Job bookmarks not working | Bookmarks only support append-only sources; enable/verify bookmark state. |

Concurrent crawlers, concurrent job runs, DPU capacity, and Data Catalog objects have per-account quotas. See the Service Quotas console for current values.[^aws-glue]


## Amazon EMR

Amazon EMR (formerly Amazon Elastic MapReduce) is a managed cluster platform for running big data frameworks such as Apache Spark, Hive, HBase, Flink, Trino, and Presto. It supports traditional EC2-based clusters, EMR Serverless, and EMR on EKS.

Key points:

- Cluster: master node plus core and task nodes; core nodes run HDFS, task nodes add compute.
- Release label: versioned bundle (for example, emr-7.5.0) that pins applications and their versions.
- Steps: ordered work units (Spark/Hive jobs) submitted to a cluster.
- Applications: Spark, Hive, HBase, Flink, Trino/Presto, Hue, Zeppelin, and ecosystem tools (Hudi, Iceberg, Delta Lake).
- Auto scaling: scale core/task nodes based on metrics or schedules.

Practices:

- Use EMR Serverless for intermittent workloads and EMR on EC2 for long-running, latency-sensitive clusters.
- Store data in S3 (with EMRFS) rather than HDFS so clusters are ephemeral and data survives termination.
- Use Spot for task nodes and auto scaling to match demand; enable Cluster Auto Scaling.

| Symptom | Check |
| --- | --- |
| Cluster fails to launch | Check IAM roles (EMR_DefaultRole/EMR_EC2_DefaultRole), subnet, key pair, and service quotas. |
| Steps fail | Inspect step logs in CloudWatch/S3, driver logs, and application stderr. |
| Out of memory | Increase executor memory/cores, use dynamic allocation, or scale task nodes. |
| S3 access denied | Verify the instance profile role allows the S3 actions and bucket policy. |

Cluster counts, instance counts per account, and EMR Serverless capacity are subject to service quotas. See the Service Quotas console for current values.[^aws-emr]


## Amazon Redshift

Redshift is a columnar, massively-parallel warehouse you either run as a provisioned cluster you size yourself (RA3 scales storage independently of compute; DC2 is fixed local storage) or as Serverless, which scales RPU capacity for you and can query cold S3 data directly through Spectrum either way. Amazon Redshift is a fully managed, petabyte-scale data warehouse. It uses columnar storage and massively parallel processing (MPP) for fast SQL analytics, and it integrates with the BI and SQL tools you already use. Redshift Serverless removes cluster administration, automatically provisions capacity, scales for demand, and stops charging when idle.

Key points:

- Cluster (provisioned): a set of compute nodes with a leader node; you manage node types, counts, and maintenance windows.
- Redshift Serverless: namespaces (databases) and workgroups; capacity scales automatically in RPUs (Redshift Processing Units).
- Node types: RA3 nodes separate compute from managed storage, letting you scale compute independently; DC2 is for fixed local storage.
- Columnar storage and compression: analytics-optimized layout; choose sort and distribution keys to reduce I/O.
- Redshift Spectrum: query data directly in S3 without loading it into the warehouse.

Practices:

- Choose RA3 for most workloads so storage scales separately from compute; use Serverless for variable/unpredictable demand.
- Design tables with appropriate distribution and sort keys; vacuum and analyze regularly (or use automatic maintenance).
- Load in bulk (COPY from S3 with columnar formats) instead of row-by-row inserts.

| Symptom | Check |
| --- | --- |
| Slow queries | Check distribution/sort keys, table statistics, WLM queues, and whether Spectrum would be cheaper for cold data. |
| Disk full (DC2) | Resize, offload cold data, or move to RA3 managed storage. |
| COPY failures | Validate source file format, IAM role permissions on S3, and column mapping. |
| Connection limits | Increase cluster size, use connection pooling, or add concurrency scaling. |

Cluster counts, node counts, snapshots, and Serverless capacity have per-account quotas. See the Service Quotas console for current values.[^aws-redshift]


## Amazon QuickSight

QuickSight connects to data sources, models them into datasets served either from the in-memory SPICE cache or live queries, and lets you work in an editable analysis before publishing a read-only dashboard that can be shared or embedded. Amazon QuickSight is the business intelligence and data visualization capability of Amazon Quick (the AI-powered service that evolved from QuickSight). It connects to data sources, builds interactive dashboards and analyses, and supports embedding analytics in applications. All existing QuickSight APIs, SDKs, and integrations continue to work.

Key points:

- Data sources: connect to AWS services (Athena, Redshift, RDS, S3), SaaS applications, and databases; data can be imported into SPICE (the in-memory engine) or queried live.
- SPICE: the Super-fast, Parallel, In-memory Calculation Engine that caches imported data for fast interactive analysis.
- Analyses and dashboards: analyses are working documents; dashboards are published, read-only views shared with users.
- Datasets and fields: datasets define the data and its transformations (calculated fields, joins, filters) used in analyses.
- Identity and access: users are managed with IAM Identity Center, IAM federation, or QuickSight-managed users; access is per-user with reader/author/admin roles.

Practices:

- Use SPICE for large, read-heavy datasets and live queries where freshness matters; monitor SPICE capacity.
- Model data in datasets (joins, calculated fields) rather than duplicating transformations in each analysis.
- Publish curated dashboards and restrict access by user/group; use row-level security for multi-tenant data.

| Symptom | Check |
| --- | --- |
| Data source connection fails | Verify network access (VPC/security groups), credentials, and the data source type/region. |
| SPICE refresh fails | Check dataset refresh schedule, source permissions, and SPICE capacity. |
| Dashboard not visible to users | Confirm the user/group has access and the dashboard is published (not just an analysis). |
| Embedding blank | Verify the embed URL/domain allowlist and IAM/QuickSight session permissions. |

SPICE capacity, users, datasets, dashboards, and API request rates have quotas. See the Amazon QuickSight endpoints and quotas page and Service Quotas console for current values.[^aws-quicksight]


## AWS Data Pipeline

AWS Data Pipeline is a web service for automating the movement and transformation of data between AWS services and on-premises data sources. You define a pipeline definition with data-driven activities and dependencies; the pipeline schedules and runs tasks on EC2 instances. Note: AWS Data Pipeline is no longer available to new customers and is in maintenance mode; existing customers can continue using it, and AWS provides migration guidance for moving workloads to other services.

Key points:

- Pipeline definition: specifies the business logic of the data management (activities, schedules, preconditions, resources) in a definition file.
- Pipeline: schedules and runs tasks by provisioning EC2 instances to perform the defined work; you activate the pipeline to start it.
- Task Runner: polls for and performs tasks (for example, copying logs to S3, launching EMR clusters); AWS provides a Task Runner and you can write custom task runners.
- Dependencies: tasks can depend on the successful completion of previous tasks (for example, EMR analysis waits for the last day's data upload).
- Pricing: pay based on how often activities and preconditions are scheduled and where they run; a limited free tier applies to accounts less than 12 months old.

Practices:

- Keep pipeline definitions versioned and test them on a subset of data before production schedules.
- Use preconditions to gate dependent activities instead of hard-coded timing.
- Monitor pipeline runs and set alarms for failed activities; inspect run logs in S3.

| Symptom | Check |
| --- | --- |
| Pipeline stuck | Check precondition status and dependent activity failures in the console/describe-run. |
| Task Runner not running | Verify the task runner is installed/running on the resource and can reach AWS. |
| Activity failed | Review the activity's log output in S3 and the role permissions for the resources used. |
| Definition rejected | Validate the pipeline definition file syntax and object references. |

Pipelines per account, activities/preconditions per pipeline, and API request rates have quotas. See the AWS Data Pipeline endpoints and quotas page and Service Quotas console for current values.[^aws-data-pipeline]


## Amazon AppFlow

AppFlow is a no-code data-mover between named connectors: a flow declares a source, a destination, field mapping/filters, and one of three trigger types, and AppFlow runs it without any custom integration code. Amazon AppFlow is a fully managed integration service for securely exchanging data between SaaS applications (for example, Salesforce, Slack, Zendesk, Marketo) and AWS services (S3, Redshift, Snowflake). You create flows to move records on demand, on a schedule, or in response to events, without writing code.

Key points:

- Flow: the configuration that moves data from a source to a destination, including field mapping, filters, and triggers.
- Connectors: built-in connectors for SaaS sources/destinations and AWS services; custom connectors built with the Custom Connector SDK for private APIs and other systems.
- Trigger types: on-demand (manual), scheduled (cron), or event-driven (SaaS platform events/change data capture).
- Data transformation: map fields, filter records, and aggregate/partition data for downstream analytics.
- PrivateLink: transfer data privately over the AWS network instead of the public internet.

Practices:

- Keep connector profiles in a dedicated account/Region and rotate OAuth credentials securely (Secrets Manager).
- Use scheduled flows for periodic sync and event-triggered flows for near-real-time needs; avoid overlapping runs.
- Map only the fields you need and use filters to reduce transfer volume and cost.

| Symptom | Check |
| --- | --- |
| Connection to SaaS fails | Check OAuth token/refresh, connector profile configuration, and network (VPC/PrivateLink). |
| Flow run failed | Review execution records/error messages and source/destination permissions. |
| Records missing | Verify filters, field mapping, and the source cursor/change data capture configuration. |
| Slow or throttled transfers | Reduce field count, use incremental transfers, and check API rate limits on the source. |

Flows and connector profiles per account, transfer sizes, and API request rates have quotas. See the Amazon AppFlow endpoints and quotas page and Service Quotas console for current values.[^aws-appflow]


## Related

- [Streaming and search](streaming-and-search.md)
- [Data stores](data-stores.md)
- [Domain index](index.md)

[^aws-athena]: [Amazon Athena - Runbook & Reference](../../sources/aws-athena.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/athena/README.md)
[^aws-glue]: [AWS Glue - Runbook & Reference](../../sources/aws-glue.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/glue/README.md)
[^aws-emr]: [Amazon EMR - Runbook & Reference](../../sources/aws-emr.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/emr/README.md)
[^aws-redshift]: [Amazon Redshift - Runbook & Reference](../../sources/aws-redshift.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/redshift/README.md)
[^aws-quicksight]: [Amazon QuickSight - Runbook & Reference](../../sources/aws-quicksight.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/quicksight/README.md)
[^aws-data-pipeline]: [AWS Data Pipeline - Runbook & Reference](../../sources/aws-data-pipeline.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/data-pipeline/README.md)
[^aws-appflow]: [Amazon AppFlow - Runbook & Reference](../../sources/aws-appflow.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/appflow/README.md)
