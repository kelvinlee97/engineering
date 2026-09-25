---
type: Service
title: Amazon EKS
description: "AWS's managed Kubernetes: AWS runs the control plane, and with Auto Mode also the nodes."
tags: [aws, compute, containers, kubernetes]
sources:
  - id: aws-eks
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eks/README.md
    title: "Amazon EKS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Amazon Elastic Kubernetes Service (EKS) is managed, certified-conformant Kubernetes. AWS runs the control plane; in EKS standard you manage nodes (managed node groups, Fargate, or self-managed), and EKS Auto Mode also hands nodes, scaling, and patching to AWS.[^aws-eks]

## Concepts

- EKS Capabilities: managed extensions such as Argo CD, AWS Controllers for Kubernetes (ACK), and kro.[^aws-eks]
- IAM controls access to the Kubernetes API; IRSA (IAM roles for service accounts) or EKS Pod Identity gives pods temporary AWS credentials.[^aws-eks]
- Storage through the EBS CSI driver, EFS, FSx, and S3.[^aws-eks]

## Practices

- Cluster access through IAM, never shared long-lived kubeconfig credentials.[^aws-eks]
- Managed node groups or Auto Mode with patched AMIs; Pod Security Standards; image scanning.[^aws-eks]
- Container Insights, Managed Prometheus, CloudTrail; backups such as Velero; test upgrades on staging.[^aws-eks]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Node `NotReady` | Instance health, kubelet logs, AMI, SGs |
| Pods `Pending` | Requests, capacity, taints, storage classes |
| API unreachable | VPC networking, SGs, `update-kubeconfig` context |
| IRSA `AccessDenied` | Service account annotation and the role's OIDC trust policy |

As tabled in the note.[^aws-eks] See [AWS compute options](compute-options.md).

## Related

- [Kubernetes domain](../kubernetes/index.md)
- Source: [Amazon EKS - Runbook & Reference](../../sources/aws-eks.md)

[^aws-eks]: Amazon EKS - Runbook & Reference
