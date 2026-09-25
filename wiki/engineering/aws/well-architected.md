---
type: Concept
title: AWS Well-Architected Framework
description: AWS's six-pillar set of design practices, and the tool for reviewing a workload against them.
tags: [aws, architecture]
sources:
  - id: aws-well-architected
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/well-architected/README.md
    title: "AWS Well-Architected Framework - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

The Well-Architected Framework is AWS's set of practices for reliable, secure, efficient, and cost-effective workloads, organized in six pillars. The Well-Architected Tool records a workload's answers to review questions and produces high and medium risk improvement plans.[^aws-well-architected]

| Pillar | Focus |
| --- | --- |
| Operational excellence | Run, monitor, improve processes |
| Security | Protect data, systems, assets |
| Reliability | Recover, scale, meet demand |
| Performance efficiency | Use resources efficiently |
| Cost optimization | Avoid unnecessary cost |
| Sustainability | Minimize environmental impact |

As listed in the note.[^aws-well-architected]

## Practices

- Review at design time and at milestones; attach evidence such as diagrams and runbooks.[^aws-well-architected]
- Turn high-risk items into owned tasks; use lenses (serverless, SaaS, HPC) or custom lenses.[^aws-well-architected]
- The improvement plan only appears once applicable questions are answered.[^aws-well-architected]

## Related

- Source: [AWS Well-Architected Framework - Runbook & Reference](../../sources/aws-well-architected.md)

[^aws-well-architected]: AWS Well-Architected Framework - Runbook & Reference
