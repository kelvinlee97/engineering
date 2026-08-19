# AWS DataSync - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS DataSync is a secure, reliable, high-speed data transfer service for moving file and object data to, from, and between AWS storage services. It works with on-premises storage (via an agent), AWS storage (S3, EFS, FSx), and other cloud storage, with encryption and data integrity validation built in.

## Key concepts

- **Task**: a job that transfers data between a source location and a destination location with defined options (overwrite, preserve metadata, schedule).
- **Location**: the source or destination endpoint (NFS, SMB, S3, EFS, FSx).
- **Agent**: a software appliance (Amazon EC2 or on-premises VM) that connects DataSync to on-premises storage.
- **Scheduling and monitoring**: tasks run on demand or on a schedule; monitor with CloudWatch metrics, events, and the console.
- **Acceleration**: a purpose-built network protocol with parallel, multi-threaded architecture for fast transfers.
- **Security**: transfers are encrypted end to end; DataSync uses IAM roles and supports VPC endpoints (private transfer without the public internet).
- **Use cases**: migrate active datasets, archive cold data to Glacier, replicate to S3/EFS/FSx, and move data into AWS for processing.

## Common operations (AWS CLI)

```bash
# Create locations and a task
aws datasync create-location-s3 --s3-bucket-arn arn:aws:s3:::my-bucket \
  --s3-config '{"BucketAccessRoleArn":"arn:aws:iam::123456789012:role/datasync-role"}' \
  --region us-east-1
aws datasync create-location-nfs --server-hostname 10.0.0.10 \
  --on-prem-config '{"AgentArns":["arn:aws:datasync:us-east-1:123456789012:agent/agent-0123456789abcdef0"]}' \
  --subdirectory /data
aws datasync create-task --source-location-arn <source-arn> \
  --destination-location-arn <dest-arn> --name migrate-data

# Start and monitor
aws datasync start-task-execution --task-arn <task-arn>
aws datasync describe-task-execution --task-execution-arn <exec-arn>
aws datasync list-tasks
aws datasync delete-task --task-arn <task-arn>
```

## Best practices

- Run a discovery/validation transfer on a subset before the full migration; use the dry-run option where available.
- Schedule recurring tasks for replication and set CloudWatch alarms on transfer errors and failures.
- Place the agent close to the data source and size it appropriately; use multiple tasks/agents for very large datasets.
- Use VPC endpoints for AWS-to-AWS or hybrid transfers that should not traverse the public internet.
- Preserve metadata and permissions where required; choose the right S3 storage class (for example, Glacier for cold archives).
- Monitor task execution metrics and verify integrity after transfer.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Agent offline | Verify the agent VM is running, has network access, and is activated in the same Region. |
| Task fails | Check source/destination connectivity, IAM roles, and the CloudWatch logs/error messages for the task. |
| Slow transfer | Review agent sizing, network bandwidth, small-file overhead, and task scheduling conflicts. |
| Permissions preserved incorrectly | Adjust the task's POSIX/SMB metadata options. |
| Files missing | Confirm the task filters, verification mode, and that the source was accessible during the run. |

## Limits

Agents, locations, tasks, and concurrent task executions per account have quotas. See the AWS DataSync endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS DataSync?](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [AWS DataSync endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/datasync.html)
- [AWS DataSync pricing](https://aws.amazon.com/datasync/pricing/)
- [AWS CLI: datasync commands](https://docs.aws.amazon.com/cli/latest/reference/datasync/)
