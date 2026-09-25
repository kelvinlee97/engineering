---
type: Service
title: AWS storage and migration
description: Backup, file systems, hybrid storage, data transfer, and server and database migration services on AWS.
tags: [aws, storage, migration]
sources:
  - id: aws-backup
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/backup/README.md
    title: "AWS Backup - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-fsx
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/fsx/README.md
    title: "Amazon FSx - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-storage-gateway
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/storage-gateway/README.md
    title: "AWS Storage Gateway - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-datasync
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/datasync/README.md
    title: "AWS DataSync - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-snow-family
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/snow-family/README.md
    title: "AWS Snow Family - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-transfer-family
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/transfer-family/README.md
    title: "AWS Transfer Family - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-mgn
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/mgn/README.md
    title: "AWS Application Migration Service (MGN) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-dms
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/dms/README.md
    title: "AWS Database Migration Service (DMS) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services protect data, provide file storage, and move data and servers into AWS, online or on physical devices.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS Backup](#aws-backup) | AWS Backup separates "when and how long" from "where" |
| [Amazon FSx](#amazon-fsx) | Amazon FSx is a family of fully managed file storage services for workloads that need shared file systems |
| [AWS Storage Gateway](#aws-storage-gateway) | AWS Storage Gateway connects an on-premises software appliance (or the Storage Gateway hardware appliance) to cloud storage, giving your on-premises environment access to AWS-backed file, volume, and tape storage |
| [AWS DataSync](#aws-datasync) | AWS DataSync is a secure, reliable, high-speed data transfer service for moving file and object data to, from, and between AWS storage services |
| [AWS Snow Family](#aws-snow-family) | The AWS Snow Family provides physical devices for offline data transfer and edge computing in environments without reliable connectivity |
| [AWS Transfer Family](#aws-transfer-family) | AWS Transfer Family is a fully managed service for transferring files into and out of AWS storage (Amazon S3 and Amazon EFS) over SFTP, FTPS, FTP, AS2, and browser-based web transfers |
| [AWS Application Migration Service (MGN)](#aws-application-migration-service-mgn) | MGN keeps a source server continuously replicating into AWS in the background, so cutover is just a short switch from an already-warm target rather than a from-scratch migration |
| [AWS Database Migration Service (DMS)](#aws-database-migration-service-dms) | AWS Database Migration Service (AWS DMS) migrates relational databases, data warehouses, NoSQL databases, and other data stores into AWS or between combinations of cloud and on-premises environments |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS Backup

AWS Backup separates "when and how long" from "where": a plan's rules decide backup frequency and retention, the vault (and its optional Vault Lock) decides how immutable the result is, and copy rules decide whether it also lands in another Region or account. AWS Backup is a fully managed backup service that centralizes backup policies, monitoring, and compliance across supported AWS services. You define backup plans once and apply them to resources; AWS Backup automates backup scheduling, retention, lifecycle transitions, and cross-Region/cross-account copies.

Key points:

- Backup plan: rules that define when to run backups, how long to keep them, and which vault receives them; a plan can include multiple rules.
- Backup vault: a container that stores backups and controls access with vault policies; vaults are per-Region resources.
- Vault Lock: enforces immutable (WORM) backup protection with governance or compliance modes, preventing backup deletion even by administrators.
- Lifecycle: transition backups from warm storage to cold storage after a specified period, and expire them at the retention end.
- Cross-Region and cross-account backup: copy backups to another Region or account for disaster recovery and isolation.

Practices:

- Centralize plans by workload class (for example, database, application, file) and apply them with tag-based or resource-based selections.
- Use Vault Lock in compliance mode for regulated data and test governance mode before enforcing.
- Configure cross-Region copy for critical data and cross-account copy for isolation from the production account.

| Symptom | Check |
| --- | --- |
| Backup job failed | Check the job status message, resource permissions, and that the resource is in a supported state. |
| Restore slow | Cold storage retrievals take longer; use warm copies for time-critical restores. |
| Vault Lock cannot be removed | Compliance mode is permanent by design; create a new vault if you need different protection. |
| Cross-account copy missing | Verify the destination account vault policy grants backup access and the copy role is configured. |

Backup plans, vaults, and jobs per account per Region, plus restore and copy quotas, apply. Cold storage has minimum retention periods. See the AWS Backup endpoints and quotas page and Service Quotas console for current values.[^aws-backup]


## Amazon FSx

Amazon FSx is a family of fully managed file storage services for workloads that need shared file systems. It provides native Windows file servers, a high-performance parallel file system, and POSIX file systems with NetApp and OpenZFS compatibility.

Key points:

- File system: the primary resource; you choose storage capacity, throughput, and (for Windows) SSD IOPS independently.
- File shares: SMB shares (Windows) or NFS exports (Lustre/ONTAP/OpenZFS) exposed to compute clients.
- Single-AZ / Multi-AZ: Windows file systems support high availability within one AZ or across two AZs with automatic failover.
- Active Directory integration: Windows file systems join a Microsoft AD for user authentication and ACL-based access.
- Backups: file-system-consistent, incremental backups; automatic daily backups plus manual backups.

Practices:

- Choose the FSx type by protocol and workload, not by habit: Windows/SMB vs. Lustre/HPC vs. ONTAP/OpenZFS for NAS features.
- Use Multi-AZ Windows file systems for production; use Single-AZ where cost matters and downtime is acceptable.
- Enable automatic daily backups and keep manual backups before destructive changes.

| Symptom | Check |
| --- | --- |
| Clients can't mount | Verify security group rules (SMB 445, NFS 2049) and that the client is in a peered/transit-gateway-connected VPC. |
| Windows authentication fails | Confirm the file system is joined to AD, DNS resolves the file system name, and the user has an AD account. |
| Poor performance | Check throughput/storage/IOPS settings and workload type; scale capacity as needed. |
| Backup failed | Check available storage and file system state; retry a manual backup. |

Per-account quotas for file systems, total storage, and throughput depend on file system type and Region. See the Service Quotas console for current values.[^aws-fsx]


## AWS Storage Gateway

AWS Storage Gateway connects an on-premises software appliance (or the Storage Gateway hardware appliance) to cloud storage, giving your on-premises environment access to AWS-backed file, volume, and tape storage. It is the bridge for hybrid storage architectures.

Key points:

- Gateway: the VM or hardware appliance deployed in your data center and activated to your AWS account.
- File share: an SMB/NFS export backed by an S3 bucket or FSx file system, with a local cache for frequently accessed data.
- Cached vs. stored volumes: cached volumes keep primary data in S3 with hot data on-premises; stored volumes keep primary data locally and back up as EBS snapshots.
- Virtual tape library (VTL): tape drives and libraries presented over iSCSI; tapes are stored in S3 and can be archived to Glacier.
- AWS OpsHub: the desktop application for deploying, activating, and monitoring gateways.

Practices:

- Deploy gateways close to the workloads they serve and size the local cache/disk for your working set.
- Use S3 File Gateway for on-premises file access to S3; use Volume Gateway for block workloads that need iSCSI.
- Enable bandwidth throttling on the gateway to protect your WAN link.

| Symptom | Check |
| --- | --- |
| File share mount fails | Verify the share is available, DNS/SMB settings, and that clients use the correct share path. |
| Slow uploads | Check bandwidth throttling settings, local cache size, and network connectivity. |
| Cache fills up | Increase cache disk size or reduce the share's working set. |
| Tape not showing in VTL | Verify iSCSI initiator settings and that the tape library/drive were configured on the gateway. |

Gateway counts, cache sizes, file share counts, and tape counts have per-account quotas. See the Service Quotas console for current values.[^aws-storage-gateway]


## AWS DataSync

AWS DataSync is a secure, reliable, high-speed data transfer service for moving file and object data to, from, and between AWS storage services. It works with on-premises storage (via an agent), AWS storage (S3, EFS, FSx), and other cloud storage, with encryption and data integrity validation built in.

Key points:

- Task: a job that transfers data between a source location and a destination location with defined options (overwrite, preserve metadata, schedule).
- Location: the source or destination endpoint (NFS, SMB, S3, EFS, FSx).
- Agent: a software appliance (Amazon EC2 or on-premises VM) that connects DataSync to on-premises storage.
- Scheduling and monitoring: tasks run on demand or on a schedule; monitor with CloudWatch metrics, events, and the console.
- Acceleration: a purpose-built network protocol with parallel, multi-threaded architecture for fast transfers.

Practices:

- Run a discovery/validation transfer on a subset before the full migration; use the dry-run option where available.
- Schedule recurring tasks for replication and set CloudWatch alarms on transfer errors and failures.
- Place the agent close to the data source and size it appropriately; use multiple tasks/agents for very large datasets.

| Symptom | Check |
| --- | --- |
| Agent offline | Verify the agent VM is running, has network access, and is activated in the same Region. |
| Task fails | Check source/destination connectivity, IAM roles, and the CloudWatch logs/error messages for the task. |
| Slow transfer | Review agent sizing, network bandwidth, small-file overhead, and task scheduling conflicts. |
| Permissions preserved incorrectly | Adjust the task's POSIX/SMB metadata options. |

Agents, locations, tasks, and concurrent task executions per account have quotas. See the AWS DataSync endpoints and quotas page and Service Quotas console for current values.[^aws-datasync]


## AWS Snow Family

The AWS Snow Family provides physical devices for offline data transfer and edge computing in environments without reliable connectivity. Note the current lifecycle: Snowcone (HDD/SSD) was discontinued on November 12, 2024, and AWS Snowball Edge is no longer available to new customers. For new online data transfers, use AWS DataSync; for offline transfer options, review the current Snowball Edge documentation.

Key points:

- Job: an import/export job for moving data between your site and Amazon S3; create and manage jobs in the console or with the Snowball API.
- Device configuration: Storage Optimized (210 TB, up to 40 vCPUs) vs. Compute Optimized (up to 104 vCPUs with GPU options).
- Endpoints: Snowball Edge exposes S3- and EC2-compatible endpoints plus NFS, for local workloads.
- Clusters: group 3-16 devices for local storage and compute with higher durability.
- OpsHub / Snowball Edge client: tools for unlocking the device, configuring the network, and transferring data.

Practices:

- For ongoing or online migrations, use AWS DataSync instead of physical devices where possible.
- Estimate data volume and transfer time before ordering; choose the right device size to minimize shipping legs.
- Set up the S3 bucket, IAM role, and shipping address before creating the job.

| Symptom | Check |
| --- | --- |
| Device won't unlock | Verify the job state and use the correct manifest/unlock code from the console. |
| Slow local transfer | Check the local network between clients and device (10/25/40/100 GbE), and use the S3 adapter or NFS as appropriate. |
| Data not appearing in S3 | Confirm the job completed and was processed by AWS after the device was returned. |
| Job cancelled after shipping | Contact AWS Support; shipped jobs generally cannot be cancelled. |

Job counts per account, device counts in flight, and cluster sizes (3-16 devices) are constrained by AWS quotas and regional availability. Check the Service Quotas console and Snowball Edge documentation for current values.[^aws-snow-family]


## AWS Transfer Family

AWS Transfer Family is a fully managed service for transferring files into and out of AWS storage (Amazon S3 and Amazon EFS) over SFTP, FTPS, FTP, AS2, and browser-based web transfers. You keep your existing clients, authentication, and firewall configurations; AWS manages the servers and scales them automatically. You pay only for what you use.

Key points:

- Server: a managed endpoint (public or VPC) that accepts one or more protocols (SFTP v3, FTPS, FTP, AS2); associate your hostname and DNS with the endpoint.
- Storage: data lives in Amazon S3 (data lakes, third-party uploads, distribution) or Amazon EFS (content management, supply chain, web serving).
- Identity providers: service-managed users, AWS Directory Service, or custom identity providers (Lambda-backed, API Gateway) for user authentication.
- Web apps: managed browser-based transfer interface for S3 with centralized access management.
- Managed workflows (MFTW): serverless, automated processing of uploaded files (copy, tag, scan, filter, compress/decompress, encrypt/decrypt) with end-to-end visibility.

Practices:

- Use VPC endpoints for private transfer and restrict security groups to the ports/protocols in use.
- Enforce strong authentication: service-managed with strong passwords, MFA where supported, or integrate with Directory Service/custom IdPs.
- Scope IAM roles for users with a home directory and least-privilege S3/EFS access; use logical directories for isolation.

| Symptom | Check |
| --- | --- |
| Client cannot connect | Check endpoint type (public/VPC), security groups, DNS, and protocol configuration. |
| Login denied | Verify the identity provider configuration, user name/password, and IAM role for the user. |
| Uploads fail | Check the user's home directory, S3/EFS permissions, and the server's role. |
| FTP/FTPS data connection fails | Ensure the 8192-8200 port range is open for data connections. |

Servers, users, managed workflows, and API request rates per account have quotas; FTP/FTPS data connections use a fixed port range. See the AWS Transfer Family endpoints and quotas page and Service Quotas console for current values.[^aws-transfer-family]


## AWS Application Migration Service (MGN)

MGN keeps a source server continuously replicating into AWS in the background, so cutover is just a short switch from an already-warm target rather than a from-scratch migration. AWS Application Migration Service (MGN, now documented as AWS Transform MGN) automates the migration of physical, virtual, and cloud servers to AWS with minimal downtime, typically cutover windows of minutes. MGN performs continuous block-level replication of source servers, converts them for launch on AWS, and supports large-scale migrations through templates, applications, and waves.

Key points:

- Source server: the on-premises, virtual, or cloud server being migrated; install the MGN agent to start replication.
- Replication: continuous block-level replication to a staging area in your AWS account; the target is prepared for launch without stopping the source.
- Templates: replication, launch, and post-launch templates control how servers are replicated, launched, and configured after migration; settings can be overridden per server.
- Applications and waves: group servers into applications and applications into waves to run actions (launch, cutover, archive) in bulk.
- Cutover: the controlled switch that stops replication and launches the migrated instances (usually in minutes); test launches (blue/green) validate before cutover.

Practices:

- Test migrations on a representative sample of servers before mass cutover; use test launches to validate boot, networking, and applications.
- Plan waves by dependency and business priority; avoid cutting over dependent servers out of order.
- Use launch templates for consistent instance sizing and post-launch templates for agents/config after boot.

| Symptom | Check |
| --- | --- |
| Replication lag | Check source network bandwidth, disk I/O, and the agent status on the source server. |
| Test launch fails | Review launch template settings, AMI/target subnet, and post-launch scripts. |
| Agent not installed | Install the MGN agent on the source and confirm connectivity to AWS endpoints. |
| Cutover fails | Verify the staging area, replication health, and that the source was not archived. |

Source servers per account, concurrent launches, and API request rates have quotas. See the AWS Application Migration Service endpoints and quotas page and Service Quotas console for current values.[^aws-mgn]


## AWS Database Migration Service (DMS)

AWS Database Migration Service (AWS DMS) migrates relational databases, data warehouses, NoSQL databases, and other data stores into AWS or between combinations of cloud and on-premises environments. It supports one-time migrations and ongoing replication to keep sources and targets in sync, plus Fleet Advisor (discovery) and Schema Conversion (engine conversion).

Key points:

- Replication instance: the compute resource that runs the migration tasks.
- Endpoints: source and target connection definitions (engine, host, credentials, VPC).
- Replication task: a scheduled unit of work (full load, ongoing replication/CDC, or both).
- Schema conversion: DMS Schema Conversion or the downloadable AWS Schema Conversion Tool (AWS SCT) converts schemas/code to the target engine.
- Fleet Advisor: discovers and inventories on-premises database servers to plan migrations.

Practices:

- Use Fleet Advisor and Schema Conversion early to size the migration and convert schemas before cutover.
- Run a full-load test on a representative dataset; validate data with DMS data validation.
- Keep the replication instance in a private subnet with proper security groups for both endpoints.

| Symptom | Check |
| --- | --- |
| Task stuck in failed state | Check task logs and endpoint connectivity; verify credentials and network routes. |
| CDC lag growing | Check source retention (for example, Oracle archive logs) and replication instance capacity. |
| Data mismatch | Run data validation, review transformation rules in table mappings. |
| Cannot connect to source | Verify security group/NACL rules, endpoint settings, and source-side firewall. |

Replication instances, endpoints, tasks, and concurrent connections have per-account quotas. See the Service Quotas console for current values.[^aws-dms]


## Related

- [Data stores](data-stores.md)
- [Networking](networking.md): Direct Connect for large ongoing transfers.
- [Domain index](index.md)

[^aws-backup]: [AWS Backup - Runbook & Reference](../../sources/aws-backup.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/backup/README.md)
[^aws-fsx]: [Amazon FSx - Runbook & Reference](../../sources/aws-fsx.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/fsx/README.md)
[^aws-storage-gateway]: [AWS Storage Gateway - Runbook & Reference](../../sources/aws-storage-gateway.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/storage-gateway/README.md)
[^aws-datasync]: [AWS DataSync - Runbook & Reference](../../sources/aws-datasync.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/datasync/README.md)
[^aws-snow-family]: [AWS Snow Family - Runbook & Reference](../../sources/aws-snow-family.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/snow-family/README.md)
[^aws-transfer-family]: [AWS Transfer Family - Runbook & Reference](../../sources/aws-transfer-family.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/transfer-family/README.md)
[^aws-mgn]: [AWS Application Migration Service (MGN) - Runbook & Reference](../../sources/aws-mgn.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/mgn/README.md)
[^aws-dms]: [AWS Database Migration Service (DMS) - Runbook & Reference](../../sources/aws-dms.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/dms/README.md)
