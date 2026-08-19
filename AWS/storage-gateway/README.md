# AWS Storage Gateway - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Storage Gateway connects an on-premises software appliance (or the Storage Gateway hardware appliance) to cloud storage, giving your on-premises environment access to AWS-backed file, volume, and tape storage. It is the bridge for hybrid storage architectures.

## Gateway types

| Gateway | Interface | What it exposes |
|---|---|---|
| S3 File Gateway | SMB / NFS | S3 objects as file shares, with local cache |
| FSx File Gateway | SMB | Amazon FSx for Windows File Server shares with local cache |
| Volume Gateway | iSCSI | Block volumes backed by EBS snapshots (cached or stored) |
| Tape Gateway | iSCSI VTL | Virtual tapes stored in S3 and archived to Amazon S3 Glacier |

## Key concepts

- **Gateway**: the VM or hardware appliance deployed in your data center and activated to your AWS account.
- **File share**: an SMB/NFS export backed by an S3 bucket or FSx file system, with a local cache for frequently accessed data.
- **Cached vs. stored volumes**: cached volumes keep primary data in S3 with hot data on-premises; stored volumes keep primary data locally and back up as EBS snapshots.
- **Virtual tape library (VTL)**: tape drives and libraries presented over iSCSI; tapes are stored in S3 and can be archived to Glacier.
- **AWS OpsHub**: the desktop application for deploying, activating, and monitoring gateways.

## Common operations (AWS CLI)

```bash
# Create and activate a gateway (returns a GatewayARN)
aws storagegateway create-gateway --gateway-name site-a-file --gateway-timezone GMT \
  --gateway-type FILE_FSX_SMB --gateway-platform "VMWARE" \
  --gateway-capacity Medium

# List gateways
aws storagegateway list-gateways

# Create an S3 file share
aws storagegateway create-smb-file-share --gateway-arn <gateway-arn> \
  --role arn:aws:iam::123456789012:role/StorageGatewayRole \
  --location-arn arn:aws:s3:::bucket-name

# Create a tape
aws storagegateway create-tapes --gateway-arn <gateway-arn> \
  --tape-size-in-bytes 1099511627776 --num-tapes-to-create 1 \
  --client-token tape-001

# List and inspect resources
aws storagegateway list-file-shares
aws storagegateway list-volumes
aws storagegateway list-tapes
```

## Best practices

- Deploy gateways close to the workloads they serve and size the local cache/disk for your working set.
- Use S3 File Gateway for on-premises file access to S3; use Volume Gateway for block workloads that need iSCSI.
- Enable bandwidth throttling on the gateway to protect your WAN link.
- Protect the gateway VM with backups and use the hardware appliance where VM hosting is not feasible.
- Monitor gateway metrics (cache hit rate, upload throughput) in CloudWatch and set alarms.
- Apply least-privilege IAM roles: file shares need only the S3/FSx permissions they use.
- Use AWS Backup to manage snapshots and tape lifecycle centrally.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| File share mount fails | Verify the share is available, DNS/SMB settings, and that clients use the correct share path. |
| Slow uploads | Check bandwidth throttling settings, local cache size, and network connectivity. |
| Cache fills up | Increase cache disk size or reduce the share's working set. |
| Tape not showing in VTL | Verify iSCSI initiator settings and that the tape library/drive were configured on the gateway. |
| Gateway offline | Check gateway health in OpsHub, VM resources, and network access to AWS endpoints. |

## Limits

Gateway counts, cache sizes, file share counts, and tape counts have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Storage Gateway?](https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html)
- [Amazon S3 File Gateway user guide](https://docs.aws.amazon.com/storagegateway/latest/s3fgw/WhatIsS3FileGateway.html)
- [AWS Storage Gateway pricing](https://aws.amazon.com/storagegateway/pricing/)
- [AWS CLI: storagegateway commands](https://docs.aws.amazon.com/cli/latest/reference/storagegateway/)
