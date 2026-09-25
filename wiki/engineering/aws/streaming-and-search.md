---
type: Service
title: AWS streaming and search
description: Real-time data streams with Kinesis and MSK, and full-text search with OpenSearch and CloudSearch.
tags: [aws, analytics, streaming, search]
sources:
  - id: aws-kinesis
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/kinesis/README.md
    title: "Amazon Kinesis - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-msk
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/msk/README.md
    title: "Amazon MSK - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-opensearch
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/opensearch/README.md
    title: "Amazon OpenSearch Service - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cloudsearch
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudsearch/README.md
    title: "Amazon CloudSearch - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services handle data in motion and data you search: Kinesis and managed Kafka ingest ordered streams of records, and OpenSearch and CloudSearch index documents for search and log analytics.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Amazon Kinesis](#amazon-kinesis) | Amazon Kinesis is the AWS streaming data platform |
| [Amazon MSK](#amazon-msk) | MSK manages the Kafka control plane for you |
| [Amazon OpenSearch Service](#amazon-opensearch-service) | A domain is a managed OpenSearch cluster where you place data on a spectrum of cost/latency tiers |
| [Amazon CloudSearch](#amazon-cloudsearch) | A CloudSearch domain has two separate front doors |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Amazon Kinesis

Amazon Kinesis is the AWS streaming data platform. It collects, processes, and analyzes real-time data at scale. The platform includes Kinesis Data Streams, Amazon Data Firehose, Managed Service for Apache Flink, and Kinesis Video Streams.

Key points:

- Stream and shard: a shard is a unit of capacity; data is ordered within a shard, and throughput scales with shard count.
- Record: the unit of data (partition key + data blob), retained for a configurable period (default 24 hours, up to 365 days).
- Producers and consumers: producers use `PutRecord`/`PutRecords`; consumers poll with `GetRecords` using the Kinesis Client Library (KCL) for fault tolerance.
- On-demand vs. provisioned mode: on-demand scales shards automatically; provisioned uses a fixed shard count you manage.
- Enhanced fan-out: dedicated 2 MB/s read throughput per consumer via `SubscribeToShard`.

Practices:

- Choose Data Firehose when you just need reliable delivery to storage/analytics; use Data Streams when you need custom consumers or replay.
- Design partition keys so hot keys don't skew a shard; monitor `WriteProvisionedThroughputExceeded`.
- Use the Kinesis Client Library (KCL) for exactly-once-ish, fault-tolerant consumption and dynamic shard handling.

| Symptom | Check |
| --- | --- |
| `ProvisionedThroughputExceededException` | Increase shards, improve partition key distribution, or use on-demand mode. |
| Records lost | Verify retention and consumer checkpointing; KCL checkpoints lag behind if the consumer is slow. |
| High consumer lag | Add shards/consumers, use enhanced fan-out, or move heavy processing downstream. |
| Firehose delivery failures | Check destination permissions, buffering settings, and CloudWatch metrics for the delivery stream. |

Each shard supports 1 MB/s (or 1,000 records/s) write and 2 MB/s read; default retention is 24 hours and can be extended up to 365 days. Stream, shard, and Firehose counts have per-account quotas. See the Service Quotas console for current values.[^aws-kinesis]


## Amazon MSK

MSK manages the Kafka control plane for you: provisioned gives you broker-level control, serverless removes capacity planning entirely, while your applications keep speaking standard Kafka data-plane APIs either way. Amazon Managed Streaming for Apache Kafka (Amazon MSK) is a fully managed service for building and running applications that use Apache Kafka. AWS manages the control plane (cluster create/update/delete); you use standard Apache Kafka data-plane APIs for producing and consuming, so existing applications and tools work unchanged.

Key points:

- Cluster: a group of broker nodes; minimum one broker per Availability Zone.
- MSK Provisioned: you choose broker count/type (Standard or Express brokers); AWS manages ZooKeeper nodes or KRaft controllers.
- MSK Serverless: AWS manages broker capacity; you provision at cluster level and scale automatically.
- Topics, producers, consumers: standard Kafka APIs and tools (kafka-clients, kcat, etc.).
- MSK Connect: managed connectors that stream data to/from Kafka clusters.

Practices:

- Choose MSK Serverless for variable traffic and MSK Provisioned for predictable capacity and control.
- Place brokers across at least three AZs and size broker types for peak throughput.
- Use IAM access control or SASL/SCRAM with secrets in Secrets Manager; enable TLS.

| Symptom | Check |
| --- | --- |
| Producers/consumers can't connect | Verify bootstrap brokers, security group rules, and authentication config. |
| `NotEnoughReplicasException` / under-replicated partitions | Check broker health/disk and replication factor. |
| Disk full | Increase storage or shorten retention; monitor `KafkaDataLogsDiskUsed`. |
| Throttling | Scale broker count/type or use Serverless capacity. |

Clusters per account, brokers per cluster, storage, and Serverless capacity have quotas. See the Service Quotas console for current values.[^aws-msk]


## Amazon OpenSearch Service

A domain is a managed OpenSearch cluster where you place data on a spectrum of cost/latency tiers: hot data nodes for active queries, UltraWarm and cold storage backed by S3 for aging read-only data. Amazon OpenSearch Service is a managed service for deploying, operating, and scaling OpenSearch clusters. A domain is the managed equivalent of an OpenSearch cluster. It supports OpenSearch (current releases, including 3.x) and legacy Elasticsearch OSS up to 7.10, and is used for log analytics, application monitoring, clickstream analysis, and full-text search.

Key points:

- Domain: a cluster with configured instance types, counts, storage, and security settings.
- Data nodes: EC2 instances that store and query data; domains support up to 1,002 data nodes and 25 PB of attached storage.
- Dedicated master nodes: offload cluster-management tasks for stability.
- UltraWarm and cold storage: low-cost tiers for read-only data (backed by S3).
- OpenSearch Dashboards: built-in visualization and query workbench.

Practices:

- Use UltraWarm/cold tiers for older or read-only data to control cost; keep hot data on data nodes.
- Run three data nodes and dedicated masters in production; place nodes across AZs.
- Enable encryption at rest, node-to-node encryption, and enforce HTTPS on the domain.

| Symptom | Check |
| --- | --- |
| Cluster status `red` | Check for unassigned shards; fix disk space, node count, or replica settings. |
| JVM memory pressure high | Scale instance size, add nodes, or reduce index complexity. |
| Indexing rejected | Check cluster capacity and bulk request sizes; scale or throttle. |
| Cannot access Dashboards | Verify Cognito/basic/SAML config and VPC security groups. |

Data nodes (up to 1,002), attached storage (up to 25 PB), domains per account, and OCU capacity for Serverless are subject to quotas. See the Service Quotas console for current values.[^aws-opensearch]


## Amazon CloudSearch

A CloudSearch domain has two separate front doors: a document endpoint for writes and a search endpoint for reads, and data uploaded through the first is not searchable until an explicit indexing step runs, so "upload" and "make searchable" are two distinct operations, not one. Amazon CloudSearch is a fully managed search service for building search solutions over large collections of data such as web pages, documents, forum posts, and product information. You create a search domain, upload data, and query through an HTTP search endpoint. Note: Amazon CloudSearch is no longer available to new customers; existing customers can continue using the service.

Key points:

- Search domain: a domain contains your searchable data and the search instances that serve requests; create separate domains for separate collections.
- Indexing: CloudSearch indexes structured data and plain text; the index is deployed to one or more search instances.
- Search features: full-text search with language-specific text processing, boolean, prefix and range searches, term boosting, faceting, highlighting, and autocomplete suggestions.
- Endpoints: a configuration endpoint (per Region) manages domains; each domain has a document endpoint (`doc-<domain>-<id>...`) for uploads and a search endpoint (`search-<domain>-<id>...`) for queries; results are JSON or XML.
- Scaling: add/remove search instances as data volume and traffic change.

Practices:

- Define a clear indexing schema (fields, facets, suggester) before uploading large batches.
- Batch document uploads and index once per batch to reduce indexing overhead.
- Size search instances to your data volume and query traffic; monitor latency and scale out proactively.

| Symptom | Check |
| --- | --- |
| Documents not searchable | Confirm documents uploaded to the document endpoint and `index-documents` ran successfully. |
| Search returns no results | Check the query parser, field names, and that the index is in ACTIVE state. |
| Domain endpoint unknown | Get the endpoints from `describe-domains`; they include account/domain identifiers. |
| Slow search | Increase search instances or reduce result size; review facet/aggregation usage. |

Domains per account, search instances per domain, document sizes, and API rates have quotas; service onboarding is limited to existing customers. See the Amazon CloudSearch endpoints and quotas page for current values.[^aws-cloudsearch]


## Related

- [AWS analytics](analytics.md)
- [AWS messaging](messaging.md): queues and events, when ordering and replay are not the point.
- [Domain index](index.md)

[^aws-kinesis]: [Amazon Kinesis - Runbook & Reference](../../sources/aws-kinesis.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/kinesis/README.md)
[^aws-msk]: [Amazon MSK - Runbook & Reference](../../sources/aws-msk.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/msk/README.md)
[^aws-opensearch]: [Amazon OpenSearch Service - Runbook & Reference](../../sources/aws-opensearch.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/opensearch/README.md)
[^aws-cloudsearch]: [Amazon CloudSearch - Runbook & Reference](../../sources/aws-cloudsearch.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudsearch/README.md)
