---
type: Concept
title: AWS shared responsibility model
description: AWS secures the cloud itself; the customer secures what they put in it, and the split moves toward AWS as services become more managed.
tags: [aws, security, governance]
sources:
  - id: aws-shared-responsibility-model
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/shared-responsibility-model/README.md
    title: "AWS Shared Responsibility Model - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Security in AWS is shared. AWS is responsible for "security of the cloud": facilities, hardware, networking, and the virtualization layer. The customer is responsible for "security in the cloud": guest OS patching, applications, data, IAM, network and firewall configuration, encryption, and regulatory compliance.[^aws-shared-responsibility-model]

| Service model | Example | Who manages the OS |
| --- | --- | --- |
| IaaS | EC2 | Customer |
| PaaS | RDS | AWS |
| SaaS | Fully managed | AWS manages more still |

As described in the note.[^aws-shared-responsibility-model]

## Applying it

- Document per workload who owns data, OS, network, identity, and compliance controls.[^aws-shared-responsibility-model]
- AWS durability does not replace your own tested backups.[^aws-shared-responsibility-model]
- For audits, AWS Artifact reports cover AWS-side controls; you supply evidence for yours.[^aws-shared-responsibility-model]
- It is a governance framework, not an API; actual obligations depend on services used and applicable law.[^aws-shared-responsibility-model]

## Related

- [AWS compute options](compute-options.md)
- Source: [AWS Shared Responsibility Model - Runbook & Reference](../../sources/aws-shared-responsibility-model.md)

[^aws-shared-responsibility-model]: AWS Shared Responsibility Model - Runbook & Reference
