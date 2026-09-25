---
type: Service
title: Amazon ECR
description: AWS's container image registry, with IAM-controlled private repositories, scanning, lifecycle cleanup, and replication.
tags: [aws, containers, supply-chain]
sources:
  - id: aws-ecr
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ecr/README.md
    title: "Amazon ECR - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Amazon Elastic Container Registry (ECR) stores Docker and OCI images and artifacts in private (IAM-controlled) or public repositories. A registry is per account per Region.[^aws-ecr]

## Concepts and practices

- Scan on push (basic) or enhanced scanning with Amazon Inspector; fix critical and high findings before deploying.[^aws-ecr]
- Lifecycle policies prune untagged and old images; test rules first.[^aws-ecr]
- Immutable tags stop deployed images being overwritten.[^aws-ecr]
- Cross-Region and cross-account replication; pull-through cache for upstream registries; managed signing on push.[^aws-ecr]
- Repository policies are resource-based IAM policies for push and pull.[^aws-ecr]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Authorization Token has expired` | Re-run `aws ecr get-login-password` and `docker login` |
| Access denied | Repository policy and IAM (`ecr:BatchGetImage`, `ecr:PutImage`) |
| No scan results | Scan config, image pushed after enabling, Region |
| Replication not working | Registry settings, destination, IAM |

As tabled in the note.[^aws-ecr]

## Related

- Source: [Amazon ECR - Runbook & Reference](../../sources/aws-ecr.md)

[^aws-ecr]: Amazon ECR - Runbook & Reference
