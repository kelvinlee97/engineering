---
type: Concept
title: AWS foundations
description: The shared responsibility model and the Well-Architected Framework, the two ideas the other AWS pages assume.
tags:
- aws
aliases:
- engineering/aws/shared-responsibility-model
- engineering/aws/well-architected
sources:
- id: aws-shared-responsibility-model
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/shared-responsibility-model/README.md
  title: AWS Shared Responsibility Model - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-well-architected
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/well-architected/README.md
  title: AWS Well-Architected Framework - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Two ideas the other AWS pages assume: the shared responsibility model, which splits security duties between AWS and the customer, and the Well-Architected Framework, AWS's checklist for reviewing a workload.

## AWS shared responsibility model

Security in AWS is shared. AWS is responsible for "security of the cloud": facilities, hardware, networking, and the virtualization layer. The customer is responsible for "security in the cloud": guest OS patching, applications, data, IAM, network and firewall configuration, encryption, and regulatory compliance.

| Service model | Example | Who manages the OS |
| --- | --- | --- |
| IaaS | EC2 | Customer |
| PaaS | RDS | AWS |
| SaaS | Fully managed | AWS manages more still |

As described in the note.[^aws-shared-responsibility-model]

### Applying it

- Document per workload who owns data, OS, network, identity, and compliance controls.
- AWS durability does not replace your own tested backups.
- For audits, AWS Artifact reports cover AWS-side controls; you supply evidence for yours.
- It is a governance framework, not an API; actual obligations depend on services used and applicable law.[^aws-shared-responsibility-model]

## AWS Well-Architected Framework

The Well-Architected Framework is AWS's set of practices for reliable, secure, efficient, and cost-effective workloads, organized in six pillars. The Well-Architected Tool records a workload's answers to review questions and produces high and medium risk improvement plans.

| Pillar | Focus |
| --- | --- |
| Operational excellence | Run, monitor, improve processes |
| Security | Protect data, systems, assets |
| Reliability | Recover, scale, meet demand |
| Performance efficiency | Use resources efficiently |
| Cost optimization | Avoid unnecessary cost |
| Sustainability | Minimize environmental impact |

As listed in the note.[^aws-well-architected]

### Practices

- Review at design time and at milestones; attach evidence such as diagrams and runbooks.
- Turn high-risk items into owned tasks; use lenses (serverless, SaaS, HPC) or custom lenses.
- The improvement plan only appears once applicable questions are answered.[^aws-well-architected]

## Related

- [AWS compute](compute.md)

[^aws-shared-responsibility-model]: [AWS Shared Responsibility Model - Runbook & Reference](../../sources/aws-shared-responsibility-model.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/shared-responsibility-model/README.md)
[^aws-well-architected]: [AWS Well-Architected Framework - Runbook & Reference](../../sources/aws-well-architected.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/well-architected/README.md)
