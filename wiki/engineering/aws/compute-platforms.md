---
type: Service
title: AWS compute platforms
description: Batch jobs, simple virtual servers, managed web platforms, on-premises AWS hardware, and scaling for non-EC2 resources.
tags: [aws, compute]
sources:
  - id: aws-batch
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/batch/README.md
    title: "AWS Batch - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-lightsail
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/lightsail/README.md
    title: "Amazon Lightsail - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-elastic-beanstalk
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/elastic-beanstalk/README.md
    title: "AWS Elastic Beanstalk - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-outposts
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/outposts/README.md
    title: "AWS Outposts - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-application-auto-scaling
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/application-auto-scaling/README.md
    title: "Application Auto Scaling - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
Beyond raw [EC2](compute.md), these services package compute for particular jobs: queued batch work, simple fixed-price servers, managed application platforms, AWS hardware in your own data center, and scaling for resources other than EC2.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS Batch](#aws-batch) | AWS Batch is a queue in front of elastic compute |
| [Amazon Lightsail](#amazon-lightsail) | Amazon Lightsail is the simplest way to launch and manage virtual private servers and web applications on AWS, with low, predictable monthly pricing |
| [AWS Elastic Beanstalk](#aws-elastic-beanstalk) | AWS Elastic Beanstalk is a managed service that deploys and scales web applications and worker processes on familiar AWS resources such as EC2, S3, and load balancers |
| [AWS Outposts](#aws-outposts) | An Outpost is a physical extension of an AWS Region into your building |
| [Application Auto Scaling](#application-auto-scaling) | Application Auto Scaling is one control loop applied uniformly to many non-EC2 resource types |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS Batch

AWS Batch is a queue in front of elastic compute: a job waits in a priority-ordered queue until its compute environment has room, then runs as a container (or an array/multi-node group of containers): you describe the work and its resource needs, Batch handles provisioning. AWS Batch is a fully managed batch computing service. It provisions compute resources on your behalf, optimizes workload distribution, and runs containerized batch jobs on Amazon ECS, Amazon EKS, EC2, and AWS Fargate. It also provides queuing for SageMaker Training jobs.

Key points:

- Compute environment: the pool of compute (EC2 On-Demand/Spot, Fargate, or EKS) where jobs run.
- Job queue: ordered submission queue mapped to one or more compute environments with priorities.
- Job definition: the container image, resources (vCPU/memory), IAM role, and parameters for a job.
- Job: a single unit of work submitted to a queue; can be a single container or an array of jobs.
- Array jobs: run many copies of the same job with different index values.

Practices:

- Use Fargate for simple container jobs and EC2 (with Spot) for large or GPU workloads.
- Separate job queues per priority/team and use scheduling policies to enforce fairness.
- Make jobs idempotent and fault-tolerant; retry logic belongs in the application.

| Symptom | Check |
| --- | --- |
| Job stuck in RUNNABLE | Check queue/compute environment capacity, subnet/IP availability, and job definitions. |
| Container fails | Inspect CloudWatch logs and exit codes; test the image locally. |
| Compute environment insufficient | Increase max vCPU or add Spot capacity; check service quotas. |
| IAM errors | Verify the job role and execution role permissions. |

Compute environments, job queues, jobs in flight, and max vCPU per account have quotas. See the Service Quotas console for current values.[^aws-batch]


## Amazon Lightsail

Amazon Lightsail is the simplest way to launch and manage virtual private servers and web applications on AWS, with low, predictable monthly pricing. It bundles instances, containers, managed databases (MySQL/PostgreSQL), load balancers, CDN distributions, block/object storage, static IPs, DNS, and snapshots in one console.

Key points:

- Instance: a virtual private server with a click-to-launch blueprint (OS, WordPress, LAMP, Nginx, etc.) and a built-in firewall.
- Blueprints and bundles: preconfigured OS/app images and fixed instance sizes (RAM, vCPU, storage, transfer).
- Managed database: fully configured MySQL or PostgreSQL that scales independently of instances.
- Container service: run containerized apps with a load balancer and HTTPS.
- Load balancer: distributes traffic across instances with health checks and session persistence.

Practices:

- Use Lightsail for simple, predictable workloads; move to EC2/RDS when you need advanced features or deep AWS integration.
- Enable the built-in firewall and only open required ports; use snapshots before changes.
- Use managed databases instead of running MySQL/PostgreSQL on instances.

| Symptom | Check |
| --- | --- |
| Instance unreachable | Check instance state, firewall rules, and static IP attachment. |
| Slow site | Review bundle size, add a load balancer, or use the CDN distribution. |
| Database connection fails | Check database endpoint, credentials, and public/private access settings. |
| Snapshot restore issues | Create a new instance from the snapshot and verify data/configuration. |

Instances, databases, load balancers, static IPs, and transfer allowances are capped per account and plan. See the Lightsail pricing page and Service Quotas console for current values.[^aws-lightsail]


## AWS Elastic Beanstalk

AWS Elastic Beanstalk is a managed service that deploys and scales web applications and worker processes on familiar AWS resources such as EC2, S3, and load balancers. You upload code and Elastic Beanstalk handles capacity provisioning, load balancing, scaling, health monitoring, and updates, while you keep control of the underlying resources.

Key points:

- Application: the logical container for versions and environments.
- Environment: a running deployment of an application version.
- Platform: the runtime stack, including Go, Java (Corretto, Tomcat), .NET (Linux), Node.js, PHP, Python, Ruby, and Docker (single-container and multi-container); the platform maintains your chosen runtime version.
- Configuration: environment settings for instances, scaling, load balancing, updates, and health; saved configurations can be reused.
- Deployment policies: all-at-once, rolling, rolling with additional batch, immutable, traffic splitting (canary), and blue/green via environment CNAME swap.

Practices:

- Use environments for separate stages (dev, staging, prod) and keep application versions immutable.
- Set environment variables in configuration rather than hard-coding them; use Secrets Manager for sensitive values.
- Configure scaling policies and alarms for the load you expect; verify health checks before routing traffic.

| Symptom | Check |
| --- | --- |
| Environment `Degraded`/`Severe` | Open the environment health page and inspect instance-level causes and recent events. |
| Deployment fails | Review build/application logs (`eb logs`) and confirm the artifact is valid for the platform. |
| Instances unhealthy | Verify security groups, health check path, and that the app binds to the expected port. |
| Worker jobs not processed | Check the SQS queue, worker environment scaling, and application error logs. |

Elastic Beanstalk itself has no additional charge; you pay for the underlying AWS resources it provisions. Application counts, environment counts, and platform version availability are subject to service quotas and supported platform lifecycle. See the Elastic Beanstalk platform and Service Quotas documentation for current values.[^aws-elastic-beanstalk]


## AWS Outposts

An Outpost is a physical extension of an AWS Region into your building: it runs the same APIs locally over a service link back to the Region, while a local gateway connects Outpost resources to your on-premises network. AWS Outposts brings AWS infrastructure, services, APIs, and tools to your premises. An Outpost is a pool of AWS compute and storage capacity installed at your site, operated and managed by AWS as an extension of an AWS Region. You use the same APIs and console as in the Region, with local low latency and local data processing.

Key points:

- Outpost site: the customer-managed physical location where the Outpost is installed.
- Outposts racks: industry-standard 42U racks with servers, switches, and cabling owned and managed by AWS.
- Outposts servers: 1U/2U servers for sites with limited space or smaller capacity needs.
- ACE rack: aggregation/core/edge rack required for deployments of four or more compute racks.
- Service link: the network route between the Outpost and its associated Region.

Practices:

- Validate facility requirements (power, cooling, space, networking) before ordering; plan for the service link bandwidth to the Region.
- Order the right form factor: racks for capacity, servers for small sites; install the ACE rack when scaling to four or more compute racks.
- Design VPC/subnet architecture so Outpost resources are isolated yet connected to the Region.

| Symptom | Check |
| --- | --- |
| Instances fail to launch | Verify Outpost capacity, subnet placement, and instance type availability on the Outpost. |
| High latency to Region | Check service link bandwidth and local gateway routing. |
| Local storage full | Monitor EBS/S3 on Outposts capacity and offload cold data to the Region. |
| Hardware issue | AWS monitors and manages hardware; open a support case for replacement. |

Outposts capacity, instance types, racks per site, and supported services depend on Region and order configuration. See AWS Outposts documentation and the Service Quotas console for current values.[^aws-outposts]


## Application Auto Scaling

Application Auto Scaling is one control loop applied uniformly to many non-EC2 resource types: register a resource as a scalable target with min/max bounds, attach a policy that watches a metric or a clock, and let the loop add or remove capacity within those bounds. Application Auto Scaling automatically scales scalable resources for AWS services other than EC2 instance fleets. You register a scalable resource (for example, a DynamoDB table, ECS service, Lambda function, Aurora replica, or EMR cluster) as a scalable target and attach scaling policies; Application Auto Scaling adjusts capacity in response to the conditions you define.

Key points:

- Scalable target: a resource registered for scaling with a service namespace, resource ID, and min/max capacity (for example, DynamoDB table read/write capacity units, ECS service desired count, Lambda provisioned concurrency).
- Target tracking scaling: keep a CloudWatch metric near a target value (for example, average CPU or queue depth) by adding/removing capacity automatically.
- Step scaling: apply scaling adjustments that vary with the size of the alarm breach (large vs. small deviations).
- Scheduled scaling: scale at a specific time, once or on a recurring schedule (for example, business hours).
- Predictive scaling: proactively scale to match anticipated load based on historical patterns.

Practices:

- Register every scalable resource explicitly and set meaningful min/max bounds to control cost and protect capacity.
- Prefer target tracking on a metric that reflects actual load (utilization, queue depth, requests); avoid noisy metrics.
- Combine scheduled scaling with target tracking for predictable peaks (for example, business hours) and unknown bursts.

| Symptom | Check |
| --- | --- |
| Resource not scaling | Confirm the resource is registered as a scalable target and the policy is attached; check CloudWatch alarm state. |
| Wrong dimension/namespace | Verify the service namespace, resource ID, and scalable dimension match the resource type. |
| Scaling stuck at min/max | Review min/max capacity bounds and the metric values driving the policy. |
| Scheduled action not firing | Check the cron/rate schedule, time zone, and that the scalable target still exists. |

Scaling policies and scheduled actions per scalable target, and per-resource registration counts have quotas. See the Application Auto Scaling endpoints and quotas page and Service Quotas console for current values.[^aws-application-auto-scaling]


## Related

- [Compute](compute.md)
- [Containers and serverless](containers-and-serverless.md)
- [Domain index](index.md)

[^aws-batch]: [AWS Batch - Runbook & Reference](../../sources/aws-batch.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/batch/README.md)
[^aws-lightsail]: [Amazon Lightsail - Runbook & Reference](../../sources/aws-lightsail.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/lightsail/README.md)
[^aws-elastic-beanstalk]: [AWS Elastic Beanstalk - Runbook & Reference](../../sources/aws-elastic-beanstalk.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/elastic-beanstalk/README.md)
[^aws-outposts]: [AWS Outposts - Runbook & Reference](../../sources/aws-outposts.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/outposts/README.md)
[^aws-application-auto-scaling]: [Application Auto Scaling - Runbook & Reference](../../sources/aws-application-auto-scaling.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/application-auto-scaling/README.md)
