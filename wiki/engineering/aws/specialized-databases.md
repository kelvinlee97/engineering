---
type: Service
title: AWS specialized databases
description: "Purpose-built AWS databases beyond RDS and DynamoDB: DocumentDB, Neptune, QLDB, and Managed Blockchain."
tags: [aws, database]
sources:
  - id: aws-documentdb
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/documentdb/README.md
    title: "Amazon DocumentDB - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-neptune
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/neptune/README.md
    title: "Amazon Neptune - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-qldb
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/qldb/README.md
    title: "Amazon QLDB - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-managed-blockchain
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/managed-blockchain/README.md
    title: "Amazon Managed Blockchain (AMB) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
Beyond the core [data stores](data-stores.md), AWS offers databases shaped for one data model: documents, graphs, and verifiable ledgers.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Amazon DocumentDB](#amazon-documentdb) | Amazon DocumentDB (with MongoDB compatibility) is a fast, reliable, fully managed document database |
| [Amazon Neptune](#amazon-neptune) | A Neptune cluster is one primary and up to 15 replicas all reading the same self-healing, multi-AZ cluster volume |
| [Amazon QLDB](#amazon-qldb) | QLDB reached end of support on July 31, 2025 |
| [Amazon Managed Blockchain (AMB)](#amazon-managed-blockchain-amb) | AMB has two independent shapes |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Amazon DocumentDB

Amazon DocumentDB (with MongoDB compatibility) is a fast, reliable, fully managed document database. You can run the same application code, drivers, and tools you use with MongoDB. It separates storage from compute: a cluster volume is replicated six ways across three Availability Zones and grows automatically as data grows.

Key points:

- Cluster: one primary instance plus up to 15 replicas sharing a cluster volume; all instances can serve reads.
- Elastic clusters: a deployment type for millions of reads/writes per second and petabyte-scale storage.
- Storage growth: storage grows automatically in 10 GB increments, up to 256 TiB for engine version 8.0+ (128 TiB for earlier versions).
- Reader endpoint: a stable endpoint that load-balances reads across replicas.
- Backups: automatic, continuous, incremental backups to S3 with point-in-time recovery (up to the last 5 minutes); retention up to 35 days.

Practices:

- Right-size the primary and add replicas in different AZs for reads and failover; use the reader endpoint in applications.
- Enable automated backups and set retention per your RPO; test PITR restores.
- Use indexes that match your MongoDB query patterns; use `explain` to validate.

| Symptom | Check |
| --- | --- |
| Connection failures | Check security groups, TLS settings, and that the client uses the cluster endpoint (port 27017). |
| Read latency | Add replicas and use the reader endpoint; check replica lag. |
| Storage full | DocumentDB grows automatically; if at the engine limit, evaluate elastic clusters or archive data. |
| Slow queries | Review indexes and query patterns with `explain`; adjust instance class if CPU-bound. |

Up to 15 replicas per cluster; storage up to 256 TiB (engine 8.0+) or 128 TiB (earlier engines); backup retention up to 35 days. Cluster and instance counts have per-account quotas. See the Service Quotas console for current values.[^aws-documentdb]


## Amazon Neptune

A Neptune cluster is one primary and up to 15 replicas all reading the same self-healing, multi-AZ cluster volume: writes always go through the primary, reads scale out across replicas. Amazon Neptune is a fast, reliable, fully managed graph database for highly connected datasets. It supports property graphs (Apache TinkerPop Gremlin and openCypher) and RDF graphs (SPARQL), and is used for fraud detection, recommendation engines, knowledge graphs, drug discovery, and network security.

Key points:

- DB cluster: a primary instance plus up to 15 read replicas sharing a cluster volume.
- Cluster volume: SSD-backed storage replicated across three Availability Zones; durable, self-healing, and grows automatically.
- Property graph vs. RDF: choose Gremlin/openCypher for property graphs or SPARQL for RDF data.
- Neptune Analytics: an analytics engine that loads large graph datasets (from Neptune or a data lake) into memory for fast analysis.
- Backups: continuous backups to S3 and point-in-time recovery (PITR).

Practices:

- Model data as a graph deliberately: high-fanout nodes and deep traversals are where graph databases win over relational joins.
- Use replicas for reads and automatic failover; keep the primary for writes.
- Design IDs and indexes (for Gremlin/SPARQL) to match query patterns; avoid full-graph scans.

| Symptom | Check |
| --- | --- |
| Slow traversals | Review query plans, add indexes, and reduce super-node traversal. |
| Write throughput low | Scale the primary instance class; Neptune is read-scalable, writes go through the primary. |
| Failover issues | Confirm replicas are in different AZs and check replica lag. |
| PITR unavailable | Ensure backup retention is configured (PITR requires automated backups). |

Up to 15 replicas per cluster; instance classes, clusters per account, and storage growth are subject to quotas. See the Service Quotas console for current values.[^aws-neptune]


## Amazon QLDB

QLDB reached end of support on July 31, 2025: treat this article only as a runbook for exporting and decommissioning existing ledgers on the way to Amazon Aurora PostgreSQL, never as a starting point for new work. Amazon Quantum Ledger Database (Amazon QLDB) was a fully managed ledger database with an append-only journal, cryptographic verification, and PartiQL queries. Amazon QLDB reached end of support on July 31, 2025. Existing customers were guided to migrate QLDB ledgers to Amazon Aurora PostgreSQL. Do not build new systems on QLDB.

Key points:

- Ledger: the QLDB database resource holding an immutable, append-only journal.
- Journal: a cryptographically chained log of all changes to the ledger.
- Digest and verification: hash-based integrity checks proving the journal was not modified.
- PartiQL: the SQL-compatible query language used to read and write documents.
- Migration path: Amazon Aurora PostgreSQL with an append-only/audit design is the documented replacement for ledger workloads.

Practices:

- Do not start new projects on QLDB; it is end-of-life. Evaluate Amazon Aurora PostgreSQL or an alternative ledger/audit architecture.
- If you operate existing QLDB ledgers, plan and execute the migration to Aurora PostgreSQL before decommissioning.
- Export journal contents to S3 as a retention record before deletion.

| Symptom | Check |
| --- | --- |
| Cannot create a new ledger | Expected: the service is end-of-life; new deployments are no longer supported. |
| Migration questions | Follow the official guide for migrating QLDB ledgers to Amazon Aurora PostgreSQL. |
| Decommissioning | Export journals to S3, then delete ledgers and remove associated IAM roles/policies. |

The service is end-of-life (support ended July 31, 2025). Existing capacity limits no longer apply to new usage; plan decommissioning and migration.[^aws-qldb]


## Amazon Managed Blockchain (AMB)

AMB has two independent shapes: AMB Access gives you API access into public Ethereum/Bitcoin nodes, while private networks let you run a permissioned Hyperledger Fabric network made of member organizations and their peer nodes. Amazon Managed Blockchain (AMB) provides access to public blockchain networks (Ethereum and Bitcoin) and lets you create private, permissioned blockchain networks with the Hyperledger Fabric framework. AMB Access offers fully managed, dedicated (single-tenant), and serverless multi-tenant API operations for public nodes, and fully managed private networks for use cases requiring access controls.

Key points:

- AMB Access: standardized API access to blockchain infrastructure.
- Network: the private blockchain network (Fabric) or public network membership.
- Member: an organization in a Fabric network; members run peer nodes and can propose changes (chaincode, membership) with voting.
- Peer node: the Fabric component that hosts the ledger and chaincode; deploy multiple peers for high availability.
- Accessor and tokens: token-based access to Ethereum nodes (accessors are containers with token-based access information).

Practices:

- Choose the deployment model by requirement: public API access (AMB Access), dedicated nodes, or a private Fabric network for permissioned use cases.
- Run multiple peer nodes across Availability Zones for high availability in Fabric networks.
- Manage membership carefully: proposals and votes control who can join and change the network.

| Symptom | Check |
| --- | --- |
| Node unavailable | Check network/member status, node health, and IAM permissions. |
| Token access denied | Verify the accessor exists and the token is valid for the network. |
| Chaincode proposal fails | Confirm voting policy thresholds and member permissions. |
| Fabric network creation fails | Validate the member configuration (admin user, password policy, instance type). |

Networks, members, nodes, and accessors per account have quotas; framework versions are fixed at network creation. See the Amazon Managed Blockchain endpoints and quotas page and Service Quotas console for current values.[^aws-managed-blockchain]


## Related

- [Data stores](data-stores.md)
- [Domain index](index.md)

[^aws-documentdb]: [Amazon DocumentDB - Runbook & Reference](../../sources/aws-documentdb.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/documentdb/README.md)
[^aws-neptune]: [Amazon Neptune - Runbook & Reference](../../sources/aws-neptune.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/neptune/README.md)
[^aws-qldb]: [Amazon QLDB - Runbook & Reference](../../sources/aws-qldb.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/qldb/README.md)
[^aws-managed-blockchain]: [Amazon Managed Blockchain (AMB) - Runbook & Reference](../../sources/aws-managed-blockchain.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/managed-blockchain/README.md)
