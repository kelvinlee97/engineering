---
type: Service
title: AWS Systems Manager
description: "AWS's toolkit for operating fleets of servers through an agent, without SSH: commands, sessions, patching, parameters, and runbooks."
tags: [aws, operations]
sources:
  - id: aws-systems-manager
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/systems-manager/README.md
    title: "AWS Systems Manager - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Systems Manager operates nodes at scale across AWS, on-premises, and other clouds. Nodes running the SSM Agent register as managed nodes, and tools act on them without logging in.[^aws-systems-manager]

| Tool | Purpose |
| --- | --- |
| Run Command | Commands on many nodes without SSH or RDP |
| Session Manager | Audited shells with no inbound ports or bastions |
| Patch Manager | Patch baselines and compliance |
| Automation | Runbooks (SSM documents) for tasks and remediation |
| Parameter Store | Versioned configuration; SecureString with KMS |
| State Manager, Inventory, OpsCenter | Desired state, metadata, operational issues |

As listed in the note.[^aws-systems-manager]

## Practices

- Give nodes a role with `AmazonSSMManagedInstanceCore`; prefer Session Manager to SSH and record sessions.[^aws-systems-manager]
- Restrict `SendCommand` and `StartSession` with IAM and SCPs.[^aws-systems-manager]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Node not managed | Agent running, instance role, outbound access to SSM endpoints |
| Session won't start | Session Manager config, IAM, SSM VPC endpoint or NAT |
| Patching not applied | Baseline, maintenance window, registration |

As tabled in the note.[^aws-systems-manager]

## Related

- Source: [AWS Systems Manager - Runbook & Reference](../../sources/aws-systems-manager.md)

[^aws-systems-manager]: AWS Systems Manager - Runbook & Reference
