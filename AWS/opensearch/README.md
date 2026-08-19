# Amazon OpenSearch Service - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon OpenSearch Service is a managed service for deploying, operating, and scaling OpenSearch clusters. A domain is the managed equivalent of an OpenSearch cluster. It supports OpenSearch (current releases, including 3.x) and legacy Elasticsearch OSS up to 7.10, and is used for log analytics, application monitoring, clickstream analysis, and full-text search.

## Key concepts

- **Domain**: a cluster with configured instance types, counts, storage, and security settings.
- **Data nodes**: EC2 instances that store and query data; domains support up to 1,002 data nodes and 25 PB of attached storage.
- **Dedicated master nodes**: offload cluster-management tasks for stability.
- **UltraWarm and cold storage**: low-cost tiers for read-only data (backed by S3).
- **OpenSearch Dashboards**: built-in visualization and query workbench.
- **Ingestion pipelines**: transform data before indexing (OpenSearch Ingestion).
- **Security**: IAM, VPC placement, encryption at rest and node-to-node, Cognito/basic/SAML for Dashboards, and fine-grained access control.
- **Automated snapshots**: daily snapshots to S3 for backup and restore.
- **Serverless**: OpenSearch Serverless collections with OCU-based scaling.

## Common operations (AWS CLI)

```bash
# Create a domain
aws opensearch create-domain --domain-name logs-prod \
  --engine-version OpenSearch_3.1 \
  --cluster-config InstanceType=m5.large.search,InstanceCount=3,DedicatedMasterEnabled=true \
  --ebs-options EBSEnabled=true,VolumeSize=100,VolumeType=gp3 \
  --encryption-at-rest-options Enabled=true \
  --node-to-node-encryption-options Enabled=true

# List and describe domains
aws opensearch list-domain-names
aws opensearch describe-domain --domain-name logs-prod
aws opensearch describe-domains --domain-names logs-prod

# Scale
aws opensearch update-domain-config --domain-name logs-prod \
  --cluster-config InstanceType=m5.large.search,InstanceCount=5

# Back up / restore via snapshot repositories
aws opensearch create-package --package-name backup-repo --package-type SNAPSHOT \
  --package-source S3BucketName=snapshots-bucket,S3Key=repo

# Delete
aws opensearch delete-domain --domain-name logs-prod
```

## Best practices

- Use UltraWarm/cold tiers for older or read-only data to control cost; keep hot data on data nodes.
- Run three data nodes and dedicated masters in production; place nodes across AZs.
- Enable encryption at rest, node-to-node encryption, and enforce HTTPS on the domain.
- Put domains in a VPC for production; use Cognito/SAML for Dashboards access and fine-grained access control for indexes.
- Take regular manual snapshots to S3 in addition to automated snapshots; test restores.
- Monitor with CloudWatch (cluster status, JVM memory pressure, CPU) and alert on `red` cluster status.
- Upgrade to a standard-support OpenSearch version; extended support for older versions is charged.
- Load streaming data from Kinesis/Firehose/CloudWatch Logs with Lambda or ingestion pipelines.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cluster status `red` | Check for unassigned shards; fix disk space, node count, or replica settings. |
| JVM memory pressure high | Scale instance size, add nodes, or reduce index complexity. |
| Indexing rejected | Check cluster capacity and bulk request sizes; scale or throttle. |
| Cannot access Dashboards | Verify Cognito/basic/SAML config and VPC security groups. |
| Snapshot restore fails | Confirm the snapshot repository IAM role and S3 bucket permissions. |
| Slow queries | Review mappings, shard count/size, and use index patterns suited to the query workload. |

## Limits

Data nodes (up to 1,002), attached storage (up to 25 PB), domains per account, and OCU capacity for Serverless are subject to quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon OpenSearch Service?](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)
- [Amazon OpenSearch Service quotas](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html)
- [Amazon OpenSearch Service pricing](https://aws.amazon.com/opensearch-service/pricing/)
- [AWS CLI: opensearch commands](https://docs.aws.amazon.com/cli/latest/reference/opensearch/)
