---
type: Service
title: AWS containers and serverless
description: Running containers on ECS or EKS with images in ECR, and running functions on Lambda.
tags:
- aws
- containers
- serverless
aliases:
- engineering/aws/ecs
- engineering/aws/eks
- engineering/aws/ecr
- engineering/aws/lambda
sources:
- id: aws-ecs
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ecs/README.md
  title: Amazon ECS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-eks
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eks/README.md
  title: Amazon EKS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-ecr
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ecr/README.md
  title: Amazon ECR - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-lambda
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/lambda/README.md
  title: AWS Lambda - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Two ways to run code on AWS with less to operate than EC2: containers on Amazon ECS or EKS, pulling images from Amazon ECR, and functions on AWS Lambda.

## Amazon ECS

Amazon Elastic Container Service (ECS) is a fully managed container orchestrator with no control plane to operate.[^aws-ecs]

### Concepts

- Three layers: capacity, controller, and provisioning tools.
- Capacity: ECS Managed Instances, self-managed EC2, AWS Fargate (serverless), and ECS Anywhere (on-premises).
- A task definition is the blueprint (image, CPU, memory, networking, IAM role); a task is a short-lived run; a service keeps tasks running and scales them.
- Service auto scaling sets desired task count; cluster auto scaling manages EC2 capacity.
- Fargate tasks go up to 16 vCPU and 120 GB memory.[^aws-ecs]

### Practices

- Separate a task role (the app's permissions) from an execution role (pulling images and secrets).
- Secrets from Secrets Manager or Parameter Store; target tracking scaling; ELB health checks; CloudWatch Logs; ECR scanning.[^aws-ecs]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Tasks stuck `PENDING` | Capacity, subnet and ENI quotas, VPC endpoints, execution role |
| Cannot place tasks | Task CPU/memory versus cluster capacity, placement constraints |
| Image pull failure | ECR permissions and `ecr:GetAuthorizationToken`, `ecr:BatchGetImage` on the execution role |
| ELB target unhealthy | Health check path, port mapping, SGs |

As tabled in the note.[^aws-ecs] See [AWS compute options](compute.md#choosing-compute).

## Amazon EKS

Amazon Elastic Kubernetes Service (EKS) is managed, certified-conformant Kubernetes. AWS runs the control plane; in EKS standard you manage nodes (managed node groups, Fargate, or self-managed), and EKS Auto Mode also hands nodes, scaling, and patching to AWS.[^aws-eks]

### Concepts

- EKS Capabilities: managed extensions such as Argo CD, AWS Controllers for Kubernetes (ACK), and kro.
- IAM controls access to the Kubernetes API; IRSA (IAM roles for service accounts) or EKS Pod Identity gives pods temporary AWS credentials.
- Storage through the EBS CSI driver, EFS, FSx, and S3.[^aws-eks]

### Practices

- Cluster access through IAM, never shared long-lived kubeconfig credentials.
- Managed node groups or Auto Mode with patched AMIs; Pod Security Standards; image scanning.
- Container Insights, Managed Prometheus, CloudTrail; backups such as Velero; test upgrades on staging.[^aws-eks]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Node `NotReady` | Instance health, kubelet logs, AMI, SGs |
| Pods `Pending` | Requests, capacity, taints, storage classes |
| API unreachable | VPC networking, SGs, `update-kubeconfig` context |
| IRSA `AccessDenied` | Service account annotation and the role's OIDC trust policy |

As tabled in the note.[^aws-eks] See [AWS compute options](compute.md#choosing-compute).

## Amazon ECR

Amazon Elastic Container Registry (ECR) stores Docker and OCI images and artifacts in private (IAM-controlled) or public repositories. A registry is per account per Region.[^aws-ecr]

### Concepts and practices

- Scan on push (basic) or enhanced scanning with Amazon Inspector; fix critical and high findings before deploying.
- Lifecycle policies prune untagged and old images; test rules first.
- Immutable tags stop deployed images being overwritten.
- Cross-Region and cross-account replication; pull-through cache for upstream registries; managed signing on push.
- Repository policies are resource-based IAM policies for push and pull.[^aws-ecr]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| `Authorization Token has expired` | Re-run `aws ecr get-login-password` and `docker login` |
| Access denied | Repository policy and IAM (`ecr:BatchGetImage`, `ecr:PutImage`) |
| No scan results | Scan config, image pushed after enabling, Region |
| Replication not working | Registry settings, destination, IAM |

As tabled in the note.[^aws-ecr]

## AWS Lambda

Lambda runs code without provisioning servers; AWS handles capacity, scaling, and patching. It offers Lambda Functions, which run per event or API call and scale horizontally, and Lambda MicroVMs, isolated environments with state kept for up to 8 hours for per-user or per-job work such as running untrusted code.[^aws-lambda]

### Concepts

- Handlers on managed or custom runtimes; triggers from 200+ AWS services and HTTP endpoints.
- Isolated Firecracker-based execution environments, reused between invocations (warm starts).
- Versions, aliases, and layers; pay per request plus GB-seconds.[^aws-lambda]

### Quotas

| Resource | Quota |
| --- | --- |
| Memory | 128 MB to 10,240 MB (1,769 MB is about 1 vCPU) |
| Timeout | 900 seconds (15 minutes) |
| `/tmp` | 512 MB to 10,240 MB |
| Package | 50 MB zipped, 250 MB unzipped; 10 GB container images |
| Environment variables | 4 KB total |
| Layers | 5 |
| Payload | 6 MB synchronous, 1 MB asynchronous |
| Concurrency | 1,000 per Region by default, adjustable |

As tabled in the note, verified 2026-08-18. Each execution environment serves up to 10 synchronous requests per second.[^aws-lambda]

### Practices

- Stateless, idempotent handlers with least-privilege execution roles.
- DLQs or on-failure destinations for async invocations; Lambda retries async events twice by default.
- Provisioned concurrency and small packages against cold starts.[^aws-lambda]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Timeouts | Timeout value, blocking calls, slow downstreams |
| Throttling (`429`) | Reserved and account concurrency; API Gateway default is 10,000 rps |
| No logs | Execution role has the three `logs:` permissions |
| Async events lost | DLQ or on-failure destination |

As tabled in the note.[^aws-lambda] See [AWS compute options](compute.md#choosing-compute).

## Related

- [Kubernetes IP or ENI exhaustion](../kubernetes/ip-eni-exhaustion.md): a related address-capacity failure in ENI-based pod networks.
- [Kubernetes domain](../kubernetes/index.md)

[^aws-ecs]: [Amazon ECS - Runbook & Reference](../../sources/aws-ecs.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/ecs/README.md)
[^aws-eks]: [Amazon EKS - Runbook & Reference](../../sources/aws-eks.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/eks/README.md)
[^aws-ecr]: [Amazon ECR - Runbook & Reference](../../sources/aws-ecr.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/ecr/README.md)
[^aws-lambda]: [AWS Lambda - Runbook & Reference](../../sources/aws-lambda.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/lambda/README.md)
