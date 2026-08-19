# AWS Batch - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Batch is a fully managed batch computing service. It provisions compute resources on your behalf, optimizes workload distribution, and runs containerized batch jobs on Amazon ECS, Amazon EKS, EC2, and AWS Fargate. It also provides queuing for SageMaker Training jobs.

## Key concepts

- **Compute environment**: the pool of compute (EC2 On-Demand/Spot, Fargate, or EKS) where jobs run.
- **Job queue**: ordered submission queue mapped to one or more compute environments with priorities.
- **Job definition**: the container image, resources (vCPU/memory), IAM role, and parameters for a job.
- **Job**: a single unit of work submitted to a queue; can be a single container or an array of jobs.
- **Array jobs**: run many copies of the same job with different index values.
- **Multi-node parallel jobs**: coordinate multiple containers across instances for MPI-style workloads.
- **Scheduling policies**: fair-share scheduling across queues and job priorities.
- **SageMaker queuing**: submit ML training jobs with priorities to configurable queues.

## Common operations (AWS CLI)

```bash
# Create a Fargate compute environment and job queue
aws batch create-compute-environment --compute-environment-name fargate-env \
  --type MANAGED --compute-resources '{
    "Type": "FARGATE",
    "Subnets": ["subnet-1","subnet-2"],
    "SecurityGroupIds": ["sg-12345"],
    "AssignPublicIp": "DISABLED"
  }'
aws batch create-job-queue --job-queue-name main --state ENABLED \
  --priority 1 --compute-environment-order '{"Order":1,"ComputeEnvironment":"fargate-env"}'

# Register a job definition
aws batch register-job-definition --job-definition-name etl \
  --type container --container-properties '{
    "Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/etl:latest",
    "ResourceRequirements": [{"Type":"VCPU","Value":"2"},{"Type":"MEMORY","Value":"4096"}],
    "ExecutionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"
  }'

# Submit and monitor jobs
aws batch submit-job --job-name etl-2026-08-19 --job-queue main \
  --job-definition etl --parameters '{"date":"2026-08-19"}'
aws batch describe-jobs --jobs <job-id>
aws batch list-jobs --job-queue main --job-status RUNNABLE

# Cancel/terminate
aws batch cancel-job --job-id <job-id> --reason "schedule change"
aws batch terminate-job --job-id <job-id> --reason "maintenance"
```

## Best practices

- Use Fargate for simple container jobs and EC2 (with Spot) for large or GPU workloads.
- Separate job queues per priority/team and use scheduling policies to enforce fairness.
- Make jobs idempotent and fault-tolerant; retry logic belongs in the application.
- Store job scripts/config in S3 and container images in ECR; version both.
- Monitor queue depth, job status, and compute environment utilization; set alarms.
- Clean up compute environments when idle; use Spot with a diversified allocation strategy to save cost.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Job stuck in RUNNABLE | Check queue/compute environment capacity, subnet/IP availability, and job definitions. |
| Container fails | Inspect CloudWatch logs and exit codes; test the image locally. |
| Compute environment insufficient | Increase max vCPU or add Spot capacity; check service quotas. |
| IAM errors | Verify the job role and execution role permissions. |
| Array job partial failure | Check per-index exit codes and design retries accordingly. |

## Limits

Compute environments, job queues, jobs in flight, and max vCPU per account have quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html)
- [AWS Batch service quotas](https://docs.aws.amazon.com/batch/latest/userguide/service_limits.html)
- [AWS Batch pricing](https://aws.amazon.com/batch/pricing/)
- [AWS CLI: batch commands](https://docs.aws.amazon.com/cli/latest/reference/batch/)
