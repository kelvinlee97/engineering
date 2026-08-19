# Amazon FSx - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon FSx is a family of fully managed file storage services for workloads that need shared file systems. It provides native Windows file servers, a high-performance parallel file system, and POSIX file systems with NetApp and OpenZFS compatibility.

## File system types

| Type | Protocol | Best for |
|---|---|---|
| FSx for Windows File Server | SMB 2.0-3.1.1 | Lift-and-shift Windows workloads, home directories, business apps |
| FSx for Lustre | POSIX (Lustre) | High-performance computing, ML training, media processing |
| FSx for NetApp ONTAP | NFS, SMB, iSCSI | Enterprise NAS features: snapshots, clones, data tiering |
| FSx for OpenZFS | NFS (POSIX) | Linux workloads needing ZFS features: snapshots, clones, compression |

## Key concepts

- **File system**: the primary resource; you choose storage capacity, throughput, and (for Windows) SSD IOPS independently.
- **File shares**: SMB shares (Windows) or NFS exports (Lustre/ONTAP/OpenZFS) exposed to compute clients.
- **Single-AZ / Multi-AZ**: Windows file systems support high availability within one AZ or across two AZs with automatic failover.
- **Active Directory integration**: Windows file systems join a Microsoft AD for user authentication and ACL-based access.
- **Backups**: file-system-consistent, incremental backups; automatic daily backups plus manual backups.
- **Data tiering**: ONTAP can tier cold data to Amazon S3 to control costs.

## Common operations (AWS CLI)

```bash
# Create a file system (Windows example)
aws fsx create-file-system --file-system-type WINDOWS \
  --storage-capacity 300 --storage-type SSD \
  --subnet-ids subnet-0123456789abcdef0 \
  --windows-configuration ThroughputCapacity=32,DeploymentType=MULTI_AZ_1,PreferredSubnetId=subnet-0123456789abcdef0

# List and describe file systems
aws fsx describe-file-systems
aws fsx describe-file-systems --file-system-ids fs-0123456789abcdef0

# Create a backup
aws fsx create-backup --file-system-id fs-0123456789abcdef0

# Update capacity
aws fsx update-file-system --file-system-id fs-0123456789abcdef0 \
  --storage-capacity 600

# Delete (after taking a final backup)
aws fsx delete-file-system --file-system-id fs-0123456789abcdef0
```

## Best practices

- Choose the FSx type by protocol and workload, not by habit: Windows/SMB vs. Lustre/HPC vs. ONTAP/OpenZFS for NAS features.
- Use Multi-AZ Windows file systems for production; use Single-AZ where cost matters and downtime is acceptable.
- Enable automatic daily backups and keep manual backups before destructive changes.
- Place file systems in private subnets and control access with VPC security groups.
- Join Windows file systems to Managed Microsoft AD and use Windows ACLs for file-level permissions.
- Monitor with CloudWatch and enable CloudTrail for API auditing.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Clients can't mount | Verify security group rules (SMB 445, NFS 2049) and that the client is in a peered/transit-gateway-connected VPC. |
| Windows authentication fails | Confirm the file system is joined to AD, DNS resolves the file system name, and the user has an AD account. |
| Poor performance | Check throughput/storage/IOPS settings and workload type; scale capacity as needed. |
| Backup failed | Check available storage and file system state; retry a manual backup. |
| Multi-AZ failover issues | Verify preferred subnet and standby subnet are in different AZs with correct routing. |

## Limits

Per-account quotas for file systems, total storage, and throughput depend on file system type and Region. See the Service Quotas console for current values.

## Official references

- [What is FSx for Windows File Server?](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html)
- [Amazon FSx for Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html)
- [Amazon FSx for NetApp ONTAP](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is.html)
- [Amazon FSx for OpenZFS](https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is.html)
- [AWS CLI: fsx commands](https://docs.aws.amazon.com/cli/latest/reference/fsx/)
