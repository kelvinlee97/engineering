# Amazon EMR - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon EMR (formerly Amazon Elastic MapReduce) is a managed cluster platform for running big data frameworks such as Apache Spark, Hive, HBase, Flink, Trino, and Presto. It supports traditional EC2-based clusters, EMR Serverless, and EMR on EKS.

## Deployment models

| Model | Description |
|---|---|
| EMR on EC2 | Provisioned cluster of EC2 instances with a chosen release and applications |
| EMR Serverless | Run Spark/Hive jobs without managing clusters; pay per job |
| EMR on EKS | Run Spark workloads on Amazon EKS with the EMR Spark runtime |

## Key concepts

- **Cluster**: master node plus core and task nodes; core nodes run HDFS, task nodes add compute.
- **Release label**: versioned bundle (for example, emr-7.5.0) that pins applications and their versions.
- **Steps**: ordered work units (Spark/Hive jobs) submitted to a cluster.
- **Applications**: Spark, Hive, HBase, Flink, Trino/Presto, Hue, Zeppelin, and ecosystem tools (Hudi, Iceberg, Delta Lake).
- **Auto scaling**: scale core/task nodes based on metrics or schedules.
- **Spot instances**: use Spot for task nodes to cut cost; keep core on On-Demand.
- **Integrations**: S3 (S3A), Glue Data Catalog, DynamoDB, Kinesis, and EMRFS for S3 storage.

## Common operations (AWS CLI)

```bash
# Create a Spark cluster (use default EMR roles)
aws emr create-cluster --name analytics --release-label emr-7.5.0 \
  --applications Name=Spark \
  --ec2-attributes KeyName=my-key,InstanceProfile=EMR_EC2_DefaultRole \
  --instance-groups InstanceGroupType=MASTER,InstanceType=m5.xlarge,InstanceCount=1 \
    InstanceGroupType=CORE,InstanceType=m5.xlarge,InstanceCount=2 \
  --service-role EMR_DefaultRole \
  --auto-terminate

# List and describe clusters
aws emr list-clusters --cluster-states RUNNING WAITING
aws emr describe-cluster --cluster-id j-XXXXXXXXXXXXX

# Add a step (Spark job)
aws emr add-steps --cluster-id j-XXXXXXXXXXXXX \
  --steps Type=Spark,Name=ETL,ActionOnFailure=CONTINUE,Args=[--class,com.example.ETL,s3://bucket/job.jar]

# Terminate
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX
```

## Best practices

- Use EMR Serverless for intermittent workloads and EMR on EC2 for long-running, latency-sensitive clusters.
- Store data in S3 (with EMRFS) rather than HDFS so clusters are ephemeral and data survives termination.
- Use Spot for task nodes and auto scaling to match demand; enable Cluster Auto Scaling.
- Use the Glue Data Catalog for shared table metadata with Athena and Redshift Spectrum.
- Submit work as steps or orchestrate with Step Functions; monitor via CloudWatch and EMR managed scaling metrics.
- Configure encryption (S3 SSE, in-transit TLS) and keep cluster subnets private.
- Pin release labels and test application upgrades in a staging cluster.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cluster fails to launch | Check IAM roles (EMR_DefaultRole/EMR_EC2_DefaultRole), subnet, key pair, and service quotas. |
| Steps fail | Inspect step logs in CloudWatch/S3, driver logs, and application stderr. |
| Out of memory | Increase executor memory/cores, use dynamic allocation, or scale task nodes. |
| S3 access denied | Verify the instance profile role allows the S3 actions and bucket policy. |
| Slow Spark jobs | Tune partitioning, use columnar formats, and enable EMRFS consistent view if needed. |

## Limits

Cluster counts, instance counts per account, and EMR Serverless capacity are subject to service quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon EMR?](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [EMR Serverless user guide](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)
- [Amazon EMR pricing](https://aws.amazon.com/emr/pricing/)
- [AWS CLI: emr commands](https://docs.aws.amazon.com/cli/latest/reference/emr/)
